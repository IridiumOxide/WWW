# -*- coding: utf-8 -*-

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

    def test_overwrite(self):
        driver2 = WebDriver()
        self.selenium.get('%s%s' % (self.live_server_url, '/apka/1/'))
        self.selenium.implicitly_wait(100)
        edit_button1 = self.selenium.find_element_by_id('editButton1')
        save_button1 = self.selenium.find_element_by_id('submitButton1')
        edit_button1.click()

        driver2.get('%s%s' % (self.live_server_url, '/apka/1/'))
        driver2.implicitly_wait(100)
        edit_button2 = driver2.find_element_by_id('editButton1')
        save_button2 = driver2.find_element_by_id('submitButton1')
        edit_button2.click()
        driver2.implicitly_wait(100)
        inputok = driver2.find_element_by_name('ok')
        inputok.clear()
        inputok.send_keys('0')
        inputupr = driver2.find_element_by_name('upr')
        inputupr.clear()
        inputupr.send_keys('1')
        save_button2.click()
        alert = driver2.switch_to.alert
        self.assertEqual(alert.text, "Zapisano dane")
        alert.accept()
        obwod = Obwod.objects.get(id=1)
        self.assertEqual(obwod.otrzymanych_kart, 0)
        self.assertEqual(obwod.uprawnionych, 1)
        driver2.quit()

        self.selenium.implicitly_wait(100)
        inputok = self.selenium.find_element_by_name('ok')
        inputok.clear()
        inputok.send_keys('42')
        inputupr = self.selenium.find_element_by_name('upr')
        inputupr.clear()
        inputupr.send_keys('1337')
        save_button1.click()
        alert = self.selenium.switch_to.alert
        self.assertEqual(alert.text, u"Dane zmieniły się od ostatniego zapisu. Zapisujesz 1337, a ktoś inny zapisał 1")
        alert.accept()
        obwod = Obwod.objects.get(id=1)
        self.assertEqual(obwod.otrzymanych_kart, 0)
        self.assertEqual(obwod.uprawnionych, 1)