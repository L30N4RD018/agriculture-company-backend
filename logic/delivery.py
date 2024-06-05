from datetime import date

class Delivery(object):
    def __init__(self, id: int = None, client_name: str = 'client name', deliver_date: date = date.today(),
                 request_date: date = date.today(), address: str = 'address'):
        """
        Constructor for Delivery class.
        """
        self._id = id
        self._client_name = client_name.title()
        self._deliver_date = deliver_date
        self._request_date = request_date
        self._address = address

    @property
    def id(self) -> int:
        """
        Getter for the id attribute.
        :return: the id of the delivery
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, value: int):
        """
        Setter for the id attribute.
        :param value: the new value for the id of the delivery
        :type value: int
        """
        self._id = value

    @property
    def client_name(self) -> str:
        """
        Getter for the client_name attribute.
        :return: the client_name of the delivery
        :rtype: str
        """
        return self._client_name

    @client_name.setter
    def client_name(self, value: str):
        """
        Setter for the client_name attribute.
        :param value: the new value for the client_name of the delivery
        :type value: str
        """
        self._client_name = value

    @property
    def deliver_date(self) -> date:
        """
        Getter for the deliver_date attribute.
        :return: the deliver_date of the delivery
        :rtype: date
        """
        return self._deliver_date

    @deliver_date.setter
    def deliver_date(self, value: date):
        """
        Setter for the deliver_date attribute.
        :param value: the new value for the deliver_date of the delivery
        :type value: date
        """
        self._deliver_date = value

    @property
    def request_date(self) -> date:
        """
        Getter for the request_date attribute.
        :return: the request_date of the delivery
        :rtype: date
        """
        return self._request_date

    @request_date.setter
    def request_date(self, value: date):
        """
        Setter for the request_date attribute.
        :param value: the new value for the request_date of the delivery
        :type value: date
        """
        self._request_date = value

    @property
    def address(self) -> str:
        """
        Getter for the address attribute.
        :return: the address of the delivery
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, value: str):
        """
        Setter for the address attribute.
        :param value: the new value for the address of the delivery
        :type value: str
        """
        self._address = value

    def __str__(self) -> str:
        """
        Method to represent the object as a string.
        :return: the string representing the object
        :rtype: str
        """
        return f'{self.id} {self.client_name} {self.deliver_date} {self.request_date} {self.address}'

    def __eq__(self, other: object) -> bool:
        """
        Method to compare two objects.
        :param other: the other object
        :type other: object
        :return: True if the objects are equal, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Delivery):
            return False
        return self.id == other.id and self.client_name == other.client_name and \
               self.deliver_date == other.deliver_date and self.request_date == other.request_date and \
               self.address == other.address

    def __dict__(self):
        """
        Method to represent the object as a dictionary.
        :return: the object as a dictionary
        :rtype: dict
        """
        return {
            'id': self.id,
            'client_name': self.client_name,
            'deliver_date': self.deliver_date.isoformat() if self.deliver_date is not None else None,
            'request_date': self.request_date.isoformat() if self.request_date is not None else None,
            'address': self.address
        }

    def __tuple__(self):
        """
        Method to represent the object as a tuple.
        :return: the object as a tuple
        :rtype: tuple
        """
        return self.client_name, self.deliver_date, self.request_date, self.address

    def __update_tuple__(self):
        """
        Method to represent the object as a tuple.
        :return: the object as a tuple
        :rtype: tuple
        """
        return self.client_name, self.deliver_date, self.request_date, self.address, self.id
    