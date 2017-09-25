#  File Transfer model #1
#
#  In which the server sends the entire file to the client in
#  large chunks with no attempt at flow control.
#  TODO this is clearly labelled as the WRONG way to 
#  safely perform this operation

from threading import Thread
from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

destrank = 1-rank

def mpi_send(file, chunksize=250000):
  start = time.time()

  #loop until client tells us it's done
  #try:


  #file = open("testdata", "r")


  #First frame in each message is the sender identity
  #Second frame is "fetch" command
  if chunksize>0:
    chunk_id = 123
    while True:
      data = file.read(chunksize)
      #print("Rank %d sending chunk id %d to rank %d" %(rank, chunk_id, destrank))
      comm.send(data, dest = destrank, tag = chunk_id)
      chunk_id = chunk_id + 1
      if not data:
        break
  else:
    data = file.read()
    comm.send(data, dest = destrank, tag = 123)
    data = file.read()
    comm.send(data, dest = destrank, tag = 124)

  end = time.time()
  print("MPI: Send time = %f "%(end-start))
