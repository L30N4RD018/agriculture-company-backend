from logic.storage import Storage
from fastapi import HTTPException


class StorageDecorator(object):
    
    """
    StorageDecorator is a class that represents a decorator for a crop storage.
    """

    def __init__(self, storage: Storage = Storage ()):
        """
        Constructor for StorageDecorator class.
        :param crop_storage: the crop storage to decorate
        :type crop_storage: Storage
        """
        self._storage = storage
    
    @property
    def crop_storage(self) -> Storage:
        """
        Getter for the crop_storage attribute.
        :return: the crop storage
        :rtype: Storage
        """
        return self._storage
    
    @crop_storage.setter
    def crop_storage(self, value: Storage):
        """
        Setter for the crop_storage attribute.
        :param value: the new value for the crop storage
        :type value: Storage
        """
        self._storage = value


class StorageCapacityDecorator(object):
    
    """
    StorageCapacityDecorator is a class that represents a decorator for a crop storage capacity.
    """

    def __init__(self, storage: Storage =  Storage()):
        """
        Constructor for StorageCapacityDecorator class.
        :param Storage: the crop storage to decorate
        :type Storage: Storage
        """
        self._storage = storage

    @property
    def storage(self) -> Storage:
        """
        Getter for the storage attribute.
        :return: the crop storage
        :rtype: Storage
        """
        return self._storage

    @storage.setter
    def storage(self, value: Storage):
        """
        Setter for the storage attribute.
        :param value: the new value for the crop storage
        :type value: Storage
        """
        self._storage = value
    
    def increase_capacity(self, value: float):
        """
        Increases the capacity of the crop storage.
        :param value: the value to increase the capacity with
        :type value: int
        """
        if self._storage.current_capacity + value > self._storage.max_capacity:
            raise ValueError("The capacity of the storage is exceeded.")
        self._storage.current_capacity += value

    def decrease_capacity(self, value: float):
        """
        Decreases the capacity of the crop storage.
        :param value: the value to decrease the capacity with
        :type value: int
        """
        if self._storage.current_capacity - value < 0:
            raise ValueError("The capacity of the storage cannot be negative.")
        self._storage.current_capacity -= value
