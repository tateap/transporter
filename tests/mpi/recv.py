from mpi4py import MPI
import time
#from zhelpers import socket_set_hwm


def recv():
  start = time.time()

  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  srcrank = 1-rank
  print srcrank


  total = 0     # Total bytes received
  chunks = 0    # Total chunks received
  chunk_id = 123

  while True:
    chunk = comm.recv(source=srcrank, tag = chunk_id)
    chunks = chunks + 1
    chunk_id = chunk_id + 1
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

  print ("MPI: transfered %i GB in %f sec : %f GB/s rate" % (giga_bytes, walltime,rate))
