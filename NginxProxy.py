TEMPLATE = '''
upstream backend {{
    {remote}
}}

server {{
    listen {port};
    server_name {server_name};

    {ssl}
    {ssl_certificate_path}
    {ssl_key_path}

    location / {{
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://backend/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }}
}}
'''

class NginxProxy(object):
    def __init__(self, server_name, port, remote,  ssl=False, ssl_certificate_path="/etc/nginx/ssl/server.crt", ssl_key_path="/etc/nginx/ssl/server.key"):
        self.server_name = server_name
        self.port = port
        self.ssl = ssl
        self.ssl_certificate_path = ssl_certificate_path
        self.ssl_key_path = ssl_key_path
        self.remote = remote

    def gen_config(self):
        d= {
            "remote" : "server " + self.remote + ";",
            "server_name" : self.server_name,
            "port" : self.port,
            "remote" : "server " + self.remote + ";",
            "ssl" : "",
            "ssl_certificate_path" : "",
            "ssl_key_path" : ""
        }
        if self.ssl:
            d.update({
                "ssl" : "ssl on;",
                "ssl_certificate_path" : "ssl_certificate " + self.ssl_certificate_path + ";",
                "ssl_key_path" : "ssl_certificate_key " + self.ssl_key_path + ";",
            })
        return TEMPLATE.format(**d)


if __name__ == "__main__":
    c = NginxProxy("test.example.com", "80", "1.2.3.4:5555")
    print c.gen_config()
    c = NginxProxy("test.example.net", "80", "1.2.3.4:5555", ssl=True, ssl_certificate_path="/etc/nginx/ssl/server.crt", ssl_key_path = "/etc/nginx/ssl/server.key")
    print c.gen_config()
