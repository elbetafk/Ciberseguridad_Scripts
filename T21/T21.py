import requests
import json
import logging
import getpass

# Solicitar API Key
#key : ec1e2ebed1754f1b8c00f2b90aa15906
key = getpass.getpass("Introduce el API Key de Have I Been Pwned: ")

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'python',
    'hibp-api-key': key,
    'api-version': '3'
}

email = input("Ingrese el correo a investigar: ")

url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false'

try:
    r = requests.get(url, headers=headers)

    # Verificar si la respuesta fue exitosa
    if r.status_code == 200:
        data = r.json()
        encontrados = len(data)

        if encontrados > 0:
            print(f"Los sitios en los que se ha filtrado el correo {email} son:")
            for filtracion in data:
                print(filtracion['Name'], filtracion['Domain'], filtracion['BreachDate'], filtracion['Description'])

            # Guardar la informacion en un archivo log
            msg = f"Filtraciones encontradas: {str(encontrados)}"
            logging.basicConfig(filename='hibpINFO.log', 
                                format="%(asctime)s %(message)s", 
                                datefmt="%m/%d/%Y %I:%M:%S %p", 
                                level=logging.INFO)
            logging.info(msg)
        else:
            print(f"El correo {email} no ha sido filtrado.")
            logging.basicConfig(filename='hibpINFO.log', 
                                format="%(asctime)s %(message)s", 
                                datefmt="%m/%d/%Y %I:%M:%S %p", 
                                level=logging.INFO)
            logging.info(f"No se encontraron filtraciones para {email}.")

    else:
        msg = r.text
        logging.basicConfig(filename='hibpERROR.log', 
                            format="%(asctime)s %(message)s", 
                            datefmt="%m/%d/%Y %I:%M:%S %p", 
                            level=logging.ERROR)
        logging.error(msg)
        print(f"Error en la solicitud: {msg}")

except Exception as e:
    # Manejo de cualquier otro tipo de excepción
    msg = f"Error al hacer la solicitud: {str(e)}"
    logging.basicConfig(filename='hibpERROR.log', 
                        format="%(asctime)s %(message)s", 
                        datefmt="%m/%d/%Y %I:%M:%S %p", 
                        level=logging.ERROR)
    logging.error(msg)
    print(f"Se produjo un error: {msg}")
