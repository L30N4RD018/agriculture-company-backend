from __future__ import annotations
from logic.state import CropState, SownState
from datetime import date

class Crop(object):

    """
    Class used to represent a Crop
    """

    def __init__(self, id: int = None, type: str = 'Crop Type',
                 state: CropState = SownState(), sow_date: date = date.today(),
                 harvest_date: date = None, storage_id: int = None,
                 smallholding_id: int = None, quantity: int = 0):
        """
        Constructor for Crop class
        :param id: Crop id
        :type id: int
        :param type: Crop type
        :type type: str
        :param state: Crop state
        :type state: str
        :param sow_date: Crop sow date
        :type sow_date: date
        :param harvest_date: Crop harvest date
        :type harvest_date: date
        :param storage_id: Crop storage id
        :type storage_id: int
        :param smallholding_id: Crop smallholding id
        :type smallholding_id: int
        :param quantity: Crop quantity
        :type quantity: int        
        """
        self._id = id
        self._type = type.capitalize()
        self._state = state
        self._sow_date = sow_date
        self._harvest_date = harvest_date
        self._storage_id = storage_id
        self._smallholding_id = smallholding_id
        self._quantity = quantity
    
    @property
    def id(self) -> int:
        """
        Getter for the crop id.
        :return: the crop id
        :rtype: int
        """
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:        
        """
        Setter for the crop id.
        :param id: the crop id
        :type id: int
        """
        self._id = id
    
    @property
    def type(self) -> str:
        """
        Getter for the crop type.
        :return: the crop type
        :rtype: str
        """
        return self._type
    
    @type.setter
    def type(self, type: str) -> None:
        """
        Setter for the crop type.
        :param type: the crop type
        :type type: str
        """
        self._type = type
    
    @property
    def state(self) -> str:
        """
        Getter for the crop state.
        :return: the crop state
        :rtype: str
        """
        return self._state
    
    @state.setter
    def state(self, state: CropState) -> None:
        """
        Setter for the crop state.
        :param state: the crop state
        :type state: str
        """
        self._state = state        

    @property
    def sow_date(self) -> date:
        """
        Getter for the crop sow date.
        :return: the crop sow date
        :rtype: date
        """
        return self._sow_date
    
    @sow_date.setter
    def sow_date(self, sow_date: date) -> None:
        """
        Setter for the crop sow date.
        :param sow_date: the crop sow date
        :type sow_date: date
        """
        self._sow_date = sow_date

    @property
    def harvest_date(self) -> date:
        """
        Getter for the crop harvest date.
        :return: the crop harvest date
        :rtype: date
        """
        return self._harvest_date
    
    @harvest_date.setter
    def harvest_date(self, harvest_date: date) -> None:
        """
        Setter for the crop harvest date.
        :param harvest_date: the crop harvest date
        :type harvest_date: date
        """
        self._harvest_date = harvest_date
    
    @property
    def storage_id(self) -> int:
        """
        Getter for the crop storage id.
        :return: the crop storage id
        :rtype: int
        """
        return self._storage_id
    
    @storage_id.setter
    def storage_id(self, storage_id: int) -> None:
        """
        Setter for the crop storage id.
        :param storage_id: the crop storage id
        :type storage_id: int
        """
        self._storage_id = storage_id
    
    @property
    def smallholding_id(self) -> int:
        """
        Getter for the crop smallholding id.
        :return: the crop smallholding id
        :rtype: int
        """
        return self._smallholding_id
    
    @smallholding_id.setter
    def smallholding_id(self, smallholding_id: int) -> None:
        """
        Setter for the crop smallholding id.
        :param smallholding_id: the crop smallholding id
        :type smallholding_id: int
        """
        self._smallholding_id = smallholding_id    
    
    @property
    def quantity(self) -> int:
        """
        Getter for the crop quantity.
        :return: the crop quantity
        :rtype: int
        """
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity: int) -> None:
        """
        Setter for the crop quantity.
        :param quantity: the crop quantity
        :type quantity: int
        """
        self._quantity = quantity    
    
    def __str__(self) -> str:
        """
        Methor used to represent a Crop as a string.
        :return: the crop as a string.
        :rtype: str
        """
        return f'Crop: [{self._id}, {self._type}, {self._state.__str__()}, {self._sow_date}, {self._harvest_date}, {self._storage_id}, {self._smallholding_id}, {self._quantity}]'
    
    def __dict__(self) -> dict:
        """
        Method used to represent a Crop as a dictionary.
        :return: the crop as a dictionary
        :rtype: dict
        """
        return {'id': self._id, 'type': self._type, 'state': self._state.__str__(), 
                'sow_date': self._sow_date.isoformat() if self._sow_date else None
                , 'harvest_date': self._harvest_date.isoformat() if self._harvest_date else None, 
                'storage_id': self._storage_id, 'smallholding_id': self._smallholding_id, 
                'quantity': self._quantity}
    
    def __tuple__(self) -> tuple:
        """
        Method used to represent a Crop as a tuple.
        :return: the crop as a tuple
        :rtype: tuple
        """
        return (self._id,self._type, self._state.__str__(), self._sow_date, 
                self._harvest_date, self._storage_id, self._smallholding_id, 
                self._quantity)

    def __eq__(self, other: object) -> bool:
        """
        Method used to compare two crops.
        :param other: the other crop
        :type other: Crop
        :return: True if the crops are the same, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Crop):
            return False
        return self._id == other.id and self._type == other.type and self._state == other.state and self._sow_date == other.sow_date and self._harvest_date == other.harvest_date and self._storage_id == other.storage_id and self._smallholding_id == other.smallholding_id and self._quantity == other.quantity
    
    def __ne__(self, other: object) -> bool:
        """
        Method used to compare two crops.
        :param other: the other crop
        :type other: Crop
        :return: True if the crops are different, False otherwise
        :rtype: bool
        """
        return not self.__eq__(other)
            

