import unittest
from datetime import datetime
from logic.crop import Crop

class TestCrop(unittest.TestCase):
    def setUp(self):
        self.crop = Crop(crop_id=1, crop_type='corn', state='growing', quantity=100)
    
    def test_crop_id(self):
        self.assertEqual(self.crop.crop_id, 1)
        self.crop.crop_id = 2
        self.assertEqual(self.crop.crop_id, 2)
    
    def test_crop_type(self):
        self.assertEqual(self.crop.crop_type, 'corn')
        self.crop.crop_type = 'wheat'
        self.assertEqual(self.crop.crop_type, 'wheat')
    
    def test_state(self):
        self.assertEqual(self.crop.state, 'growing')
        self.crop.state = 'harvested'
        self.assertEqual(self.crop.state, 'harvested')
    
    def test_sow_date(self):
        self.assertEqual(self.crop.sow_date.date(), datetime.now().date())
        new_date = datetime(2022, 1, 1)
        self.crop.sow_date = new_date
        self.assertEqual(self.crop.sow_date, new_date)
    
    def test_harvest_date(self):
        self.assertEqual(self.crop.harvest_date.date(), datetime.now().date())
        new_date = datetime(2022, 2, 1)
        self.crop.harvest_date = new_date
        self.assertEqual(self.crop.harvest_date, new_date)
    
    def test_storage_id(self):
        self.assertIsNone(self.crop.storage_id)
        self.crop.storage_id = 1
        self.assertEqual(self.crop.storage_id, 1)
    
    def test_smallholding_id(self):
        self.assertIsNone(self.crop.smallholding_id)
        self.crop.smallholding_id = 2
        self.assertEqual(self.crop.smallholding_id, 2)
    
    def test_quantity(self):
        self.assertEqual(self.crop.quantity, 100)
        self.crop.quantity = 200
        self.assertEqual(self.crop.quantity, 200)
    
    def test_change_state(self):
        self.crop.change_state('harvested')
        self.assertEqual(self.crop.state, 'harvested')

    def test_str(self):
        self.assertEqual(str(self.crop), '1, corn, growing, 100, None, None, None, None')
    
    def test_dict(self):
        self.assertEqual(self.crop.__dict__(), {'crop_id': 1, 'crop_type': 'corn', 'state': 'growing', 'sow_date': datetime.now(), 'harvest_date': datetime.now(), 'storage_id': None, 'smallholding_id': None, 'quantity': 100})
    
    def test_eq(self):
        crop2 = Crop(crop_id=1, crop_type='corn', state='growing', quantity=100)
        crop3 = Crop(crop_id=2, crop_type='wheat', state='harvested', quantity=200)
        self.assertEqual(self.crop, crop2)
        self.assertNotEqual(self.crop, crop3)    


if __name__ == '__main__':
    unittest.main()