from threading import Thread
from zhelpers import socket_set_hwm
import zmq
import time

import subprocess

def cephfs_send(file):
   start = time.time()
   lock = ['touch','/ceph/atate/transporter/lockfile']
   subprocess.call(lock)
# write to cephfs
   write = ['cp','/home/atate/transporter/'+str(file.name),'/ceph/atate/transporter/']
   subprocess.call(write)

# let receiver know its OK to write 
   unlock = ['rm','/ceph/atate/transporter/lockfile']
   subprocess.call(unlock)
   end = time.time()
   print("CEPHFS: SEND time %f " %(end-start))
