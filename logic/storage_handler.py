from abc import ABC, abstractmethod
import mysql.connector as mc
import json


QUERYS = json.load(open('config/querys.json'))


class StorageHandler(ABC):
      
    def __init__(self, next_handler = None):
        self.next_handler = next_handler
    
    @abstractmethod
    def handle(self, request: dict):
        if self.next_handler:
            return self.next_handler.handle(request)
        return True


class IdHandler(StorageHandler):        
    def handle(self, request: dict):
        if request['id'] is not None and (request['id'] < 0 or not isinstance(request['id'], int)):
            return {'error': 'Invalid id'}
        return super().handle(request)


class StorageExistenceHandler(StorageHandler):
    
    def __init__(self, next_handler = None, connection = None):
        super().__init__(next_handler)
        self.connection = connection
        
    def handle(self, request: dict):
        if request['id'] is not None:
            cursor = self.connection.cursor()
            cursor.execute(QUERYS['SEARCH_STORAGE'], (request['id'],))
            storage = cursor.fetchone()
            if storage is None:
                return {'error': 'Storage not exist'}
        return super().handle(request)


class MaxCapacityHandler(StorageHandler):        
    def handle(self, request: dict):                  
        if request['max_capacity'] < 0 or not isinstance(request['max_capacity'], int):
            return {'error': 'Invalid max capacity'}
        return super().handle(request)


class CurrentCapacityHandler(StorageHandler):    
    def handle(self, request: dict):        
        if request['current_capacity'] < 0 or request['current_capacity'] > request['max_capacity']:
            return {'error': 'Invalid current capacity'}
        if not isinstance(request['current_capacity'], int):
            return {'error': 'Invalid current capacity'}
        return super().handle(request)


class LocationHandler(StorageHandler):
    def handle(self, request: dict):              
        if request['storage_ubication'] is None:
            return {'error': 'Location is required'}
        if not isinstance(request['storage_ubication'], str):
            return {'error': 'Invalid location'}        
        return super().handle(request)
    

class EquipmentHandler(StorageHandler):
    def handle(self, request: dict):          
        if not isinstance(request['equipment'], str):
            return {'error': 'Invalid equipment'}
        return super().handle(request)

class CapacityHandler(StorageHandler):
    def handle(self, request: dict):
        if request['max_capacity'] < request['current_capacity']:
            return {'error': 'Current capacity must be less than the maximum capacity'}
        return super().handle(request)
    
def storage_validation(request: dict, connection: mc.MySQLConnection) -> dict:
    handler = IdHandler()
    handler = StorageExistenceHandler(handler, connection)
    handler = MaxCapacityHandler(handler)
    handler = CurrentCapacityHandler(handler)
    handler = LocationHandler(handler)
    handler = EquipmentHandler(handler)
    return handler.handle(request)