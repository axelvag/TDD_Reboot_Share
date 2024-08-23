import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from ft_return_api import create_file_API
from ft_create_taux_de_dispo import create_taux_de_dispo_csv, create_line_csv
from ft_reset_borne import find_evse_uid

# INFO sur cette API
# https://platform.greenflux.com/api/1.0/remotecommands/RESET
# il faut les param evse_uid et type
# je les passent soit par params soit direct dans l'url

# Supprime le msg warning du terminal
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
YOUR_API_KEY = os.getenv('YOUR_API_KEY')

if __name__ == '__main__':
    # print(YOUR_API_KEY)

    url = "https://platform.greenflux.com/api/1.0/ChargeStations"

    headers = {
        "accept": "application/json",
        "Authorization": YOUR_API_KEY
        }

    # Define date_from and date_to
    date_to = datetime.utcnow()
    date_from = date_to - timedelta(hours=72)
    
    params = {
        "date_from": date_from.isoformat() + "Z",  # heure actuel -72h
        "date_to": date_to.isoformat() + "Z" # heure actuel
    }
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        # print(response.text)
        
        create_file_API(response.text)  # creer le fichier brut dans /resultat
        
        # create_line_csv(response.text)  # cree le fichier charge_station.csv

        find_evse_uid(response.text)
    
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
