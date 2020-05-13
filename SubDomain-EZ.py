import requests
import re
import subprocess
from subprocess import Popen, PIPE
import os
from termcolor import colored
import terminal_banner
import socket
import argparse
import subprocess
import shutil
import itertools
import time



parser = argparse.ArgumentParser(description='\u001b[36mSubZ - A Subdomain Enumeration Tool \u001b[0m')
parser.add_argument('-d','--domain' , help = 'Domain name of the taget [ex : bugcrowd.com]' , required=True)
parser.add_argument('-https', help='To get the Subdomains with HTTPS Service ',action='store_true')
parser.add_argument('-ip', help='To get the IP address of the Subdomains',action='store_true')

args = parser.parse_args()
os.system('clear')

banner = ("""\u001b[36m
                    
                
  ____        _     ____                        _             _____ _____
 / ___| _   _| |__ |  _ \  ___  _ __ ___   __ _(_)_ __       | ____|__  /
 \___ \| | | | '_ \| | | |/ _ \| '_ ` _ \ / _` | | '_ \ _____|  _|   / / 
  ___) | |_| | |_) | |_| | (_) | | | | | | (_| | | | | |_____| |___ / /_ 
 |____/ \__,_|_.__/|____/ \___/|_| |_| |_|\__,_|_|_| |_|     |_____/____|
                                                                         
                                                                        \u001b[0m  
                              \u001b[32m Made with \u001b[31m❤️\u001b[0m 
                    \u001b[32mFor the Community, By the Community   
                    ###################################
                        Developed by Jitesh Kumar
                Intagram  - https://instagram.com/jitesh.haxx
                   linkedin  - https://linkedin.com/j1t3sh
                     Github - https://github.com/j1t3sh
                                            
            ( DONT COPY THE CODE. CONTRIBUTIONS ARE MOST WELCOME \u001b[31m❤️\u001b[0m \u001b[32m)\u001b[0m 
                                                                                
""")

print(banner)

if args.https:
    args.https = "--prefer-https"
else:
    args.https = ""

def subez():
    spinner=itertools.cycle(['|','/','-','\\'])
    process=subprocess.Popen("assetfinder --subs-only " + args.domain + " | httprobe " + args.https +" > " + args.domain +".txt",shell=True)
    while process.poll() is None:
        time.sleep(0.5)
        cols=" "*(shutil.get_terminal_size((80, 20))[0]-65)
        count = len(open(args.domain+".txt").read().split('\n')) - 1
        print("\r[+]Searching Subdomains "+next(spinner)+ cols+ "\u001b[32mFound: "+str(count),end=''+"\u001b[0m ")
    list_sub = []
    new_list=[]
    file1 = open(args.domain + '.txt','r')
    count = 0
    while True:
        count +=1
        line = file1.readline()

        if not line:
            break
        list_sub.append(line)
    #print("Total no. of Subdomains Found for "+args.domain+" - "+str(len(list_sub)))
    print("\n")
    for i in range(len(list_sub)):
        z = str(list_sub[i])
        z = re.sub("\\n$","",z)
        new_list.append(z)
    print("[+]Scanning for the Services....")
    for q in new_list:
        def ip():
            if "https" in q:
                ipaddr = q.replce("https://","")
                return ipaddr
            else:
                ipaddr = q.replace("http://","")
                return ipaddr
    
    if args.ip:
        args.ip =  socket.gethostbyname(ip())
    else:
        args.ip = ""

    for m in new_list:
        try:
            response = requests.get(m)
            if response.status_code == 200:
                print("\u001b[32m"+m + " - " +args.ip+" :",response.status_code,response.reason+"\u001b[0m ")
            elif(400<response.status_code<500):
                print("\u001b[31m"+m+ " - " +args.ip+" :",response.status_code,response.reason+"\u001b[0m")
            else:
                print("\u001b[36m"+m+ " - " +args.ip+" :",response.status_code,response.reason+"\u001b[0m")
        except:
            continue   
    file1.close() 
    os.system("rm "+args.domain+".txt")


def assetfinder():
    print("\u001b[36m[+]Checking if assetfinder is installed.....\u001b[0m\n")
    p = Popen(['/usr/bin/which', "assetfinder"], stdout=PIPE, stderr=PIPE)
    p.communicate()
    if(p.returncode == 1): #If assetfinder not installed
        print("\u001b[31m[+]Assetfinder not found.\u001b[0m")
        print("\u001b[36m[+]Installing Assetfinder Please Wait......\u001b[0m")
        os.system("wget https://github.com/tomnomnom/assetfinder/releases/download/v0.1.0/assetfinder-linux-amd64-0.1.0.tgz")
        os.system("tar zxvf assetfinder-linux-amd64-0.1.0.tgz;chmod +x assetfinder;sudo cp assetfinder /usr/bin/;rm assetfinder-linux-amd64-0.1.0.tgz;rm assetfinder")
        assetfinder()
    else:
        print("\u001b[32m[+]Assetfinder Found.\u001b[0m\n")
        subez()

try:
    print("\u001b[36m[+]Checking if httprobe is installed.....\u001b[0m\n")
    s = Popen(['/usr/bin/which', "httprobe"], stdout=PIPE, stderr=PIPE)
    s.communicate()
    if(s.returncode == 1): #If httprobe not installed
        print("\u001b[31m[+]Httprobe not found.\u001b[0m")
        print("\u001b[36m[+]Installing httprobe Please Wait......\u001b[0m")
        os.system("sudo apt install git;sudo apt install golang;sudo git clone https://github.com/tomnomnom/httprobe;cd httprobe;sudo go build main.go;sudo mv main httprobe;sudo mv httprobe /usr/bin.")
    else:
        print("\u001b[32m[+]Httprobe Found.\u001b[0m\n")
        assetfinder()    

except:
   os.system("exit")