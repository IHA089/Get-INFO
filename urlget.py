import subprocess
import os
import sys
from time import sleep

def start_ngrok_http(port=80):

    try:
        ngrok_path = os.path.join(os.getcwd(), "ngrok")

        if not os.path.isfile(ngrok_path):
            raise FileNotFoundError("Ngrok executable not found in the current directory.")

        process = subprocess.Popen(
            [ngrok_path, "http", str(port)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        sleep(4)

        result = subprocess.run(
            ["curl", "-s", "http://localhost:4040/api/tunnels"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception("Failed to fetch tunnel details from ngrok API.")

        tunnels = json.loads(result.stdout)
        for tunnel in tunnels.get("tunnels", []):
            if tunnel.get("proto") == "https":
                return tunnel.get("public_url")

        raise Exception("No HTTPS tunnel found.")

    except Exception as e:
        print(f"Error: {e}")
        return None

def create_public_connection():
    file = "forward.txt"
    command = "ssh -R 80:0.0.0.0:4567 serveo.net -y > {} &".format(file)
    subprocess.Popen(command, shell=True)

def get_public_url():
    ffile = "forward.txt"
    file = open(ffile, 'r')
    read_data = file.read()
    os.remove(ffile)
    file.close()
    new_data = read_data.replace("Forwarding HTTP traffic from", "")
    new_data = new_data.replace("\n","")
    new_data = new_data.replace("\r","")
    if new_data == "":
        print("Please restart.....")
        sys.exit()
    else:
        return new_data
