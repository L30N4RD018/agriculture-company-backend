from logic.storage import Storage

class StorageDecorator(Storage):

    """
    StorageDecorator is a class that represents a decorator for a crop storage.    
    """

    def __init__(self, storage: Storage = Storage()):
        """
        Constructor for StorageDecorator class.
        :param storage: the storage to be decorated.
        :type storage: Storage
        """
        self._storage = storage
    
    @property
    def storage(self) -> Storage:
        """
        Getter for the storage.
        :return: the storage
        :rtype: Storage
        """
        return self._storage
    
    @storage.setter
    def storage(self, storage: Storage) -> None:
        """
        Setter for the storage.
        :param storage: the storage
        :type storage: Storage
        """
        self._storage = storage
    
class StorageCapacityDecorator(object):

    """
    StorageCapacityDecorator is a class that represents a decorator for a crop storage capacity.
    """

    def __init__(self, storage: Storage = Storage()):
        """
        Constructor for StorageCapacityDecorator class.
        :param storage: the storage to be decorated.
        :type storage: Storage
        """
        self._storage = storage
    
    @property
    def storage(self) -> Storage:
        """
        Getter for the storage.
        :return: the storage
        :rtype: Storage
        """
        return self._storage
    
    @storage.setter
    def storage(self, storage: Storage) -> None:
        """
        Setter for the storage.
        :param storage: the storage
        :type storage: Storage
        """
        self._storage = storage
    
    def increase_capacity(self, amount: float) -> None:
        """
        Increase the storage capacity.
        :param amount: the amount to increase
        :type amount: float
        """
        self._storage.current_capacity += amount
    
    def decrease_capacity(self, amount: float) -> None:
        """
        Decrease the storage capacity.
        :param amount: the amount to decrease
        :type amount: float
        """
        self._storage.current_capacity -= amount
