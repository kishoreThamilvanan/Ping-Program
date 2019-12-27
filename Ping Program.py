# NAIM YOUSSIF TRAORE 111256860

import os
import struct
import socket
import time
import statistics

def ping(addr,packet,nb,timeout):

    stats = []

    for x in range (nb):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.connect((host, 7))
        print("ping",addr,"...")
        sock.settimeout(timeout)
        sock.send(packet)
        time_of_depature = time.time()
        sock.recv(1024)
        time_of_arrival = time.time()
        print("get ping in", time_of_arrival - time_of_depature)
        stats.append(time_of_arrival - time_of_depature)
        sock.close()
    if len(stats) != 1:
        print("\nstatistics:")
        print("mean",statistics.mean(stats))
        print("stdev", statistics.stdev(stats))
        print("min", min(stats))
        print("max", max(stats))

def checksum(source_string):
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = source_string[count + 1]*256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2
    if countTo<len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    return answer

ICMP_TYPE=8
ICMP_CODE=0
ID=os.getpid()&0xFFFF
SEQUENCE=1
CHECKSUM=0
header = struct.pack("bbHHh", ICMP_TYPE, ICMP_CODE, CHECKSUM, ID, SEQUENCE)
data=bytes("paul","utf-8")
CHECKSUM=checksum(header+data)
header = struct.pack("bbHHh", ICMP_TYPE, ICMP_CODE, CHECKSUM, ID, SEQUENCE)
packet=header+data


while True:
    while True:
        try:
            host = input("Target host : ")
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.connect((host, 7))
            break
        except socket.gaierror:
            print("<INVALID ADDRESS>");

    timeout = float(input("Enter timeout (sec): "))
    nbpack = int(input("Enter #packets: "))
    try:
        ping(host,packet,nbpack,timeout)
    except socket.timeout:
        timeout = int(input("Enter timeout (sec): "))
        print("<FAILED>")

    if input("Done? (y/n) ") != 'n':
        break



