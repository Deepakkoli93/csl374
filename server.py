from socket import *
import socket
import sys
import select

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
    
    s.bind((ip,port))

    print 'Socket binded successfully to ' + host + ' is ' + ip
    #s.listen(10)
    #print 'Socket now listening'
    #conn, addr = s.accept()
    return s
    

def recv_from_client(sock):
  while True:
    data, addr=sock.recvfrom(1024)
    print "Received from client"
    #print "\n addr is "+str(addr)
    return (data,addr)



def send_to_client(sock,data,addr):
  #for i in range(1,10):
    #ip=socket.gethostbyname(host)
    #sock.sendto(data,(ip,port))
    try:
        sock.sendto(data,addr)
    except socket.error:
        print 'Sending failed'
        sys.exit()

    print 'Message Sent to client!' 
    

# This function takes a datagram, decrements TTL
# and returns the updated datagram
def decrement_ttl_from_datagram(datagram):
    temp=datagram.split(',')
    #temp has a list [msg,timestamp,ttl]
    temp[2] = str(int(temp[2]) - 1)
    datagram=','.join(temp)
    
    return datagram

# This function receives a datagram from the client,
# decreases the TTL and sends the datagram back to the client.
# No need to check for packet loss.
def receive_and_send_datagrams(sock):
  while True:
  #for i in range(1,10):
    received,addr=recv_from_client(sock)
    print '\n'+received
    decremented=decrement_ttl_from_datagram(received)
    #print "decremented datagram"+ decremented
    send_to_client(sock,decremented,addr)


def usage():
    print "Usage <host> <port>"
    sys.exit()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage()

    host = sys.argv[1]
    port = int(sys.argv[2])

    sock=create_socket(host,port)
    receive_and_send_datagrams(sock)
    close_socket(sock)
