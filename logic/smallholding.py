class Smallholding(object):

    """
    Class used to represent a Smallholding.
    """

    def __init__(self, id: int = None, size: float = 0.0, ubication: str = None,
                 shape: str = "Rectangular", delimited: bool = False):
        """
        Constructor for Smallholding class
        :param id: Smallholding id
        :type id: int
        :param size: Smallholding size
        :type size: float
        :param ubication: Smallholding ubication
        :type ubication: str
        :param shape: Smallholding shape
        :type shape: str
        :param delimited: Smallholding delimited
        :type delimited: bool
        """
        self._id = id
        self._size = size
        self._ubication = ubication
        self._shape = shape
        self._delimited = delimited
    
    @property
    def id(self) -> int:
        """
        Getter for the smallholding id.
        :return: the smallholding id
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int) -> None:
        """
        Setter for the smallholding id.
        :param id: the smallholding id
        :type id: int
        """
        self._id = id
    
    @property
    def size(self) -> float:
        """
        Getter for the smallholding size.
        :return: the smallholding size
        :rtype: float
        """
        return self._size
    
    @size.setter
    def size(self, size: float) -> None:
        """
        Setter for the smallholding size.
        :param size: the smallholding size
        :type size: float
        """
        self._size = size
    
    @property
    def ubication(self) -> str:
        """
        Getter for the smallholding ubication.
        :return: the smallholding ubication
        :rtype: str
        """
        return self._ubication
    
    @ubication.setter
    def ubication(self, ubication: str) -> None:
        """
        Setter for the smallholding ubication.
        :param ubication: the smallholding ubication
        :type ubication: str
        """
        self._ubication = ubication
    
    @property
    def shape(self) -> str:
        """
        Getter for the smallholding shape.
        :return: the smallholding shape
        :rtype: str
        """
        return self._shape
    
    @shape.setter
    def shape(self, shape: str) -> None:
        """
        Setter for the smallholding shape.
        :param shape: the smallholding shape
        :type shape: str
        """
        self._shape = shape
    
    @property
    def delimited(self) -> bool:
        """
        Getter for the smallholding delimited.
        :return: the smallholding delimited
        :rtype: bool
        """
        return self._delimited
    
    @delimited.setter
    def delimited(self, delimited: bool) -> None:
        """
        Setter for the smallholding delimited.
        :param delimited: the smallholding delimited
        :type delimited: bool
        """
        self._delimited = delimited
    
    def __str__(self) -> str:
        """
        Method used to represent a Smallholding as a string
        :return: the smallholding as a string
        :rtype: str
        """
        return f"Smallholding: [{self._id}, {self._size}, {self._ubication}, {self._shape}, {self._delimited}]"

    def __dict__(self) -> dict:
        """
        Method used to represent a Smallholding as a dictionary
        :return: the smallholding as a dictionary
        :rtype: dict
        """
        return {"id": self._id, "size": self._size, "ubication": self._ubication, "shape": self._shape, "delimited": 'Yes' if self._delimited else 'No'}
    
    def __tuple__(self) -> tuple:
        """
        Method used to represent a Smallholding as a tuple
        :return: the smallholding as a tuple
        :rtype: tuple
        """
        return (self._id, self._size, self._ubication, self._shape, self._delimited)

    def __eq__(self, other: object) -> bool:
        """
        Method used to compare two Smallholdings
        :param other: the other Smallholding
        :type other: object
        :return: True if they are equal, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Smallholding):
            return False
        return self._id == other.id and self._size == other.size and self._ubication == other.ubication and self._shape == other.shape and self._delimited == other.delimited

    def __ne__(self, other: object) -> bool:
        """
        Method used to compare two Smallholdings
        :param other: the other Smallholding
        :type other: object
        :return: True if they are not equal, False otherwise
        :rtype: bool
        """
        return not self.__eq__(other)
    

