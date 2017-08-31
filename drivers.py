
import subprocess
from zeromq_send import zeromq_send
from cephfs_send import cephfs_send
#from cephreados_send import cephrados_send

import threading
import time

def recv(tf,test):
# use srun to run on the remote resource
# has to spawn a new process to do so 
    srun = ['srun','-N1','--ntasks-per-node=1','python','/home/atate/transporter/tests/'+str(test)+'/recv.py']
    proc = subprocess.Popen(srun)
    # if we want to get back info from stdout, it will be ,stdout=subprocess.PIPE)

def send(tf,test):

    # generic method calling (lifted from stackexchange)

    method_name = str(test)+'_send'
    possibles = globals().copy()
    possibles.update(locals())

    method = possibles.get(method_name)
    if not method:
        raise NotImplementedError("Method %s not implemented" % method_name)
    method(tf)

    return

def driver(test,tfile):
   tf = tfile
   start = time.time()

   # start the receiver in one thread
   ts = []
   recv_thread = threading.Thread(target=recv(tf,test))
   recv_thread.start()
   ts.append(recv_thread)

   # start the sender in another thread

   send_thread = threading.Thread(target=send(tf,test))
   send_thread.start()
   ts.append(send_thread)

   for t in ts:
      t.join()

   end = time.time()
   time_zeromq = end-start
