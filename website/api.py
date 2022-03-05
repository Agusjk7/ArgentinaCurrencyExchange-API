import json
from time import strftime, strptime

import requests
import xmltodict
from constants import *
from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

"""
Ruta que retorna información de compra y venta de cierta divisa.
Las divisas posibles son: USD, EUR, BRL, GBP, UYU, CLP y PYG.

Parámetro:
    <string:code>
"""


@api.route("/currency")
def get_currency():
    try:
        # Obtener los valores de las divisas y verificar que la petición fue exitosa.
        r = requests.get(URL)
        if r.status_code != OK_STATUS:
            return (
                jsonify(
                    {"msg": SERVICE_UNAVAILABLE, "status": SERVICE_UNAVAILABLE_STATUS}
                ),
                SERVICE_UNAVAILABLE_STATUS,
            )

        # Obtener y verificar el parámetro de la petición y añadirlo a una variable.
        try:
            args = json.loads(json.dumps(request.args))
            code = args.get("code").upper()

            if code not in CURRENCY_CODES:
                raise Exception
        except:
            return (
                jsonify({"msg": INVALID_PARAMETERS, "status": BAD_REQUEST_STATUS}),
                BAD_REQUEST_STATUS,
            )

        # Obtener la información de las divisas.
        data = json.loads(json.dumps(xmltodict.parse(r.content)))["cotiza"]

        # Filtrar información de la divisa requerida y añadirla dentro de un objeto.
        currency = {}
        for i in data.get("cotizador"):
            if (
                data["cotizador"][i].get("nombre")
                == CURRENCIES[CURRENCY_CODES.index(code)]
            ):
                currency = data["cotizador"][i]
                break

        # Helper para cambiar el formato de la fecha y hora de latinoamericana a inglesa.
        date_and_time = data.get("ultima").get("zona37")
        date = strftime("%m/%d/%Y", strptime(date_and_time.get("fecha"), "%d/%m/%Y"))
        time = strftime("%I:%M %p", strptime(date_and_time.get("hora"), "%H:%M"))

        return (
            jsonify(
                {
                    "data": {
                        code: {
                            "buy": float(currency.get("compra").replace(",", ".")),
                            "name": CURRENCY_NAMES[CURRENCY_CODES.index(code)],
                            "sell": float(currency.get("venta").replace(",", ".")),
                        }
                    },
                    "update": {"date": date, "time": time, "time-zone": "UTC-3"},
                    "status": OK_STATUS,
                }
            ),
            OK_STATUS,
        )
    except:
        return (
            jsonify(
                {"msg": INTERNAL_SERVER_ERROR, "status": INTERNAL_SERVER_ERROR_STATUS}
            ),
            INTERNAL_SERVER_ERROR_STATUS,
        )


"""
Ruta que retorna información de compra y venta de todas las divisas.
"""


@api.route("/currencies")
def get_currencies():
    try:
        # Obtener los valores de las divisas y verificar que la petición fue exitosa.
        r = requests.get(URL)
        if r.status_code != OK_STATUS:
            return (
                jsonify(
                    {"msg": SERVICE_UNAVAILABLE, "status": SERVICE_UNAVAILABLE_STATUS}
                ),
                SERVICE_UNAVAILABLE_STATUS,
            )

        # Obtener la información de las divisas.
        data = json.loads(json.dumps(xmltodict.parse(r.content)))["cotiza"]

        # Filtrar la información de cada divisa y añadirla dentro de un objeto.
        currencies = {}
        for i in data.get("cotizador"):
            code = CURRENCIES.index(data["cotizador"][i].get("nombre"))

            currencies[CURRENCY_CODES[code]] = {
                "buy": float(data["cotizador"][i].get("compra").replace(",", ".")),
                "name": CURRENCY_NAMES[code],
                "sell": float(data["cotizador"][i].get("venta").replace(",", ".")),
            }

        # Helper para cambiar el formato de la fecha y hora de latinoamericana a inglesa.
        date_and_time = data.get("ultima").get("zona37")
        date = strftime("%m/%d/%Y", strptime(date_and_time.get("fecha"), "%d/%m/%Y"))
        time = strftime("%I:%M %p", strptime(date_and_time.get("hora"), "%H:%M"))

        return (
            jsonify(
                {
                    "data": currencies,
                    "update": {"date": date, "time": time, "time-zone": "GMT-3"},
                    "status": OK_STATUS,
                }
            ),
            OK_STATUS,
        )
    except:
        return (
            jsonify(
                {"msg": INTERNAL_SERVER_ERROR, "status": INTERNAL_SERVER_ERROR_STATUS}
            ),
            INTERNAL_SERVER_ERROR_STATUS,
        )


"""
Ruta que retorna información de compra, venta y variación de
todos los tipos de dólares que se manejan en Argentina.
"""


@api.route("/dollars")
def get_usd():
    try:
        # Obtener los valores de las divisas y verificar que la petición fue exitosa.
        r = requests.get(URL)
        if r.status_code != OK_STATUS:
            return (
                jsonify(
                    {"msg": SERVICE_UNAVAILABLE, "status": SERVICE_UNAVAILABLE_STATUS}
                ),
                SERVICE_UNAVAILABLE_STATUS,
            )

        # Obtener la información de los dólares.
        data = json.loads(json.dumps(xmltodict.parse(r.content))).get("cotiza")
        values = data.get("valores_principales")

        # Eliminar información innecesaria.
        del values["casa311"], values["casa399"]

        # Filtrar la información de cada dolar y añadirla dentro de un arreglo de objetos.
        dollars = {"USD": []}
        for i in values:
            compra = values[i].get("compra")
            dollars["USD"].append(
                {
                    "buy": float(compra.replace(",", "."))
                    if compra != "No Cotiza"
                    else 0.0,
                    "name": values[i].get("nombre").title(),
                    "sell": float(values[i].get("venta").replace(",", ".")),
                    "variation": values[i].get("variacion").replace(",", ".") + "%",
                }
            )

        # Helper para cambiar el formato de la fecha y hora de latinoamericana a inglesa.
        date_and_time = data.get("ultima").get("zona37")
        date = strftime("%m/%d/%Y", strptime(date_and_time.get("fecha"), "%d/%m/%Y"))
        time = strftime("%I:%M %p", strptime(date_and_time.get("hora"), "%H:%M"))

        return (
            jsonify(
                {
                    "data": dollars,
                    "update": {"date": date, "time": time, "time-zone": "GMT-3"},
                    "status": OK_STATUS,
                }
            ),
            OK_STATUS,
        )
    except:
        return (
            jsonify(
                {"msg": INTERNAL_SERVER_ERROR, "status": INTERNAL_SERVER_ERROR_STATUS}
            ),
            INTERNAL_SERVER_ERROR_STATUS,
        )
