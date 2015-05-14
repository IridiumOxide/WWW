# Encoding: utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import transaction
from django.core.urlresolvers import reverse
from models import Gmina, Obwod


def index(request):
    gminas = Gmina.objects.all()
    context = {'gminas': gminas}
    return render(request, 'apka/index.html', context)


def gmina_menu(request, gmina_numer):
    gid = int(gmina_numer)
    gmina = get_object_or_404(Gmina, numer=gid)
    obwody = Obwod.objects.filter(gmina=gmina)
    context = {'gmina': gmina, 'obwody': obwody}
    return render(request, 'apka/gmina_menu.html', context)


@transaction.atomic
def obwod(request, obwod_numer):
    oid = int(obwod_numer)

    obwod = None

    try:
        obwod = Obwod.objects.select_for_update().get(id=oid)
        ok_stare = int(request.POST['ok_stare'])
        ok = int(request.POST['ok'])
        upr_stare = int(request.POST['upr_stare'])
        upr = int(request.POST['upr'])

        if ok < 0 or upr < 0:
            messages.error(request, "Nie można wprowadzać ujemnych liczb")
        elif ok_stare != obwod.otrzymanych_kart:
            messages.error(request, "Dane zostały zmienione od ostatniego odczytu."
                                    "Zapisujesz %d, a ktoś inny zapisał %d" % (ok, obwod.otrzymanych_kart))
        elif upr_stare != obwod.uprawnionych:
            messages.error(request, "Dane zostały zmienione od ostatniego odczytu."
                                    "Zapisujesz %d, a ktoś inny zapisał %d" % (upr, obwod.uprawnionych))
        else:
            obwod.otrzymanych_kart = ok
            obwod.uprawnionych = upr
            obwod.save()
            messages.success(request, "Dane zostały zapisane.")

    except ValueError:
        messages.error(request, "Błędne dane")
    except KeyError:
        messages.error(request, "Niekompletne dane")
    except Obwod.DoesNotExist:
        messages.error(request, "Obwod not found")

    return HttpResponseRedirect(reverse('gmina_menu', args=(obwod.gmina.numer,)))