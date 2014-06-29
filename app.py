from flask import Flask, render_template, request
from models import ProxyMapping, ProxyHost
import pickle
import os
import re
import StringIO
from RemoteExecutor import RemoteExecutor
from NginxProxy import NginxProxy

app = Flask(__name__)
app.config.from_envvar("AT_CONFIG")
app.debug=app.config["DEBUG"]

hosts = {}
mappings = {}


for key, value in app.config["HOSTS"].iteritems():
    h = ProxyHost()
    h.address = value["address"]
    h.port = value["port"]
    h.displayname = value["displayname"]
    if h.displayname != key:
        raise ValueError("%s != $s" %(h.displayname, key))
    hosts[key] = h
    mappings[key] = []

mapping_file = app.config["MAPPINGFILE"]
if os.path.isfile(mapping_file):
    mappings = pickle.load(open(mapping_file))

def save():
    pickle.dump(mappings, open(mapping_file, "w"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hosts", methods=["GET"])
def hosts_route():
    return render_template("hosts.html", hosts = app.config["HOSTS"].keys())

@app.route("/host/<host>", methods = ["GET"])
def host(host):
    h = app.config['HOSTS'][host]
    m = mappings.get(host, "")
    return render_template("host.html", host = h, mappings = m)

@app.route("/edit/<host>", methods = ["GET", "POST"])
def edit(host):
    if request.method == "GET":
        m = mappings.get(host, "")
        return render_template("edit.html", host = host, mapping = m)
    else:
        try:
            loaded_mapping = parse_mapping(request.form)
        except ValueError as e:
            return render_template("saved.html", error = str(e))
        mappings[host].append(loaded_mapping)
        save()
        result = apply_remote_config(host)
        if not result:
            return render_template("saved.html", error = "Cannot apply remote configuration")
        return render_template("saved.html", host = host)

@app.route("/remove/<host>/<mapping>")
def remove(host, mapping):
    mappings[host] = [m for m in mappings[host] if m.tostr() != mapping]
    save()
    return render_template("saved.html", host=host)


def parse_mapping(form):
    m = ProxyMapping()
    print form
    if "ssl" in form:
        print "GOT SSL!"
        if form["ssl_certificate"] == "":
            raise ValueError("Empty ssl certificate")
        if form["ssl_key"] == "":
            raise ValueError("Empty ssl key")
        m.serverssl = True
        m.servercertificate = form["ssl_certificate"].encode("ascii", "ignore")
        m.serverkey = form["ssl_key"].encode("ascii", "ignore")
        m.serverport = 443
    try:
        servername, remotehost, remoteport = form["remotes"].encode("ascii", "ignore").strip().split(":")
        m.servername = servername
        m.remotehost = remotehost
        m.remoteport = int(remoteport)
    except:
        raise ValueError("Cannot parse mapping")
    return m

def unixify(s):
    return  re.sub("[^a-zA-Z0-9]","_",s)

def apply_remote_config(host):
    h = hosts[host]
    try:
        e = RemoteExecutor(h.address, h.port, app.config["REMOTE_USER"], app.config["SSH_KEY_FILE"])
        e.connect()
        # 1) cleanout nginx ssl files
        e.send_command("rm -rf " + app.config["NGINX_SSL_DIR"] + "/*")
        e.send_command("rm -f " + app.config["NGINX_CONFIG_DIR"] + "/*")
        # 2) put the files in for each mapping
        for m in mappings[host]:
            # create safe name for ssl cert dir and for config
            c = NginxProxy(m.servername, 80, m.remotehost+":"+str(m.remoteport))
            safename = unixify(m.tostr())
            if m.serverssl:
                ssl_dirname = app.config["NGINX_SSL_DIR"] + "/" + safename
                cert_fname = ssl_dirname + "/server.crt"
                key_fname = ssl_dirname + "/server.key"
                e.send_command("sudo mkdir -p " + ssl_dirname)
                e.send_file(StringIO.StringIO(m.servercertificate), cert_fname)
                e.send_file(StringIO.StringIO(m.serverkey), key_fname)
                c.ssl = True
                c.port = 443
                c.ssl_certificate_path = cert_fname
                c.ssl_key_path = key_fname
            config_fname = app.config["NGINX_CONFIG_DIR"] + "/" + safename + ".conf"
            e.send_file(StringIO.StringIO(c.gen_config()), config_fname)
        e.send_command("/etc/init.d/nginx restart")

        return True
    except (ValueError, IOError, RuntimeError) as e:
        app.logger.error(e)
        return False

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"])
    save()
