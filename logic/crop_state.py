from __future__ import annotations
from abc import ABC, abstractmethod

class CropState(ABC):

    """
    CropState is a class that represents the state of a crop.
    """
        
    @property
    def crop(self) -> object:
        """
        Getter for the crop.
        :return: the crop
        :rtype: Crop
        """
        return self._crop
    
    @crop.setter
    def crop(self, crop: object) -> None:
        """
        Setter for the crop.
        :param crop: the new crop
        :type crop: Crop
        :return: None
        """
        self._crop = crop

    @abstractmethod
    def execute_state(self) -> None:
        pass

    @abstractmethod
    def transition(self) -> None:
        pass


class Sown(CropState):

    """
    StateSown is a class that represents the sown state of a crop.
    """    

    def execute_state(self):
        """
        Executes the sown state of a crop.
        """

    def transition(self):
        """
        Changes the state of a crop to germinated.
        """
        self.crop.change_state(Germinated())


class Germinated(CropState):
    """
    StateGerminated is a class that represents the germinated state of a crop.
    """    

    def execute_state(self):
        """
        Executes the germinated state of a crop.
        """

    def transition(self):
        """
        Changes the state of a crop to growth.
        """
        self.crop.chansow_datege_state(Storaged())


class Storaged(CropState):

    """
    StateStoraged is a class that represents the storaged state of a crop.
    """

    def execute_state(self):
        """
        Executes the storaged state of a crop.
        """

    def transition(self):
        """
        Changes the state of a crop to sown.
        """
        self.crop.change_state(Delivering())


class Delivering(CropState):

    """
    StateDelivering is a class that represents the delivering state of a crop.
    """

    def execute_state(self):
        """
        Executes the delivering state of a crop.
        """

    def transition(self):
        """
        Changes the state of a crop to sown.
        """
        self.crop.change_state(Delivered())


class Delivered(CropState):

    """
    StateDelivered is a class that represents the delivered state of a crop.
    """

    def execute_state(self):
        """
        Executes the delivered state of a crop.
        """

    def transition(self):
        """
        Changes the state of a crop to sown.
        """
        pass