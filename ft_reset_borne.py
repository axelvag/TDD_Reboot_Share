import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
YOUR_API_KEY = os.getenv('YOUR_API_KEY')

# extrait les evse_uid de chaque ligne de l'extract response_text
# ils sont sous la forme: # evses":[{"uid":"FR-VIA-ETEST-DBT-LYON-1"
def find_evse_uid(response_text):
	# Split par le mot charge_station_id
    text = response_text.split('charge_station_id')
    
    # tab a mettre en csv
    tab = []

    for line_brut in text:
        if line_brut.strip():  # si elle est pas vide
            # trouve le premier : pour recuperer evse_uid
            start_index = line_brut.find('evses":[{"uid":"') + 16
            # trouve la fin du char_station_id
            end_index = line_brut.find('"', start_index)
            if start_index != -1 and end_index != -1:
                if 'AVAILABLE' not in line_brut and 'CHARGING' not in line_brut and 'Stock' not in line_brut:
                    # 1. evse_uid
                    evse_uid = line_brut[start_index:end_index]
                    print(f'{evse_uid}\n')
                    call_API_reset(evse_uid)

                    # tab.append(evse_uid)
                    # print(tab)

	# call_API_reset(FR-VIA-ETest-DBT-Lyon-2-1)

def call_API_reset(evse_uid):
	url = "https://platform.greenflux.com/api/1.0/remotecommands/RESET"

	params = json.dumps({
	"evse_uid": evse_uid,
	"type": "Hard"
	})
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': YOUR_API_KEY,
	}

	response = requests.request("POST", url, headers=headers, data=params, verify=False)
	print(response.text)

# if __name__ == '__main__':
#     call_API_reset("FR-VIA-E1000145322-1")