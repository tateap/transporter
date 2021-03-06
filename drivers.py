
import subprocess
#from cephfs_send import cephfs_send
#from cephreados_send import cephrados_send
from tests.zeromq.zeromq_send import zeromq_send
from tests.mpi.mpi_send import mpi_send, mpi_send_netcdf

import threading
import time
import argparse


def recv(tf,test,args):
  # use srun to run on the remote resource
# has to spawn a new process to do so 
  print test
  if test != 'mpi':

    method_suffix = ''
    if args.format != 'binary':
      method_suffix += '_' + args.format
      
    srun = ['srun','-N1','--ntasks-per-node=1','python','./tests/'+str(test)+'/recv'+str(method_suffix)+'.py']
    proc = subprocess.Popen(srun)#, stdout=subprocess.PIPE)
    # if we want to get back info from stdout, it will be ,stdout=subprocess.PIPE)
  else:
    if args.format == 'binary':
      from tests.mpi.recv import recv as mpi_recv
      mpi_recv()
    if args.format == 'netcdf':
      from tests.mpi.recv_netcdf import recv as mpi_recv_netcdf
      mpi_recv_netcdf()

def send(tf,test,args):

    chunksize = args.chunksize
  # generic method calling (lifted from stackexchange)

    method_name = str(test)+'_send'
    if args.format != 'binary':
      method_name += '_' + args.format
    possibles = globals().copy()
    possibles.update(locals())

    method = possibles.get(method_name)
    if not method:
      raise NotImplementedError("Method %s not implemented" % method_name)
    method(tf,chunksize)

    return

def driver(test,tfile,args):
  
  tf = tfile
  start = time.time()


  if test != 'mpi':

    # start the receiver in one thread
    ts = []
    recv_thread = threading.Thread(target=recv(tf,test,args))
    recv_thread.start()
    ts.append(recv_thread)

    # start the sender in another thread

    send_thread = threading.Thread(target=send(tf,test,args))
    send_thread.start()
    ts.append(send_thread)

    for t in ts:
      t.join()

  else:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank==0:
      #print("%d sends" % rank)
      send(tf,test,args)
    else:
      #print("%d receives" %rank)
      recv(tf,test,args)


  end = time.time()
  time_transmission = end-start
