from abc import ABC, abstractmethod
import mysql.connector as mc
import json


QUERYS = json.load(open('config/querys.json'))

class CropHandler(ABC):
      
    def __init__(self, next_handler = None):
        self.next_handler = next_handler
    
    @abstractmethod
    def handle(self, request: dict) :
        if self.next_handler:
            return self.next_handler.handle(request)
        return True

class IdHandler(CropHandler):
    
    def handle(self, request: dict):
        if request['id'] is not None and (request['id'] < 0 or not isinstance(request['id'], int)):
            return {'error': 'Invalid id'}
        return super().handle(request)

        
class StateHandler(CropHandler):        
    
    def handle(self, request: dict):
        if request['state'] not in ('Sown', 'Germinated', 'Harvested', 'Stored', 'Delivered', 'Delivering'):
            return {'error': 'Invalid state'}
        
        if request['state'] == 'Sown':
            if request['sow_date'] is None:
                return {'error': 'Sow date is required for this state'}
            if request['harvest_date'] is not None:
                return {'error': 'Harvest date is not required for this state'}
            if request['storage_id'] is not None:
                return {'error': 'Storage id is not required for this state'}
            if request['smallholding_id'] is None:
                return {'error': 'Smallholding id is required for this state'}            
        
        if request['state'] in ('Germinated', 'Harvested', 'Stored', 'Delivered', 'Delivering'):
            if request['sow_date'] is None or request['harvest_date'] is None:
                return {'error': 'Sow and harvest dates are required for this state'}            
            if request['storage_id'] is None:
                return {'error': 'Storage id is required for this state'}
                    
        if request['state'] in ('Stored', 'Delivered', 'Delivering') and request['storage_id'] is None:
            return {'error': 'Storage id is required'}
             
        return super().handle(request)


class DatesHandler(CropHandler):        
    
    def handle(self, request: dict):
        if request['sow_date'] is not None and request['harvest_date'] is not None:
            if request['sow_date'] > request['harvest_date']:
                return {'error': 'Sow date must be before harvest date'}
        return super().handle(request)


class QuantityHandler(CropHandler):
    
    def handle(self, request: dict):
        if request['quantity'] < 0:
            return {'error': 'Quantity must be a positive number'}
        return super().handle(request)


class SmallholdingHandler(CropHandler):
    
    def __init__(self, next_handler = None, connection = None):
        super().__init__(next_handler)
        self.connection = connection
    
    def handle(self, request: dict):        
        if request['smallholding_id'] is not None:
            if request['smallholding_id'] < 0:
                return {'error': 'Smallholding id must be a positive number'}
            cursor = self.connection.cursor()
            try:
                cursor.execute(QUERYS['SEARCH_SMALLHOLDING'], (request['smallholding_id'],))
                if not cursor.fetchone():
                    return {'error': 'Smallholding not found'}                
            except mc.Error:
                return {'error': 'Error while searching for smallholding'}
            finally:
                cursor.close()
        return super().handle(request)


class StorageHandler(CropHandler):
    
    def __init__(self, next_handler = None, connection = None):
        super().__init__(next_handler)
        self.connection = connection
    
    def handle(self, request: dict):        
        if request['storage_id'] is not None:            
            if request['storage_id'] < 0:
                return {'error': 'Storage id must be a positive number'}
            cursor = self.connection.cursor()
            try:
                cursor.execute(QUERYS['SEARCH_STORAGE'], (request['storage_id'],))
                if not cursor.fetchone():
                    return {'error': 'Storage not found'}                
            except mc.Error:
                return {'error': 'Error while searching for storage'}
            finally:
                cursor.close()
        return super().handle(request)

def crop_validation(request: dict, connection: mc.MySQLConnection) -> dict:
    handler = IdHandler()
    handler = StateHandler(handler)
    handler = DatesHandler(handler)
    handler = QuantityHandler(handler)
    handler = SmallholdingHandler(handler, connection)
    handler = StorageHandler(handler, connection)
    return handler.handle(request)