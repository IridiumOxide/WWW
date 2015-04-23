from django.db import models


class Obwod(models.Model):
    gmina = models.ForeignKey('Gmina')
    numer = models.IntegerField()
    adres = models.CharField(max_length=128)
    otrzymanych_kart = models.IntegerField(default=0)
    uprawnionych = models.IntegerField(default=0)

    def __unicode__(self):
        return u"%s" % self.adres


class Gmina(models.Model):
    numer = models.IntegerField()
    nazwa = models.CharField(max_length=128)

    def __unicode__(self):
        return u"%s" % self.nazwa