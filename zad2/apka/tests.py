from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from models import Obwod, Gmina


class SeleniumTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        g1 = Gmina(numer=1, nazwa="Gmina1")
        g1.save()
        g2 = Gmina(numer=2, nazwa="Gmina2")
        g2.save()
        Obwod.objects.create(gmina=g1, numer=40, adres="Obwod1")
        Obwod.objects.create(gmina=g1, numer=41, adres="Obwod2")
        Obwod.objects.create(gmina=g1, numer=42, adres="Obwod3")
        Obwod.objects.create(gmina=g2, numer=43, adres="Obwod4")
        Obwod.objects.create(gmina=g2, numer=44, adres="Obwod5")
        super(SeleniumTest, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTest, cls).tearDownClass()

    def test_edit(self):
        self.selenium.get('%s%s' % (self.live_server_url, 'apka/1/'))