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
