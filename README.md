
# Introduction 
Objective is to give a GUI page to represent current state of Network Health.

## Getting Started
### Installation
1. Requirements
    - Ubuntu Server (Minimal hardware requirements)
    - Python3 installed for Django
<pre>
apt-get install -y python3 python3-dev python3-setuptools build-essential libxml2-dev libxslt1-dev libffi-dev graphviz libpq-dev libssl-dev zlib1g-dev python3-pip libldap2-dev
</pre>

2. Packages to install on Ubuntu Server (All installed via pip3)
    - netmiko
    - Django

<pre>
pip3 install netmiko django
</pre>

3. Install additional packages. Not necessarily needed, but good to do so:

4. Clone the Git Repository
    - Make files and move to the directory
<pre>mkdir -p /opt/nhweb && cd /opt/nhweb</pre>

- Clone the Repo (Don't forget the period on the end)
You may need to create new RSA public keys and assign to your ID in Git. You should do this from the root account.
<pre>
sudo git clone <git_url> .
</pre>

5. Change the allowed hosts within settings.py to match what is necessary [WIP]
6. Install Web Server - nginx
<pre>
apt-get install -y nginx
</pre>
7. Modify <code>/etc/nginx/sites-available/nhweb</code>
<pre>
server {
    listen 80;

    server_name networkhealth.example.com;

    client_max_body_size 25m;

    location /static/ {
        alias /opt/nhweb/nhweb/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
    }
}
</pre>
8. Delete <code>/etc/nginx/sites-enabled/default</code> and create a symlink <code>sites-enabled</code> directory to the configuration file just created.

<pre>
#cd /etc/nginx/sites-enabled
#rm default
#ln -s /etc/nginx/sites-available/nhweb
</pre>
9. Restart nginx (<code>service nginx restart</code>)

### gunicorn Installation
Install gunicorn via <code>pip</code><br>
<pre><code>pip3 install gunicorn</code></pre>
Save the following configuration in the root nhweb installation path as <code>gunicorn_config.py</code>. Such as <code>/opt/nhweb/gunicorn_config.py</code>
<pre>
command = '/usr/bin/gunicorn'
pythonpath = '/opt/nhweb/NetworkHealthWeb'
bind = '127.0.0.1:8001'
workers = 4
user = 'www-data'
</pre>

### supervisord Installation
Install supervisor:
<pre># apt-get install -y supervisor</pre>
Save the following as <code>/etc/supervisor/conf.d/nhweb.conf</code>.
<pre>
[program:networkhealth]
command = gunicorn -c /opt/nhweb/gunicorn_config.py nhweb.wsgi
directory = /opt/nhweb/NetworkHealthWeb/
user = www-data
</pre>

### Documentation Updates Yet
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

## Build and Test
TODO: Describe and show how to build your code and run the tests. 

## Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://www.visualstudio.com/en-us/docs/git/create-a-readme). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)