from mpi4py import MPI
import time
#from zhelpers import socket_set_hwm
import numpy as np

def recv():
  start = time.time()

  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  srcrank = 1-rank

  ndims = comm.recv(source = srcrank, tag = 101)

  shape = np.empty(ndims, dtype='i')
  shape = comm.recv(source=srcrank, tag=102)

  buff = np.empty(shape, dtype=np.float32)
  buff = comm.recv(source = srcrank, tag=123)


  end = time.time()
  walltime  = end - start

  total = buff.size * 4

  print total

  kilo_bytes = float(total) / float(1000.00)
  mega_bytes = kilo_bytes / float(1000.00)
  giga_bytes = mega_bytes / float(1000.00)

  rate = giga_bytes / float(walltime)

  print ("MPI: transfered %i GB in %f sec : %f GB/s rate" % (giga_bytes, walltime,rate))
