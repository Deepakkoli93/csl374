from socket import *
import socket
import time
import sys
import string
import random
import datetime

from datetime import datetime

# This function creates an arbitrary string of length size.
def create_random_string(size,chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def close_socket(sock):
    sock.close()
    

def create_socket(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'socket created'

    try: 
     ip = socket.gethostbyname(host)
    
    except socket.gaierror:
      print 'cannot resolve host name...exiting'
      sys.exit()
    

    print 'Ip address of ' + host + ' is ' + ip
    
    s.connect((ip,port))

    print 'Socket Connected successfully to ' + host + ' is ' + ip
    return s

    

def recv_from_server(sock):
  while True: 
   try:
    reply, addr = sock.recvfrom(1024)
    print "Datagram received from server.. "#+reply
   except socket.error:
    sys.exit()
    
   return (reply,addr)

def send_to_server(sock,data,host,port):
    #sock=create_socket(host,port)

    ip=socket.gethostbyname(host)
    try:
        sock.sendto(data,(ip,port))
    except socket.error:
        print 'Sending failed'
        sys.exit()

    print 'Datagram Sent to server!' 
    

# This function decrements TTL from datagram
# and returns updated datagram and TTL
def decrement_ttl_from_datagram(data):
    temp=data.split(',')
    #temp has a list [msg,timestamp,ttl]
    temp[2] = str(int(temp[2]) - 1)
    data=','.join(temp)
    
    return data

# This function fetch timestamp from datagram
def fetch_timestamp_from_datagram(data):
    temp=data.split(',')

    return float(temp[1])

# This function prints the cumalative RTT to a file
def dump_record(initial_timestamp, fobj):
    t=time.time() * 1000000
    fobj.write("RTT "+": "+ str((t-initial_timestamp))+'\n')
    return t-initial_timestamp


# This function adds TTL and timestamp to a datagram
def add_ttl_and_timestamp(msg, ttl):

    t=repr(time.time()*1000000)
    temp=[msg,t,str(ttl)]
    return ','.join(temp)
    
# This function sends datagrams to server, receives datagrams from
# server and dump record if TTL is zero.
# No need to check for packet loss.
def send_and_receive_datagrams(sock, msg, ttl, fobj, host, port):
    
    print ".....Record dumped...new datagram 1 is being generated......"
    data=add_ttl_and_timestamp(msg, ttl)
    print "sending... "+data
    ip=socket.gethostbyname(host)
    send_to_server(sock,data,host,port)
    #received,addr=recv_from_server(sock)
    i=1
    sum=0
    while (i<=50):
     #print "Entered the while loop"
     received,addr=recv_from_server(sock)
     decremented=decrement_ttl_from_datagram(received)
     temp=decremented.split(',')
     if (int(temp[2])==0): 
        sum+=dump_record(float(temp[1]), fobj)
        print "Record dumped " +str(i)
        i+=1
        if (i>50): 
           fobj.write("Cumulative RTT : "+str(sum))
           break
        print ".....New datagram "+str(i)+" is being generated......"
        newmsg = create_random_string(len(msg))
        newdata=add_ttl_and_timestamp(newmsg,ttl)
        send_to_server(sock,newdata,host,port)
        
        #print "sent for "+str(i)+" time"

     else:
        send_to_server(sock,decremented,host,port)
        
        #print "sent for "+str(i)+" time"
    sys.exit()



def usage():
    print "Usage <host> <port> <P> <TTL> <filename>"
    sys.exit()

if __name__ == "__main__":

    if len(sys.argv) != 6:
        usage()

    host = sys.argv[1]
    port = int(sys.argv[2])
    dlen = int(sys.argv[3])
    ttl = sys.argv[4]
    filename = sys.argv[5]

    if int(ttl) % 2 != 0:
        print "FATAL: TTL must be even"
        sys.exit()
    
    if int(ttl) < 2 or int(ttl) > 20:
        print "TTL must be in the range of 2 to 20"
        sys.exit()

    if dlen < 100 or dlen > 1300:
        print "Packet length must be in the range of 100 to 1300"
        sys.exit()

    fobj = open(filename, "wb")

    sock=create_socket(host,port)
    msg = create_random_string(dlen)
    send_and_receive_datagrams(sock, msg, ttl, fobj, host, port);
    close_socket(sock)
    fobj.close()
