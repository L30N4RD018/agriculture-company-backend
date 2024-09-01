class Smallholding(object):
    
    """
    Class to represent a piece of land.
    """

    def __init__(self, id: int = None, size: float = 0.0, ubication: str = None, shape: str = "Regular o Irregular",
                 delimited: bool = True):
        """
        Constructor for Smallholding class.
        """
        self._id = id
        self._size = size
        self._ubication = ubication
        self._shape = shape.title()
        self._delimited = delimited
    
    @property
    def id(self) -> int:
        """
        Getter for the id attribute.
        :return: the id of the smallholding
        :rtype: int
        """
        return self._id
    
    @id.setter
    def id(self, value: int):
        """
        Setter for the id attribute.
        :param value: the new value for the id of the smallholding
        :type value: int
        """
        self._id = value

    @property
    def size(self) -> float:
        """
        Getter for the size attribute.
        :return: the size of the smallholding
        :rtype: float
        """
        return self._size
    
    @size.setter
    def size(self, value: float):
        """
        Setter for the size attribute.
        :param value: the new value for the size of the smallholding
        :type value: float
        """
        self._size = value
    
    @property
    def ubication(self) -> str:
        """
        Getter for the ubication attribute.
        :return: the ubication of the smallholding
        :rtype: str
        """
        return self._ubication
    
    @ubication.setter
    def ubication(self, value: str):
        """
        Setter for the ubication attribute.
        :param value: the new value for the ubication of the smallholding
        :type value: str
        """
        self._ubication = value
    
    @property
    def shape(self) -> str:
        """
        Getter for the shape attribute.
        :return: the shape of the smallholding
        :rtype: str
        """
        return self._shape
    
    @shape.setter
    def shape(self, value: str):
        """
        Setter for the shape attribute.
        :param value: the new value for the shape of the smallholding
        :type value: str
        """
        self._shape = value
    
    @property
    def delimited(self) -> bool:
        """
        Getter for the delimited attribute.
        :return: delimited of the smallholding
        :rtype: bool
        """
        return self._delimited
    
    @delimited.setter
    def delimited(self, value: bool):
        """
        Setter for the delimited attribute.
        :param value: the new value for the delimitation of the smallholding
        :type value: bool
        """
        self._delimited = value
    
    def __str__(self):
        """
        Method to represent the object as a string.
        :return: the object as a string
        :rtype: str
        """
        return "Smallholding: [size: {}, ubication: {}, shape: {}, delimited: {}]".format(
            self._size, self._ubication, self._shape, self._delimited)

    def __tuple__(self):
        """
        Method to represent the object as a tuple.
        :return: the object as a tuple
        :rtype: tuple
        """
        return self._size, self._ubication, self._shape, self._delimited

    def __update_tuple__(self):
        """
        Method to represent the object as a tuple.
        :return: the object as a tuple
        :rtype: tuple
        """
        return self._size, self._ubication, self._shape, self._delimited, self._id

    def __dict__(self):
        """
        Method to represent the object as a dictionary.
        :return: the object as a dictionary
        :rtype: dict
        """
        return {
            "id": self._id,
            "size": self._size,
            "ubication": self._ubication,
            "shape": self._shape,
            "delimited": self._delimited
        }
    
    def __eq__(self, other: object) -> bool:
        """
        Method to compare two objects.
        :param other: the other object
        :type other: object
        :return: True if the objects are equal, False otherwise
        :rtype: bool
        """
        if isinstance(other, Smallholding):
            return (self._id == other.id and self._size == other.size and self._ubication == other.ubication and
                    self._shape == other.shape and self._delimited == other.delimited)
        return False
    
    def __ne__(self, other: object) -> bool:
        """
        Method to compare two objects.
        :param other: the other object
        :type other: object
        :return: True if the objects are not equal, False otherwise
        :rtype: bool
        """
        return not self.__eq__(other)
