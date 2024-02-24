from datetime import date

class Delivery(object):
    
    """
    Class used to represent a Delivery.
    """

    def __init__(self, id: int = None, client_name: str = "Client Name", deliver_date: date = date.today(),
                 request_date: date = date.today(), address: str = "Address"):
        """
        Constructor for Delivery class.
        :param id: Delivery id
        :type id: int
        :param client_name: Delivery client name
        :type client_name: str
        :param deliver_date: Delivery deliver date
        :type deliver_date: date
        :param request_date: Delivery request date
        :type request_date: date
        :param address: Delivery address
        :type address: str        
        """
        self._id = id
        self._client_name = client_name.title()
        self._deliver_date = deliver_date
        self._request_date = request_date
        self._address = address.title()
    
    @property
    def id(self) -> int:
        """
        Getter for the delivery id.
        :return: the delivery id
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int) -> None:
        """
        Setter for the delivery id.
        :param id: the delivery id
        :type id: int
        """
        self._id = id
    
    @property
    def client_name(self) -> str:
        """
        Getter for the delivery client name.
        :return: the delivery client name
        :rtype: str
        """
        return self._client_name
    
    @client_name.setter
    def client_name(self, client_name: str) -> None:
        """
        Setter for the delivery client name.
        :param client_name: the delivery client name
        :type client_name: str
        """
        self._client_name = client_name.title()
    
    @property
    def deliver_date(self) -> date:
        """
        Getter for the delivery deliver date.
        :return: the delivery deliver date
        :rtype: date
        """
        return self._deliver_date
    
    @deliver_date.setter
    def deliver_date(self, deliver_date: date) -> None:
        """
        Setter for the delivery deliver date.
        :param deliver_date: the delivery deliver date
        :type deliver_date: date
        """
        self._deliver_date = deliver_date

    @property
    def request_date(self) -> date:
        """
        Getter for the delivery request date.
        :return: the delivery request date
        :rtype: date
        """
        return self._request_date
    
    @request_date.setter
    def request_date(self, request_date: date) -> None:
        """
        Setter for the delivery request date.
        :param request_date: the delivery request date
        :type request_date: date
        """
        self._request_date = request_date
    
    @property
    def address(self) -> str:
        """
        Getter for the delivery address.
        :return: the delivery address
        :rtype: str
        """
        return self._address
    
    @address.setter
    def address(self, address: str) -> None:
        """
        Setter for the delivery address.
        :param address: the delivery address
        :type address: str
        """
        self._address = address.title()
    
    def __str__(self) -> str:
        """
        Method to represent the Delivery as a string.
        :return: the Delivery as a string
        :rtype: str
        """
        return f"Delivery: [{self._id}, {self._client_name}, {self._address}, {self._deliver_date}, {self._request_date}]"

    def __dict__(self) -> dict:
        """
        Method to represent the Delivery as a dictionary.
        :return: the Delivery as a dictionary
        :rtype: dict
        """
        return { "id": self._id, "client_name": self._client_name, 
                "deliver_date": self._deliver_date.isoformat() if self._deliver_date else None,
                "request_date": self._request_date.isoformat() if self._request_date else None, 
                "address": self._address}

    def __tuple__(self) -> tuple:
        """
        Method to represent the Delivery as a tuple.
        :return: the Delivery as a tuple
        :rtype: tuple
        """
        return (self._id, self._client_name, self._deliver_date, self._request_date, self._address)

    def __eq__(self, other: object) -> bool:
        """
        Method to compare two Deliveries.
        :param other: the other Delivery
        :type other: object
        :return: True if both Deliveries are the same, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Delivery):
            return False
        
        return self._id == other.id and self._client_name == other.client_name and self._deliver_date == other.deliver_date and self._request_date == other.request_date and self._address == other.address
    
    def __ne__(self, other: object) -> bool:
        """
        Method to compare two Deliveries.
        :param other: the other Delivery
        :type other: object
        :return: True if both Deliveries are different, False otherwise
        :rtype: bool
        """
        return not self.__eq__(other)

