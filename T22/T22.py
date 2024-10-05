import requests
import json
import logging
import getpass
import argparse
import six
import sys

# 1. Verificación de la versión de Python con six
if not six.PY3:
    raise Exception("Este script requiere Python 3 para ejecutarse.")

# 2. Solicitar la API Key de manera segura con getpass
key = getpass.getpass("Ingrese su API Key de Have I Been Pwned: ")

# Encabezados para la solicitud
headers = {
    'content-type': 'application/json',
    'api-version': '3',
    'User-Agent': 'python',
    'hibp-api-key': key
}

# 3. Manejo de parámetros con argparse
parser = argparse.ArgumentParser(description='Consultar Have I Been Pwned por un correo electrónico')
parser.add_argument('email', type=str, help='Correo electrónico a investigar')
args = parser.parse_args()

email = args.email

# URL de la API
url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false'

# 4. Solicitud a la API
r = requests.get(url, headers=headers)

# 5. Manejo de errores y generación de reporte
if r.status_code == 200:
    data = r.json()
    encontrados = len(data)
    if encontrados > 0:
        print(f"Los sitios en los que se ha filtrado el correo {email} son:")
        for filtracion in data:
            print(filtracion["Name"])
    else:
        print(f"El correo {email} no ha sido filtrado.")
    
    msg = f"{email} - Filtraciones encontradas: {encontrados}"
    print(msg)

    # Configuración del logging
    logging.basicConfig(filename='hibpINFO.log',
                        format="%(asctime)s %(message)s",
                        datefmt="%m/%d/%Y %I:%M:%S %p",
                        level=logging.INFO)
    logging.info(msg)

else:
    # Mostrar mensaje de error si ocurre un fallo
    msg = r.text
    print(f"Error: {msg}")

    # Configuración del logging para errores
    logging.basicConfig(filename='hibpERROR.log',
                        format="%(asctime)s %(message)s",
                        datefmt="%m/%d/%Y %H:%M:%S",
                        level=logging.ERROR)
    logging.error(msg)
