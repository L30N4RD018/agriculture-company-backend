import unittest
from logic.smallholding import Smallholding

class TestSmallholding(unittest.TestCase):
    def setUp(self):
        self.smallholding = Smallholding(id=1, size=10.0, ubication="Somewhere", shape="Regular", delimited=True)

    def test_id(self):
        self.assertEqual(self.smallholding.id, 1)
        self.smallholding.id = 2
        self.assertEqual(self.smallholding.id, 2)

    def test_size(self):
        self.assertEqual(self.smallholding.size, 10.0)
        self.smallholding.size = 20.0
        self.assertEqual(self.smallholding.size, 20.0)

    def test_ubication(self):
        self.assertEqual(self.smallholding.ubication, "Somewhere")
        self.smallholding.ubication = "Nowhere"
        self.assertEqual(self.smallholding.ubication, "Nowhere")

    def test_shape(self):
        self.assertEqual(self.smallholding.shape, "Regular")
        self.smallholding.shape = "Irregular"
        self.assertEqual(self.smallholding.shape, "Irregular")

    def test_delimited(self):
        self.assertEqual(self.smallholding.delimited, True)
        self.smallholding.delimited = False
        self.assertEqual(self.smallholding.delimited, False)

    def test_str(self):
        self.assertEqual(str(self.smallholding), "Smallholding: [size: 10.0, ubication: Somewhere, shape: Regular, delimited: True]")

    def test_tuple(self):
        self.assertEqual(self.smallholding.__tuple__(), (10.0, "Somewhere", "Regular", True))

    def test_dict(self):
        self.assertEqual(self.smallholding.__dict__(), {"size": 10.0, "ubication": "Somewhere", "shape": "Regular", "delimited": True})

    def test_eq(self):
        other_smallholding = Smallholding(id=1, size=10.0, ubication="Somewhere", shape="Regular", delimited=True)
        self.assertEqual(self.smallholding, other_smallholding)

    def test_ne(self):
        other_smallholding = Smallholding(id=2, size=20.0, ubication="Nowhere", shape="Irregular", delimited=False)
        self.assertNotEqual(self.smallholding, other_smallholding)

if __name__ == '__main__':
    unittest.main()