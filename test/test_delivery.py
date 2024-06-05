import unittest
from logic.delivery import Delivery
from datetime import date

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.delivery = Delivery(id_delivery=1, client_name='Bruce Wayne', deliver_date=date.today(),
                                 request_date=date.today(), address='Address 1')

    def test_id_delivery(self):
        self.assertEqual(self.delivery.id_delivery, 1)
        self.delivery.id_delivery = 2
        self.assertEqual(self.delivery.id_delivery, 2)

    def test_client_name(self):
        self.assertEqual(self.delivery.client_name, 'Bruce Wayne')
        self.delivery.client_name = 'Clark Kent'
        self.assertEqual(self.delivery.client_name, 'Clark Kent')

    def test_deliver_date(self):
        self.assertEqual(self.delivery.deliver_date, date.today())
        self.delivery.deliver_date = date(2020, 12, 31)
        self.assertEqual(self.delivery.deliver_date, date(2020, 12, 31))

    def test_request_date(self):
        self.assertEqual(self.delivery.request_date, date.today())
        self.delivery.request_date = date(2020, 12, 31)
        self.assertEqual(self.delivery.request_date, date(2020, 12, 31))

    def test_address(self):
        self.assertEqual(self.delivery.address, 'Address 1')
        self.delivery.address = 'Address 2'
        self.assertEqual(self.delivery.address, 'Address 2')

    def test_str(self):
        self.assertEqual(str(self.delivery), '1 Bruce Wayne {0} {0} Address 1'.format(date.today()))

    def test_dict(self):
        self.assertEqual(self.delivery.__dict__(), {'id_delivery': 1, 'client_name': 'Bruce Wayne',
                                                    'deliver_date': date.today(), 'request_date': date.today(),
                                                    'address': 'Address 1'})

    def test_eq(self):
        delivery2 = Delivery(id_delivery=1, client_name='Bruce Wayne', deliver_date=date.today(),
                             request_date=date.today(), address='Address 1')
        delivery3 = Delivery(id_delivery=2, client_name='Clark Kent', deliver_date=date(2020, 12, 31),
                             request_date=date(2020, 12, 31), address='Address 2')
        self.assertEqual(self.delivery, delivery2)
        self.assertNotEqual(self.delivery, delivery3)


if __name__ == '__main__':
    unittest.main()
