# Encoding: utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import transaction
import json
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
    response_data = {}

    if request.method == 'GET':
        try:
            obwod = Obwod.objects.get(id=oid)
            response_data['ok'] = obwod.otrzymanych_kart
            response_data['upr'] = obwod.uprawnionych
            response_data['status'] = "OK"
        except Obwod.DoesNotExist:
            response_data['status'] = "OBWOD_NOT_FOUND"
            # messages.error(request, "Obwod not found")

    elif request.method == 'POST':
        try:
            obwod = Obwod.objects.select_for_update().get(id=oid)
            ok_stare = int(request.POST['ok_stare'])
            ok = int(request.POST['ok'])
            upr_stare = int(request.POST['upr_stare'])
            upr = int(request.POST['upr'])

            if ok < 0 or upr < 0:
                response_data['status'] = "NEGATIVE_NUMBERS"
                # messages.error(request, "Nie można wprowadzać ujemnych liczb")
            elif ok_stare != obwod.otrzymanych_kart:
                response_data['status'] = "DATA_CHANGED"
                response_data['original'] = obwod.otrzymanych_kart
                response_data['new'] = ok
                # messages.error(request, "Dane zostały zmienione od ostatniego odczytu."
                #                        "Zapisujesz %d, a ktoś inny zapisał %d" % (ok, obwod.otrzymanych_kart))
            elif upr_stare != obwod.uprawnionych:
                response_data['status'] = "DATA_CHANGED"
                response_data['original'] = obwod.uprawnionych
                response_data['new'] = upr
                # messages.error(request, "Dane zostały zmienione od ostatniego odczytu."
                #                        "Zapisujesz %d, a ktoś inny zapisał %d" % (upr, obwod.uprawnionych))
            else:
                obwod.otrzymanych_kart = ok
                obwod.uprawnionych = upr
                obwod.save()
                # messages.success(request, "Dane zostały zapisane.")
                response_data['ok'] = obwod.otrzymanych_kart
                response_data['upr'] = obwod.uprawnionych
                response_data['status'] = "OK"

        except ValueError:
            response_data['status'] = "WRONG_DATA"
            # messages.error(request, "Błędne dane")
        except KeyError:
            response_data['status'] = "INCOMPLETE DATA"
            # messages.error(request, "Niekompletne dane")
        except Obwod.DoesNotExist:
            response_data['status'] = "OBWOD_NOT_FOUND"
            # messages.error(request, "Obwod not found")

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )