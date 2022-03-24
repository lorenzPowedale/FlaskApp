from flask import Flask, request
import os
import subprocess

app = Flask(__name__)


@app.route('/createUser', methods=['POST'])
def createUser():
    try:
        username = request.json['username'].strip()
        password = request.json['password'].strip()
    except:
        print("Fail")
        return "Failed!", 400

    sp = subprocess.getoutput(f"sudo useradd {username}")
    if sp:
        print("User already exists")
        return "User already exists", 409

    os.system(f"sudo adduser {username} gns_users")
    os.system(f"usermod --shell /sbin/nologin {username}")
    os.system(f'echo "{username}:{password}" | chpasswd')
    os.system(f"sudo mkdir /var/sftp/gns_users/chroot/{username}")
    os.system(f"chown {username} /var/sftp/gns_users/chroot/{username}")
    os.system(f"chmod 700 /var/sftp/gns_users/chroot/{username}")

    return "Success!", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0")
