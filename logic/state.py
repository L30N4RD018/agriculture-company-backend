from abc import ABC, abstractmethod

class CropState(ABC):    
    @abstractmethod
    def handle(self):
        """
        Handle the crop state.
        :return: the next state
        :rtype: CropState
        """
        pass

class SownState(CropState):    
    def handle(self):        
        return GermidatedState()
    
    def __str__(self) -> str:
        return "Sown"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, SownState)

class GermidatedState(CropState):
    def handle(self):
        return StoragedState()
    
    def __str__(self) -> str:
        return "Germidated"    
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, GermidatedState)    

class StoragedState(CropState):
    def handle(self):
        return DeliveringState()

    def __str__(self) -> str:
        return "Storaged"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, StoragedState)

class DeliveringState(CropState):
    def handle(self):
        return DeliveriedState()
    
    def __str__(self) -> str:
        return "Delivering"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, DeliveringState)

class DeliveriedState(CropState):
    def handle(self):
        return DeliveriedState()
    
    def __str__(self) -> str:
        return "Delivered"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, DeliveriedState)