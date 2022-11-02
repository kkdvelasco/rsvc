

import hashlib
import os
from socket import socket
import sys
import time
from urllib.request import Request, urlopen
from json import loads



soc = socket()


def current_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

username = "klaine07" 
mining_key = "klaine07_duino"
UseLowerDiff = False
#must have comma before miner name examle ,miner or ,duino_coin-3
miner_name = ",HP_LAPTOP"


def fetch_pools():
    while True:
        try:
            response = loads(urlopen(Request("https://server.duinocoin.com/getPool")).read().decode())
            NODE_ADDRESS = response["ip"]
            NODE_PORT = response["port"]
            
            return NODE_ADDRESS, NODE_PORT
        except Exception as e:
            print (f'{current_time()} : Error retrieving mining node, retrying in 15s')
            time.sleep(15)
print("#" * 60)
print("""
    \u001b[1m \u001b[48;5;214m ____  _   _ ___ _   _  ___        ____  ___ ____ \033[49m
    \u001b[1m \u001b[48;5;214m|  _ \| | | |_ _| \ | |/ _ \      |  _ \|_ _/ ___|\033[49m
    \u001b[1m \u001b[48;5;214m| | | | | | || ||  \| | | | |_____| |_) || | |  _ \033[49m
    \u001b[1m \u001b[48;5;214m| |_| | |_| || || |\  | |_| |_____|  _ < | | |_| |\033[49m
    \u001b[1m \u001b[48;5;214m|____/ \___/|___|_| \_|\___/      |_| \_\___\____|\033[49m
""")
print("#" * 60)
while True:
    try:
        pass
        try:
            NODE_ADDRESS, NODE_PORT = fetch_pools()
        except Exception as e:
            NODE_ADDRESS = "server.duinocoin.com"
            NODE_PORT = 2813
        soc.connect((str(NODE_ADDRESS), int(NODE_PORT)))
        server_version = soc.recv(100).decode()
                                                   
        
        
        while True:
            if UseLowerDiff:
                
                soc.send(bytes(
                    "JOB,"
                    + str(username)
                    + ",LOW,"
                    + str(mining_key),
                    encoding="utf8"))
            else:
                
                soc.send(bytes(
                    "JOB,"
                    + str(username)
                    + ",MEDIUM,"
                    + str(mining_key),
                    encoding="utf8"))

            
            job = soc.recv(1024).decode().rstrip("\n")
            
            job = job.split(",")
            difficulty = job[2]

            hashingStartTime = time.time()
            base_hash = hashlib.sha1(str(job[0]).encode('ascii'))
            temp_hash = None

            for result in range(100 * int(difficulty) + 1):
                # Calculate hash with difficulty
                temp_hash = base_hash.copy()
                temp_hash.update(str(result).encode('ascii'))
                ducos1 = temp_hash.hexdigest()

                
                if job[1] == ducos1:
                    hashingStopTime = time.time()
                    timeDifference = hashingStopTime - hashingStartTime
                    hashrate = result / timeDifference

                    
                    soc.send(bytes(
                        str(result)
                        + ","
                        + str(hashrate)
                        + miner_name,
                        encoding="utf8"))

                    # Get feedback about the result
                    feedback = soc.recv(1024).decode().rstrip("\n")
                    # If result was good
                    if feedback == "GOOD":
                        print(f'{current_time()} : \033[42mAccepted share\033[49m',
                              
                              "Hashrate",
                              int(hashrate/1000),
                              "kH/s",
                              "Difficulty",
                              difficulty)
                        break
                    # If result was incorrect
                    elif feedback == "BAD":
                        print(f'{current_time()} : \033[41mRejected share\033[49m',
                              result,
                              "Hashrate",
                              int(hashrate/1000),
                              "kH/s",
                              "Difficulty",
                              difficulty)
                        break

    except Exception as e:
        print(f'{current_time()} : \u001b[48;5;"Error occured\033[49: ' + str(e) + ", restarting in 5s.")
        time.sleep(5)
        os.execl(sys.executable, sys.executable, *sys.argv)
