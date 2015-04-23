# Encoding: utf-8
import requests
import re
from bs4 import BeautifulSoup
from apka.models import Gmina, Obwod

__author__ = 'fc346868'
linkWarszawa = '146501.htm'


def get_locations(link):
        page = requests.get("http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/" + link)
        p_text = page.content.decode('utf-8')
        p_text_soup = BeautifulSoup(p_text)
        return p_text_soup.select("#s0 tbody a")


def is_gmina(link):
    """ Gminy rozpoznajemy po linku. Trzeba zaifować miasto Warszawę, bo ma dzielnice"""
    return re.match(r'[0-9]{6}.htm', link) and (not (re.match(r'[0-9]{4}(00).htm', link) or link == linkWarszawa))


def get_poll_data(link):
    for potential_gmina in get_locations(link):
        pg_link = potential_gmina.attrs['href']
        if is_gmina(pg_link):
            g = Gmina(numer=int(pg_link[0:6]), nazwa=potential_gmina.string)
            g.save()
            print "Adding Gmina: \"", pg_link, "\" containing komisjas:"
            for komisja in get_locations(pg_link):
                print "   - ", komisja.string
                i = int(re.match(r'(.*[0-9]{6}_)([0-9]+)(.html)', komisja.attrs['href']).group(2))
                o = Obwod(gmina=g, numer=i, adres=komisja.string)
                o.save()
        else:
            get_poll_data(pg_link)


get_poll_data("index.htm")

print "gmin: ", len(Gmina.objects.all())
print "komisji: ", len(Obwod.objects.all())