import unittest
from logic.storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = Storage(storage_id=1, max_capacity=100.0, current_capacity=50.0, storage_ubication='Ubication 1', equipment='Equipment 1')

    def test_storage_id(self):
        self.assertEqual(self.storage.storage_id, 1)
        self.storage.storage_id = 2
        self.assertEqual(self.storage.storage_id, 2)

    def test_max_capacity(self):
        self.assertEqual(self.storage.max_capacity, 100.0)
        self.storage.max_capacity = 200.0
        self.assertEqual(self.storage.max_capacity, 200.0)

    def test_current_capacity(self):
        self.assertEqual(self.storage.current_capacity, 50.0)
        self.storage.current_capacity = 75.0
        self.assertEqual(self.storage.current_capacity, 75.0)

    def test_storage_ubication(self):
        self.assertEqual(self.storage.storage_ubication, 'Ubication 1')
        self.storage.storage_ubication = 'Ubication 2'
        self.assertEqual(self.storage.storage_ubication, 'Ubication 2')

    def test_equipment(self):
        self.assertEqual(self.storage.equipment, 'Equipment 1')
        self.storage.equipment = 'Equipment 2'
        self.assertEqual(self.storage.equipment, 'Equipment 2')

    def test_str(self):
        self.assertEqual(str(self.storage), '1, 100.0, 50.0, Ubication 1, Equipment 1')

    def test_dict(self):
        self.assertEqual(self.storage.__dict__(), {'storage_id': 1, 'max_capacity': 100.0, 'current_capacity': 50.0, 'storage_ubication': 'Ubication 1', 'equipment': 'Equipment 1'})

    def test_eq(self):
        storage2 = Storage(storage_id=1, max_capacity=100.0, current_capacity=50.0, storage_ubication='Ubication 1', equipment='Equipment 1')
        storage3 = Storage(storage_id=2, max_capacity=200.0, current_capacity=75.0, storage_ubication='Ubication 2', equipment='Equipment 2')
        self.assertEqual(self.storage, storage2)
        self.assertNotEqual(self.storage, storage3)

if __name__ == '__main__':
    unittest.main()