import unittest

from app import app


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.debug = True
        app.testing = True
        cls.client = app.test_client()

    def test_get_all_min(self):
        response = self.client.get('/min')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Группа товара': 'Блоки питания',
                                         'Дата продажи': 'Tue, 01 Jan 2019 00:00:00 GMT',
                                         'Количество товара': 1,
                                         'Наименование товара': 'GTX 1660',
                                         'Стоимость товара': 6000})

    def test_get_min(self):
        response = self.client.get('/min?columns=Дата+продажи,Количество+товара')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Дата продажи': 'Tue, 01 Jan 2019 00:00:00 GMT', 'Количество товара': 1})

    def test_get_all_max(self):
        response = self.client.get('/max')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Группа товара': 'Процессоры',
                                         'Дата продажи': 'Thu, 03 Jan 2019 00:00:00 GMT',
                                         'Количество товара': 2,
                                         'Наименование товара': 'Seasonic D600',
                                         'Стоимость товара': 60000})

    def test_get_max(self):
        response = self.client.get('/max?columns=Дата+продажи,Количество+товара')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Дата продажи': 'Thu, 03 Jan 2019 00:00:00 GMT', 'Количество товара': 2})


if __name__ == '__main__':
    unittest.main()
