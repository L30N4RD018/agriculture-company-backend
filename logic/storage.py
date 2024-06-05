class Storage(object):
    
    """
    Storage is a class that represents a storage for crops.
    """

    def __init__(self,  id: int = None, max_capacity: float = 1.0, 
                        current_capacity: float = 0.0, 
                        storage_ubication: str = 'storage_ubication',
                        equipment: str = 'equipment'):
        """
        Constructor for Storage class.
        :param id: the id of the silo
        :type id: int
        :param max_capacity: the maximum capacity of the silo
        :type max_capacity: float
        :param current_capacity: the current capacity of the silo
        :type current_capacity: float
        :param storage_ubication: the ubication of the silo
        :type storage_ubication: str
        :param equipment: the equipment of the silo
        :type equipment: str
        """
        self._id = id
        self._max_capacity = max_capacity
        self._current_capacity = current_capacity
        self._storage_ubication = storage_ubication
        self._equipment = equipment
    
    @property
    def id(self) -> int:
        """
        Getter for the id attribute.
        :return: the id of the storage
        :rtype: int
        """
        return self._id
    
    @id.setter
    def id(self, value: int):
        """
        Setter for the silo_id attribute.
        :param value: the new value for the id of the storage
        :type value: int
        """
        self._id = value
    
    @property
    def max_capacity(self) -> float:
        """
        Getter for the max_capacity attribute.
        :return: the maximum capacity of the silo
        :rtype: float
        """
        return self._max_capacity
    
    @max_capacity.setter
    def max_capacity(self, value: float):
        """
        Setter for the max_capacity attribute.
        :param value: the new value for the maximum capacity of the silo
        :type value: float
        """
        self._max_capacity = value
    
    @property
    def current_capacity(self) -> float:
        """
        Getter for the current_capacity attribute.
        :return: the current capacity of the silo
        :rtype: float
        """
        return self._current_capacity
    
    @current_capacity.setter
    def current_capacity(self, value: float):
        """
        Setter for the current_capacity attribute.
        :param value: the new value for the current capacity of the silo
        :type value: float
        """
        self._current_capacity = value
    
    @property
    def silo_ubication(self) -> str:
        """
        Getter for the silo_ubication attribute.
        :return: the ubication of the silo
        :rtype: str
        """
        return self._storage_ubication
    
    @silo_ubication.setter
    def silo_ubication(self, value: str):
        """
        Setter for the silo_ubication attribute.
        :param value: the new value for the ubication of the silo
        :type value: str
        """
        self._storage_ubication = value
    
    @property
    def equipment(self) -> str:
        """
        Getter for the equipment attribute.
        :return: the equipment of the silo
        :rtype: str
        """
        return self._equipment
    
    @equipment.setter
    def equipment(self, value: str):
        """
        Setter for the equipment attribute.
        :param value: the new value for the equipment of the silo
        :type value: str
        """
        self._equipment = value
    
    def __str__(self) -> str:
        """
        Method to represent the object as a string.
        :return: the object as a string
        :rtype: str
        """
        return (f'{self._id}, {self._max_capacity}, {self._current_capacity}, {self._storage_ubication}, '
                f'{self._equipment}')
    
    def __dict__(self) -> dict:
        """
        Method to represent the object as a dictionary.
        :return: the object as a dictionary
        :rtype: dict
        """
        return {
            'id': self._id,
            'max_capacity': self._max_capacity,
            'current_capacity': self._current_capacity,
            'storage_ubication': self._storage_ubication,
            'equipment': self._equipment
        }

    def __tuple__(self):
        """
        Method to represent the object as a tuple.
        :return: the object as a tuple
        :rtype: tuple
        """
        return self._max_capacity, self._current_capacity, self._storage_ubication, self._equipment

    def __update_tuple__(self):
        return self._max_capacity, self._current_capacity, self._storage_ubication, self._equipment, self._id
    
    def __eq__(self, other: object) -> bool:
        """
        Method to compare two Storage objects.
        :param other: the other Storage object
        :type other: Storage
        :return: True if both objects are equal, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Storage):
            return False
        return (self._id == other.id and self._max_capacity == other.max_capacity and
                self._current_capacity == other.current_capacity and self._storage_ubication ==
                other._storage_ubication and self._equipment == other.equipment)
    
    def __ne__(self, other: object) -> bool:
        """
        Method to compare two Storage objects.
        :param other: the other Storage object
        :type other: Storage
        :return: True if both objects are not equal, False otherwise
        :rtype: bool
        """
        return not self.__eq__(other)


