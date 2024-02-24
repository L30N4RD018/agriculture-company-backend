class DeliveryDetails(object):

    """
    Class used to represent the details of a delivery.
    """

    def __init__(self, id: int = None, delivery_id: int = None ,crop_id: int = None, quantity: float = 0.0):
        """
        Constructor for DeliveryDetails class
        :param id: Delivery details id
        :type id: int
        :param delivery_id: Delivery id
        :type delivery_id: int
        :param crop_id: Crop id
        :type crop_id: int
        :param quantity: Quantity of crop
        :type quantity: float
        """
        self._id = id
        self._delivery_id = delivery_id
        self._crop_id = crop_id
        self._quantity = quantity
    
    @property
    def id(self) -> int:
        """
        Getter for the delivery details id.
        :return: the delivery details id
        :rtype: int
        """
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:
        """
        Setter for the delivery details id.
        :param id: the delivery details id
        :type id: int
        """
        self._id = id
    
    @property
    def delivery_id(self) -> int:
        """
        Getter for the delivery id.
        :return: the delivery id
        :rtype: int
        """
        return self._delivery_id
    
    @delivery_id.setter
    def delivery_id(self, delivery_id: int) -> None:
        """
        Setter for the delivery id.
        :param delivery_id: the delivery id
        :type delivery_id: int
        """
        self._delivery_id = delivery_id

    @property
    def crop_id(self) -> int:
        """
        Getter for the crop id.
        :return: the crop id
        :rtype: int
        """
        return self._crop_id

    @crop_id.setter
    def crop_id(self, crop_id: int) -> None:
        """
        Setter for the crop id.
        :param crop_id: the crop id
        :type crop_id: int
        """
        self._crop_id = crop_id
    
    @property
    def quantity(self) -> float:
        """
        Getter for the quantity of crop.
        :return: the quantity of crop
        :rtype: float
        """
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity: float) -> None:
        """
        Setter for the quantity of crop.
        :param quantity: the quantity of crop
        :type quantity: float
        """
        self._quantity = quantity
    
    def __str__(self) -> str:
        """
        Method that returns the string representation of the object.
        :return: the string representation of the object
        :rtype: str
        """
        return f'Delivery details:[{self._id}, {self._delivery_id}, {self._crop_id}, {self._quantity}]'
    
    def __dict__(self) -> dict:
        """
        Method that returns the dictionary representation of the object.
        :return: the dictionary representation of the object
        :rtype: dict
        """
        return {'id': self._id, 'delivery_id': self._delivery_id,
                'crop_id': self._crop_id,'quantity': self._quantity}

    def __tuple__(self) -> tuple:
        """
        Method that returns the tuple representation of the object.
        :return: the tuple representation of the object
        :rtype: tuple
        """
        return (self._id, self._delivery_id, self._crop_id, self._quantity) 

    def __eq__(self, other: object) -> bool:
        """
        Method that returns if two objects are equal.
        :param other: the object to compare
        :type other: object
        :return: if two objects are equal
        :rtype: bool
        """
        if not isinstance(other, DeliveryDetails):
            return False 
        return self._id == other.id and self._delivery_id == other.delivery_id and self._crop_id == other.crop_id and self._quantity == other.quantity
    
    def __ne__(self, other: object) -> bool:
        """
        Method that returns if two objects are different.
        :param other: the object to compare
        :type other: object
        :return: if two objects are different
        :rtype: bool
        """
        return not self.__eq__(other)
    