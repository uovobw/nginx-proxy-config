class ProxyMapping(object):
    servername = "www.site.com"
    serverport = 22
    serverssl = False
    servercertificate = "---BEGIN ..."
    serverkey = "---BEGIN..."
    remotehost = "1.2.3.4"
    remoteport= 80

    def __repr__(self):
        return "MAP %s -> %s:%s" % (self.servername, self.remotehost, self.remoteport)

    def tostr(self):
        return "%s:%s:%s" % (self.servername, self.remotehost, self.remoteport)

class ProxyHost(object):
    displayname = "UK"
    port = 22
    group = "no-group"
    address = "some.host.com"
    assigned_mapping = []

    def __repr__(self):
        return "HOST %s (%s) mappings: %i" % (self.displayname, self.address, len(self.assigned_mapping))

