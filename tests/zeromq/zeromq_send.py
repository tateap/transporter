#  File Transfer model #1
#
#  In which the server sends the entire file to the client in
#  large chunks with no attempt at flow control.
#  TODO this is clearly labelled as the WRONG way to 
#  safely perform this operation

from threading import Thread
from zhelpers import socket_set_hwm
import zmq
import time

#CHUNK_SIZE = 250000

def zeromq_send(file, chunksize=250000):
   start = time.time()
   ctxt = zmq.Context()
   start_port = 5555
   tasks = {}
   print("binding REP socket to tcp://*:"+str(start_port))
   tasks[1] = (ctxt.socket(zmq.REP))
   tasks[1].bind("tcp://*:"+str(start_port))

   # loop until client tells us it's done
   #try:

   print tasks[1].recv()

  # file = open("testdata", "r")

   router = ctxt.socket(zmq.ROUTER)

   # Default HWM is 1000, which will drop messages here
   # since we send more than 1,000 chunks of test data,
   # so set an infinite HWM as a simple, stupid solution:
   socket_set_hwm(router, 0)
   router.bind("tcp://*:6000")

   while True:
   # First frame in each message is the sender identity
   # Second frame is "fetch" command
      try:
          identity, command = router.recv_multipart()
      except zmq.ZMQError as e:
          if e.errno == zmq.ETERM:
             return   # shutting down, quit
          else:
             raise
      if command != b"fetch":
          break
      while True:
           data = file.read(chunksize)
           router.send_multipart([identity, data])
           if not data:
               break
   end = time.time()
   print "ZeroMQ: Send time = %f "%(end-start)
