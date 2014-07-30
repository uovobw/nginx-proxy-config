HOST="0.0.0.0"
PORT=8080
DEBUG=True
MAPPINGFILE="mappings.data"
NGINX_SSL_DIR="/etc/nginx/ssl"
NGINX_CONFIG_DIR="/etc/nginx/sites-enabled"
REMOTE_USER="root"
SSH_KEY_FILE="proxy_ssh_key_priv"
HOSTS={
    "UK" : {
        "displayname" : "UK",
        "port" : 22,
        "group" : "UK",
        "address": "proxy1.example.com",
        "displayaddress" : "some.host.com"
    },
    "HK": {
        "displayname" : "HK",
        "port" : 22,
        "group" : "HK",
        "address" : "proxy2.example.com",
        "displayaddress" : "someotherhost.host.com"
    },
    "HK-2": {
        "displayname" : "HK-2",
        "port" : 22,
        "group" : "HK",
        "address" : "proxy3.example.com",
        "displayaddress" : "yetanotherhost.host.com"
    }
}
