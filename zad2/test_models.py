from django.test import TestCase
from apka.models import Gmina, Obwod


class ModelsTestCase(TestCase):
    def setUp(self):
        g1 = Gmina(numer=1, nazwa="Gmina1")
        g2 = Gmina(numer=2, nazwa="Gmina2")
        g1.save()
        g2.save()
        Obwod.objects.create(gmina=g1, numer=42, adres="Obwod42")
        Obwod.objects.create(gmina=g1, numer=41, adres="Obwod41")
        Obwod.objects.create(gmina=g2, numer=40, adres="Obwod40")

    def test_amount(self):
        self.assertEqual(Obwod.objects.count(), 3)
        self.assertEqual(Gmina.objects.count(), 2)

    def test_names(self):
        g1 = Gmina.objects.get(numer=1)
        o1 = Obwod.objects.get(numer=41)
        self.assertEqual(g1.nazwa, "Gmina1")
        self.assertEqual(o1.adres, "Obwod41")

    def test_defaults(self):
        o1 = Obwod.objects.get(numer=40)
        self.assertEqual(o1.uprawnionych, 0)
        self.assertEqual(o1.otrzymanych_kart, 0)

    def test_change_values(self):
        o2 = Obwod.objects.get(numer=41)
        self.assertEqual(o2.uprawnionych, 0)
        self.assertEqual(o2.otrzymanych_kart, 0)
        o2.uprawnionych = 1337
        o2.otrzymanych_kart = 42
        o2.save()
        self.assertEqual(o2.uprawnionych, 1337)
        self.assertEqual(o2.otrzymanych_kart, 42)