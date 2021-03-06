from datetime import datetime
import json

from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.six import BytesIO

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient


from toys.models import Toy
from toys.serializers import ToySerializer


class ToyTest(TestCase):
    def setUp(self):
        self.toy_release_date = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
        self.toy1 = Toy(
            name='Snoopy talking action figure',
            description='Snoopy speaks five languages',
            release_date=self.toy_release_date,
            toy_category='Action figures',
            was_included_in_home=True
        )
        self.toy1.save()

        self.toy2_release_date = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
        self.toy2 = Toy(
            name='Hawaiian Barbie',
            description='Barbie loves Hawaii',
            release_date=self.toy2_release_date,
            toy_category='Doll',
            was_included_in_home=True
        )
        self.toy2.save()

        self.serializer_for_toy1 = ToySerializer(self.toy1)
        self.serializer_for_toy2 = ToySerializer(self.toy2)

        self.json_string_for_new_toy = '{"name":"Clash Royale play set",' \
                                        '"description":"6 figures from Clash Royale", ' \
                                        '"release_date":"2017-10-09T12:10:00.776594Z",' \
                                        '"toy_category":"Playset","was_included_in_home":false}'

        # set client API
        self.client = APIClient()

        # initiation data for post
        self.data_post = [
            {
                "name": "Skater ska",
                "description": "Hero skater",
                "release_date": self.toy1.release_date.isoformat(),
                "toy_category": "Action figures",
                "was_included_in_home": False
            },
            {
                "name": "PvZ 2 puzzle",
                "description": "Plants vs Zombies 2 puzzle",
                "toy_category": "Puzzle",
                "was_included_in_home": False,
                "release_date": self.toy1.release_date.isoformat()
            },
        ]

        self.data_toy1_candidate = {
            "description": "Plants vs Zombies 3 puzzle",
            "name": "PvZ 3 puzzle",
            "pk": 1,
            "release_date": self.toy1.release_date.isoformat(),
            "toy_category": "Puzzles & Games",
            "was_included_in_home": False
        }

    def test_create_toy(self):
        self.assertEqual(self.toy1.pk, 1)
        self.assertEqual(self.toy1.name, 'Snoopy talking action figure')
        self.assertTrue(self.toy1.was_included_in_home, )
        self.assertEqual(self.toy2.pk, 2)
        self.assertEqual(self.toy2.name, 'Hawaiian Barbie')
        self.assertTrue(self.toy2.was_included_in_home)

    def test_serializer(self):
        self.assertDictEqual(
            {
                'pk': 1,
                'name': 'Snoopy talking action figure',
                'description': 'Snoopy speaks five languages',
                'release_date': self.toy1.release_date.isoformat(),
                'toy_category': 'Action figures',
                'was_included_in_home': True
            },
            self.serializer_for_toy1.data,
            'ok'
        )

        self.assertDictEqual(
            {
                'pk': 2,
                'name': 'Hawaiian Barbie',
                'description': 'Barbie loves Hawaii',
                'release_date': self.toy2.release_date.isoformat(),
                'toy_category': 'Doll',
                'was_included_in_home': True
            },
            self.serializer_for_toy2.data,
            'ok'
        )

    def test_json(self):
        json_renderer = JSONRenderer()
        toy1_rendered_into_json = json_renderer.render(self.serializer_for_toy1.data)
        toy2_rendered_into_json = json_renderer.render(self.serializer_for_toy2.data)

        data_toy1 = {
            "pk": 1, "name": "Snoopy talking action figure",
            "description": "Snoopy speaks five languages",
            "release_date": self.toy1.release_date.isoformat(),
            "toy_category": "Action figures",
            "was_included_in_home": True
        }

        data_toy2 = {
            "pk": 2,
            "name": "Hawaiian Barbie",
            "description": "Barbie loves Hawaii",
            "release_date": self.toy2.release_date.isoformat(),
            "toy_category": "Doll",
            "was_included_in_home": True
        }

        self.assertJSONEqual(
            json.dumps(data_toy1),
            json.loads(toy1_rendered_into_json)
        )
        self.assertJSONEqual(
            json.dumps(data_toy2),
            json.loads(toy2_rendered_into_json)
        )

    def test_json_parse(self):
        json_bytes_for_new_toy = bytes(self.json_string_for_new_toy, encoding="UTF-8")
        stream_for_new_toy = BytesIO(json_bytes_for_new_toy)
        parser = JSONParser()
        parsed_new_toy = parser.parse(stream_for_new_toy)
        self.assertDictEqual(
            parsed_new_toy,
            json.loads(self.json_string_for_new_toy)
        )

    def test_create_from_json(self):
        json_bytes_for_new_toy = bytes(self.json_string_for_new_toy, encoding="UTF-8")
        stream_for_new_toy = BytesIO(json_bytes_for_new_toy)
        parser = JSONParser()
        parsed_new_toy = parser.parse(stream_for_new_toy)
        new_toy_serializer = ToySerializer(data=parsed_new_toy)
        if new_toy_serializer.is_valid():
            toy3 = new_toy_serializer.save()
            self.assertEqual(toy3.name, 'Clash Royale play set')

    def test_rest_post_get(self):
        for item_data in self.data_post:
            self.client.post(
                reverse_lazy('toys:home'),
                data=json.dumps(item_data),
                content_type='application/json',
            )

        self.assertEqual(
            len(self.client.get(reverse_lazy('toys:home')).json()),
            4
        )

        self.assertEqual(
            self.client.get(reverse_lazy('toys:detail', kwargs={'pk': 3})).json()['name'],
            "Skater ska"
        )

        self.assertEqual(
            self.client.get(reverse_lazy('toys:detail', kwargs={'pk': 4})).json()['name'],
            "PvZ 2 puzzle"
        )

        # debug gwt json
        # print(client.get('/toys/').json())

    def test_rest_put(self):
        self.client.get(reverse_lazy('toys:detail', kwargs={'pk': 1})).json()

        self.client.put(reverse_lazy('toys:detail', kwargs={'pk': 1}), data=json.dumps(self.data_toy1_candidate),
                        content_type='application/json')
        self.assertEqual(
            self.client.get(reverse_lazy('toys:detail', kwargs={'pk': 1})).json()['name'],
            'PvZ 3 puzzle'
        )

    def test_rest_delete(self):
        self.client.delete(reverse_lazy('toys:detail', kwargs={'pk': 2}))
        try:
            self.client.get(reverse_lazy('toys:detail', kwargs={'pk': 2})).json()
            raise AssertionError
        except TypeError:
            pass

    def test_cbv_post_get(self):
        """
        test post and get
        with class based view
        :return:
        """
        data_get = self.client.get(reverse_lazy('toys:cbv_home')).json()
        self.assertEqual(len(data_get), 2, "GET class based FAILED")

        for item in self.data_post:
            self.client.post(
                reverse_lazy('toys:cbv_home'),
                data=json.dumps(item),
                content_type='application/json',
            )

        data_get = self.client.get(reverse_lazy('toys:cbv_home')).json()
        self.assertEqual(len(data_get), 4, "POST class based FAILED")

    def test_cbv_put_delete(self):
        self.client.put(
            reverse_lazy('toys:cbv_detail', kwargs={'pk': 1}),
            data=json.dumps(self.data_toy1_candidate),
            content_type='application/json'
        )

        self.assertEqual(
            self.client.get(reverse_lazy('toys:cbv_detail', kwargs={'pk': 1})).json()['name'],
            'PvZ 3 puzzle'
        )

        self.client.delete(reverse_lazy('toys:cbv_detail', kwargs={'pk': 1}))
        self.assertEqual(
            self.client.get(reverse_lazy('toys:cbv_detail', kwargs={'pk': 1})).status_code,
            404
        )
        self.assertEqual(
            self.client.get(reverse_lazy('toys:cbv_detail', kwargs={'pk': 1})).json()['detail'],
            'Not found.'
        )

    def test_mixin_post_get(self):
        data_get = self.client.get(reverse_lazy('toys:cbv_mixin_home'))
        self.assertEqual(len(data_get.json()), 4, 'Failed get data class based mixin')

        for item in self.data_post:
            self.client.post(
                reverse_lazy('toys:cbv_mixin_home'),
                data=json.dumps(item),
                content_type='application/json',
            )

        data_get = self.client.get(reverse_lazy('toys:cbv_mixin_home'))
        self.assertEqual(len(data_get.json()), 4, 'Failed POST data class based mixin')

    def test_mixin_put_delete(self):
        self.client.put(
            reverse_lazy('toys:cbv_mixin_detail', kwargs={'pk': 1}),
            data=json.dumps(self.data_toy1_candidate),
            content_type='application/json'
        )

        self.assertEqual(
            self.client.get(reverse_lazy('toys:cbv_mixin_detail', kwargs={'pk': 1})).json()['name'],
            'PvZ 3 puzzle'
        )

        self.client.delete(reverse_lazy('toys:cbv_mixin_detail', kwargs={'pk': 1}))
        self.assertEqual(
            self.client.get(reverse_lazy('toys:detail', kwargs={'pk': 1})).status_code,
            404
        )
        self.assertEqual(
            self.client.get(reverse_lazy('toys:cbv_mixin_detail', kwargs={'pk': 1})).json()['detail'],
            'Not found.'
        )

    def test_generic_post_get(self):
        data_get = self.client.get(reverse_lazy('toys:cbv_generic_home'))
        self.assertEqual(len(data_get.json()), 4, 'Failed get data GENERIC class based mixin')

        for item in self.data_post:
            self.client.post(
                reverse_lazy('toys:cbv_generic_home'),
                data=json.dumps(item),
                content_type='application/json',
            )

        data_get = self.client.get(reverse_lazy('toys:cbv_generic_home'))
        self.assertEqual(len(data_get.json()), 4, 'Failed POST data GENERIC class based mixin')

    def test_generic_put_delete(self):
        self.client.put(
            reverse_lazy('toys:cbv_generic_detail', kwargs={'pk': 1}),
            data=json.dumps(self.data_toy1_candidate),
            content_type='application/json'
        )

        self.assertEqual(
            self.client.get(reverse_lazy('toys:cbv_generic_detail', kwargs={'pk': 1})).json()['name'],
            'PvZ 3 puzzle'
        )

        self.client.delete(reverse_lazy('toys:cbv_generic_detail', kwargs={'pk': 1}))
        self.assertEqual(
            self.client.get(reverse_lazy('toys:detail', kwargs={'pk': 1})).status_code,
            404,
            'Failed delete data.'
        )
        self.assertEqual(
            self.client.get(reverse_lazy('toys:cbv_generic_detail', kwargs={'pk': 1})).json()['detail'],
            'Not found.'
        )
