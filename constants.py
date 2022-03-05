from os import getenv

URL = getenv("URL")
CURRENCY_CODES = ["USD", "EUR", "BRL", "GBP", "UYU", "CLP", "PYG"]
CURRENCIES = [
    "Dolar",
    "Euro",
    "Real",
    "Libra Esterlina",
    "Peso Uruguayo",
    "Peso Chileno",
    "Guaraní",
]
CURRENCY_NAMES = [
    "United States Dollar",
    "Euro",
    "Brazillian Real",
    "Pound",
    "Uruguayan Peso",
    "Chilean Peso",
    "Guarani",
]
OK_STATUS = 200
BAD_REQUEST_STATUS = 400
INTERNAL_SERVER_ERROR_STATUS = 500
SERVICE_UNAVAILABLE_STATUS = 503
INVALID_PARAMETERS = "Invalid parameters."
INTERNAL_SERVER_ERROR = "An internal server error ocurred."
SERVICE_UNAVAILABLE = "This service is not available, please try again in a few minutes."
