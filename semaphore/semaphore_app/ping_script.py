from datetime import datetime
import requests
import subprocess
from threading import Thread
import time
import os
from datetime import datetime
from ping_class import Ping


# get user id from environment variables
# test with fake user ID

'''
EXAMPLE INSTANCE API REQUEST RETURN

[{"id":7,"instance":"www.theverge.com","instance_provider":"Amazon Web Services","provider_service":"EBS","user":2},
{"id":6,"instance":"www.microsoft.com","instance_provider":"Amazon Web Services","provider_service":"EC2","user":2},
{"id":5,"instance":"www.mcdonalds.com","instance_provider":"Microsoft Azure","provider_service":"Azure VM","user":2},
{"id":4,"instance":"www.carls.com","instance_provider":"Google Cloud Platform","provider_service":"Machine Learning","user":2},
{"id":3,"instance":"www.djangodjango.com","instance_provider":"Google Cloud Platform","provider_service":"App Engine","user":2},
{"id":1,"instance":"www.apple.com","instance_provider":"Amazon Web Services","provider_service":"EC2","user":2}]
'''


def instances_check():
    # API CALL: GET instances for user
    instances_list = []
    raw_instances = requests.get("http://localhost:8000/api/v1/instances/", headers={"Authorization": "2"})
    instances = raw_instances.json()

    for instance in instances:
        instances_list.append(instance)

    return instances_list


def ping_hostname(u):
    print('starting thread')
    ping_result = check_ping(u)
    store_ping_result(ping_result)
    print('thread finished')
    #print("processed %s: %s" % (u, ping_result))

def check_ping(hostname):

    with open(os.devnull, 'w') as DEVNULL:
        #cmd = "fping {host} -C 3 -q".format(host=hostname)
        #res = [float(x) for x in get_simple_cmd_output(cmd).strip().split(':')[-1].split() if x != '-']
        #return res

        process = subprocess.Popen(['fping', hostname["instance"], '-C', '3', '-q'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).communicate()[0]
        return Ping.parse_ping(process, hostname)


def store_ping_result(ping_object):

    # pass instance id as parameter payload
    payload = {"id": ping_object.get_hostname(), "min_ping":ping_object.get_min(), "max_ping":ping_object.get_max(), "avg_ping": ping_object.get_avg()}
    requests.post("http://localhost:8000/api/v1/ping/{}".format(ping_object.get_hostname()), data=payload, headers={"Authorization": "2"})
    print("successfully saved: ", ping_object.get_hostname())
    return


def run_threads_please(hostnames):
    print('Prepping hostname pings...')

    for u in hostnames:
        t = Thread(target=ping_hostname, args = (u,))
        t.start()

if __name__ == '__main__':
    while True:
        instances = instances_check()
        run_threads_please(instances)
        hostnames = []
        time.sleep(60)
