class Storage(object):

    """
    Storage is a class that represents a storage for crops.
    """

    def __init__(self, id: int = None, max_capacity: float = 1.0,
                 current_capacity: float = 0.0, ubication: str = 'Ubication',
                 equipment: str = 'Equipment'):
        """
        Constructor for Storage class.
        :param id: the id of the storage.
        :type id: int
        :param max_capacity: the maximum capacity of the storage.
        :type max_capacity: float
        :param current_capacity: the current capacity of the storage.
        :type current_capacity: float
        :param ubication: the ubication of the storage.
        :type ubication: str
        :param equipment: the equipment of the storage.
        :type equipment: str        
        """

        self._id = id
        self._max_capacity = max_capacity
        self._current_capacity = current_capacity
        self._ubication = ubication.title()
        self._equipment = equipment
    
    @property
    def id(self) -> int:
        """
        Getter for the storage id.
        :return: the storage id
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int) -> None:
        """
        Setter for the storage id.
        :param id: the storage id
        :type id: int
        """
        self._id = id
    
    @property
    def max_capacity(self) -> float:
        """
        Getter for the storage max capacity.
        :return: the storage max capacity
        :rtype: float
        """
        return self._max_capacity
    
    @max_capacity.setter
    def max_capacity(self, max_capacity: float) -> None:
        """
        Setter for the storage max capacity.
        :param max_capacity: the storage max capacity
        :type max_capacity: float
        """
        self._max_capacity = max_capacity
    
    @property
    def current_capacity(self) -> float:
        """
        Getter for the storage current capacity.
        :return: the storage current capacity
        :rtype: float
        """
        return self._current_capacity
    
    @current_capacity.setter
    def current_capacity(self, current_capacity: float) -> None:
        """
        Setter for the storage current capacity.
        :param current_capacity: the storage current capacity
        :type current_capacity: float
        """
        self._current_capacity = current_capacity
    
    @property
    def ubication(self) -> str:
        """
        Getter for the storage ubication.
        :return: the storage ubication
        :rtype: str
        """
        return self._ubication
    
    @ubication.setter
    def ubication(self, ubication: str) -> None:
        """
        Setter for the storage ubication.
        :param ubication: the storage ubication
        :type ubication: str
        """
        self._ubication = ubication.title()
    
    @property
    def equipment(self) -> str:
        """
        Getter for the storage equipment.
        :return: the storage equipment
        :rtype: str
        """
        return self._equipment

    @equipment.setter
    def equipment(self, equipment: str) -> None:
        """
        Setter for the storage equipment.
        :param equipment: the storage equipment
        :type equipment: str
        """
        self._equipment = equipment.title()

    def __str__(self) -> str:
        """
        Method to represent the storage as a string.
        :return: the storage as a string
        :rtype: str
        """
        return f"Storage: [{self._id},{self._max_capacity},{self._current_capacity} ,{self._ubication}, {self._equipment}]"

    def __dict__(self) -> dict:
        """
        Method to represent the storage as a dictionary.
        :return: the storage as a dictionary
        :rtype: dict
        """
        return {"id": self._id, "max_capacity": self._max_capacity, "current_capacity": self._current_capacity, "ubication": self._ubication, "equipment": self._equipment}

    def __tuple__(self) -> tuple:
        """
        Method to represent the storage as a tuple.
        :return: the storage as a tuple
        :rtype: tuple
        """
        return (self._id, self._max_capacity, self._current_capacity, self._ubication, self._equipment)

    def __eq__(self, other: object) -> bool:
        """
        Method to compare two storages.
        :param other: the other storage
        :type other: object
        :return: True if the storages are the same, False otherwise
        """
        
        if not isinstance(other, Storage):
            return False
        
        return self._id == other.id and self._max_capacity == other.max_capacity and self._current_capacity == other.current_capacity and self._ubication == other.ubication and self._equipment == other.equipment
    
    def __ne__(self, other: object) -> bool:
        """
        Method to compare two storages.
        :param other: the other storage
        :type other: object
        :return: True if the storages are different, False otherwise
        """
        return not self.__eq__(other)

    