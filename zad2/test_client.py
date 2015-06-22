from django.test import Client
from django.test import TestCase
from apka.models import Obwod, Gmina


class SimpleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Gmina.objects.create(numer="1", nazwa="Gmina1")
        Gmina.objects.create(numer="2", nazwa="Gmina1")
        g3 = Gmina(numer="3", nazwa="Gmina1")
        g3.save()
        Obwod.objects.create(gmina=g3, numer="40", adres="Obwod0")
        Obwod.objects.create(gmina=g3, numer="41", adres="Obwod1")
        Obwod.objects.create(gmina=g3, numer="42", adres="Obwod2")

    def test_gminas_list(self):
        response = self.client.get('/apka/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['gminas']), 3)

    def test_gminas_menu(self):
        response = self.client.get('/apka/3/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['obwody']), 3)

    def test_gminas_empty(self):
        response = self.client.get('/apka/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['obwody']), 0)