import json
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse_lazy


class DronesTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_categories_post_get(self):
        category_names = ('Quadcopter X1', 'Quadcopter X2', 'Quadcopter X3')
        # reverse_lazy('drone:dronecategory-list')
        for name in category_names:
            self.client.post('/drones/drone-categories/', {'name': name})

        # check data if submitted
        data_post = self.client.get('/drones/drone-categories/')
        results = data_post.json()['results']
        for idx, name in enumerate(category_names):
            self.assertEqual(results[idx]['name'], name, 'Failed post')

        for idx, name in enumerate(category_names):
            data_get = self.client.get('/drones/drone-categories/{}/'.format(idx+1))
            # print(data_get.json()['name'])
            self.assertEqual(name, data_get.json()['name'])
