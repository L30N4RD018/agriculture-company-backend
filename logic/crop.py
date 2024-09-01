from __future__ import annotations
from datetime import date
from logic.crop_state import Sown, Germinated, Storaged, Delivering, Delivered


class Crop(object):
    """
    Class used to represent a crop.
    """
    def __init__(self, id: int = None, type: str = 'type',
                 state: str = None, sow_date: date = date.today(),
                 harvest_date: date = None, storage_id: int = None,
                 smallholding_id: int = None, quantity: int = 0) -> None:
        """
        Constructor for the Crop class.
        :param id: the id of the crop
        :type id: int
        :param type: the type of the crop
        :type type: str
        :param state: the state of the crop
        :type state: object
        :param sow_date: the date the crop was sown
        :type sow_date: datetime
        :param harvest_date: the date the crop was harvested
        :type harvest_date: datetime
        :param storage_id: the id of the storage where the crop is stored
        :type storage_id: int
        :param smallholding_id: the id of the smallholding where the crop is stored
        :type smallholding_id: int
        :param quantity: the quantity of the crop
        :type quantity: int
        """
        self._id = id
        self._type = type.title() if type is not None else None
        self._state = state.title() if state is not None else None
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
        :param id: the new crop id
        :type id: int
        :return: None
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
        :param type: the new crop type
        :type type: str
        :return: None
        """
        self._type = type
    
    @property
    def state(self) -> object:
        """
        Getter for the crop state.
        :return: the crop state
        :rtype: object
        """
        return self._state
    
    @state.setter
    def state(self, state: object) -> None:
        """
        Setter for the crop state.
        :param state: the new crop state
        :type state: object
        :return: None
        """
        self._state = state
    
    @property
    def sow_date(self) -> date:
        """
        Getter for the crop sow date.
        :return: the crop sow date
        :rtype: datetime
        """
        return self._sow_date
    
    @sow_date.setter
    def sow_date(self, sow_date: date) -> None:
        """
        Setter for the crop sow date.
        :param sow_date: the new crop sow date
        :type sow_date: datetime
        :return: None
        """
        self._sow_date = sow_date
    
    @property
    def harvest_date(self) -> date:
        """
        Getter for the crop harvest date.
        :return: the crop harvest date
        :rtype: datetime
        """
        return self._harvest_date
    
    @harvest_date.setter
    def harvest_date(self, harvest_date: date) -> None:
        """
        Setter for the crop harvest date.
        :param harvest_date: the new crop harvest date
        :type harvest_date: datetime
        :return: None
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
        :param storage_id: the new crop storage id
        :type storage_id: int
        :return: None
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
        :param smallholding_id: the new crop smallholding id
        :type smallholding_id: int
        :return: None
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
        :param quantity: the new crop quantity
        :type quantity: int
        :return: None
        """
        self._quantity = quantity
    
    def change_state(self, state: str):
        """
        Method used to change the state of a crop.
        :param state: the new state of the crop
        :type state: str
        :return: None
        """
        states = {'sown': Sown(), 'germinated': Germinated(), 'storaged': Storaged(), 'delivering': Delivering(),
                  'delivered': Delivered()}
        self._state = states[state.lower()]
        self.state.crop = self
        return self

    def __str__(self) -> str:
        """
        Method used to represent the crop as a string.
        :return: the crop as a string
        :rtype: str
        """
        return (f'({self._type}, {self._state}, {self._sow_date}, {self._harvest_date}, '
                f'{self._storage_id}, {self._smallholding_id},{self._quantity})')
    
    def __dict__(self) -> dict:
        """
        Method used to represent the crop as a dictionary.
        :return: the crop as a dictionary
        :rtype: dict
        """
        return {
                'id': self._id, 'type': self._type, 'state': self._state, 
                'sow_date': self._sow_date.isoformat() if self._sow_date is not None else None,
                'harvest_date': self._harvest_date.isoformat() if self._harvest_date is not None else None,
                'storage_id': self._storage_id, 
                'smallholding_id': self._smallholding_id, 
                'quantity': self._quantity
                }
    
    def __eq__(self, other: object) -> bool:
        """
        Method used to check if two crops are equal.
        :param other: the other crop
        :type other: Crop
        :return: True if the crops are equal, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Crop):
            return False
        return  self._id == other._id and self._type == other._type and \
                self._state == other._state and self._sow_date == other._sow_date and \
                self._harvest_date == other._harvest_date and self._quantity == other._quantity and \
                self._storage_id == other._storage_id and self._smallholding_id == other._smallholding_id
    
    def __ne__(self, other) -> bool:
        """
        Method used to check if two crops are not equal.
        :param other: the other crop
        :type other: Crop
        :return: True if the crops are not equal, False otherwise
        :rtype: bool
        """
        return not self == other

    def __tuple__(self) -> tuple:
        """
        Method used to represent the crop as a tuple.
        :return: the crop as a tuple
        :rtype: tuple
        """
        return (self._type, self._state, self._sow_date, self._harvest_date, 
                self._storage_id, self._smallholding_id, self._quantity)

    def __update_tuple__(self) -> tuple:
        """
        Method used to represent the crop as a tuple.
        :return: the crop as a tuple
        :rtype: tuple
        """
        return (self._type, self._state, self._sow_date, self._harvest_date, 
                self._storage_id, self._smallholding_id,  self._quantity, self._id)