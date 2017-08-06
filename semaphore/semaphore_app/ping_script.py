from datetime import datetime
import requests
import subprocess
from threading import Thread
import time
import os
from datetime import datetime


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


class Ping:

    def __init__(self, hostname, minimum, maximum, average):
        self.hostname = hostname
        self.min = minimum
        self.max = maximum
        self.avg = average

    @classmethod
    def parse_ping(cls, whole_ping_string, hostname_object):
        cls.hostname, cls.ping = whole_ping_string.decode("utf-8").split(":")
        cls.ping = cls.ping.strip('\n').lstrip()
        if cls.ping.split(" ")[0] == '-':
            cls.min = 0
            cls.avg = 0
            cls.max = 0
        else:
            cls.min, cls.avg, cls.max = map(float,cls.ping.split())

        return Ping(hostname_object["id"], cls.min, cls.max, cls.avg)


    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def get_avg(self):
        return self.avg

    def get_hostname(self):
        return self.hostname

    def __str__(self):
        return "<hostname_id: %s, min: %s, max: %s, avg: %s>" %(self.hostname, self.min, self.max, self.avg)


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
    #store_ping_result(ping_result,u)
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


def store_ping_result(result,hostname_ping):

    # pass instance id as parameter payload
    requests.post("http://localhost:8000/api/v1/instances/", headers={"Authorization": "2"})
    pass


def run_threads_please(hostnames):
    print('Prepping hostname pings...')

    for u in hostnames:
        t = Thread(target=ping_hostname, args = (u,))
        t.start()

if __name__ == '__main__':
    while True:
        instances = instances_check()
        test = run_threads_please(instances)
        hostnames = []
        time.sleep(60)
