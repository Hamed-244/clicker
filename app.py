import time
import json
import requests
import threading
import datetime
from datetime import timezone
from flask import Flask
import logging
import random

correct_requests = 0
wrong_requests = 0
lock = threading.Lock()
list_of_operations = []

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

with open('data.json', 'r') as f:
    data = json.load(f)


def calculate_request_body(data):
    body = {}
    # saved data
    last_request_time = data.get('lastRequestTime', 1717771516)
    last_max_taps = data.get('MaxTaps', 5500)
    last_taps_recover_per_sec = data.get('tapsRecoverPerSec', 10)
    last_earn_per_tap = data.get('earnPerTap', 10)
    last_available_taps = data.get('availableTaps', last_max_taps)
    
    # calculate request time
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    body['timestamp'] = utc_timestamp
    
    # calculate available taps
    time_difference = utc_timestamp - last_request_time
    money_saved = last_available_taps + (time_difference * last_taps_recover_per_sec)
    available_taps = money_saved if money_saved < last_max_taps else last_max_taps
    body['availableTaps'] = available_taps
    
    # calculate count of taps
    count = available_taps // last_earn_per_tap
    body['count'] = count
    
    return body


def bot(index):
    global correct_requests, wrong_requests
    
    while True:
        body = calculate_request_body(data[index])
        api_key = data[index].get('key',None)
        last_taps_recover_per_sec = data[index].get('tapsRecoverPerSec', 10)
        last_max_taps = data[index].get('MaxTaps', 5500)
        last_earn_per_tap = data[index].get('earnPerTap', 10)
        last_available_taps = data.get('availableTaps', last_max_taps)
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post('https://api.hamsterkombat.io/clicker/tap', data=json.dumps(body), headers=headers)
        result = response.ok
        
        taps_clickeable = body.get('availableTaps')
        taps_clicke_count = body.get('count')
        operation_text = f'{index} : available tabs :{taps_clickeable} , clicked count : {taps_clicke_count} , time : {datetime.datetime.now()} , status : {response.status_code}'
        list_of_operations.append(operation_text)
        
        with lock:
            if result:
                correct_requests += 1
                response_result = json.loads(response.content.decode('utf-8')) 
                response_data = response_result.get('clickerUser')
                
                # Update new data
                updated_last_request_time = body.get('timestamp')
                updated_taps_recover_per_sec = response_data.get('tapsRecoverPerSec' , last_taps_recover_per_sec)
                updated_max_taps = response_data.get('MaxTaps' , last_max_taps)
                updated_earn_per_tap = response_data.get('earnPerTap' , last_earn_per_tap)
                updated_available_taps = response_data.get('availableTaps' , last_available_taps)
                
                data[index]['lastRequestTime'] = updated_last_request_time
                data[index]['tapsRecoverPerSec'] = updated_taps_recover_per_sec
                data[index]['MaxTaps'] = updated_max_taps
                data[index]['earnPerTap'] = updated_earn_per_tap
                data[index]['availableTaps'] = updated_available_taps
                
                # Save updated data to data.json
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                wrong_requests += 1
                logging.info(f'Wrong request with {index} account ; status code {response.status_code}!')
                if response.status_code == 401 :
                    break
        sleep_time = random.randint(1800,10600)
        time.sleep(sleep_time)

for item in data:
    threading.Thread(target=bot, args=(item,)).start()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return f"""
        <h2 style='font-family: cursive;text-align: center'>Hello, this is the count of correct requests I did: {correct_requests}!</h2>
        </br>
        <h3 style='font-family: cursive;text-align: center'>And this is wrong requests: {wrong_requests}</h3>
        """

@app.route('/status')
def status():
    result = ''
    for item in list_of_operations:
        result +='<p>'+ item +'</p>' + '</br>'
    return '<div style="font-family: cursive;">' + result + '</div>'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8000)