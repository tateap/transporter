import zmq
import time
import os
#from zhelpers import socket_set_hwm

start = time.time()
ctxt = zmq.Context()

#  Socket to talk to server
socket = ctxt.socket(zmq.REQ)

router_ip = os.getenv('TRANSPORTER_ROUTER_IP', '127.0.0.1')
socket_addr = "tcp://"+router_ip+":5555"
print socket_addr

socket.connect(socket_addr)

socket.send(b"Analysis")

dealer = ctxt.socket(zmq.DEALER)
dealer_addr = "tcp://"+router_ip+":6000"
print dealer_addr

dealer.connect(dealer_addr)
dealer.send(b"fetch")

total = 0     # Total bytes received
chunks = 0    # Total chunks received

while True:
     try:
          chunk = dealer.recv()
     except zmq.ZMQError as e:
           if e.errno == zmq.ETERM:
                print "error"   # shutting down, quit
           else:
                raise
     chunks += 1
     size = len(chunk)
     total += size

     if size == 0:
          break   # whole file received

end = time.time()
walltime  = end - start

kilo_bytes = float(total) / float(1000.00)
mega_bytes = kilo_bytes / float(1000.00)
giga_bytes = mega_bytes / float(1000.00)

rate = giga_bytes / float(walltime)

print ("ZEROMQ: transfered %i GB in %f sec : %f GB/s rate" % (giga_bytes, walltime,rate))

dealer.send(b"done")
