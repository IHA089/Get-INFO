import subprocess
import os

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
