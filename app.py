#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bottle import Bottle, request, run, template
import math

app = Bottle()

def mm1_queue(arrival_rate, service_rate):
    ar = float(arrival_rate)
    sr = float(service_rate)
    
    
    Lq = (ar ** 2) / (sr * (sr - ar))
    Ls = Lq + (ar / sr)
    Wq = Lq / ar
    Ws = Wq + (1 / sr)
    
    return (
        
        '<br> M/M/1 Model: <br>' +
        'Average number of customers in the queue (Lq): ' + str(Lq) + '<br>' +
        'Average number of customers in the system (Ls): ' + str(Ls) + '<br>' +
        'Average time a customer spends waiting in the queue (Wq) in mins: ' + str(Wq * 60) + '<br>' +
        'Average time a customer spends in the system (Ws) in mins: ' + str(Ws * 60) 
        
    )

def mmc_queue(arrival_rate, service_rate, num_servers):
    ar = float(arrival_rate)
    sr = float(service_rate)
    ser = float(num_servers)

    P0 = 1 / (sum([(ar / sr) ** k / math.factorial(k) for k in range(int(ser) + 1)]) + ((ar / sr) ** ser * math.factorial(int(ser))) / (math.factorial(int(ser)) * (ser * sr - ar)))

    Lq = ((ar * sr) * ((ar / sr) ** ser)) / (math.gamma(ser) * ((ser * sr - ar) ** 2)) * P0
    Ls = Lq + (ar / sr)
    Wq = Lq / ar
    Ws = Wq + (1 / sr)

    return (
        
        '<br>M/M/C Model:<br>' +
        'Average number of customers in the queue (Lq): ' + str(Lq) + '<br>' +
        'Average number of customers in the system (Ls): ' + str(Ls) + '<br>' +
        'Average time a customer spends waiting in the queue (Wq) in mins: ' + str(Wq * 60) + '<br>' +
        'Average time a customer spends in the system (Ws) in mins: ' + str(Ws * 60)
    )

@app.route('/')
def index():
    return template('index.html')

@app.route('/', method='POST')
def process_form():
    num_servers = int(request.forms.get('num_servers'))
    arrival_rate = float(request.forms.get('arrival_rate'))
    service_rate = float(request.forms.get('service_rate'))

    # Call your mm1_queue or mmc_queue function based on num_servers
    if num_servers == 1:
        result = mm1_queue(arrival_rate, service_rate)
    else:
        result = mmc_queue(arrival_rate, service_rate, num_servers)

    return result

if __name__ == '__main__':
    run(app, host='192.168.129.186', port=8080)

