# copy data from one memory to another
# formats 
#  -binary
#  -HDF5
#  -NetCDF
#  -ADIOS
#  -conduit
#
# transport:
#  rsync
#  scp
#  gridftp
#  mpi
#  conduit
#  CephFS
#  ceph rados
#  lustre
#  ZeroMQ
#  TCP
#  libfabric

from drivers import driver
import argparse

parser = argparse.ArgumentParser(description='Tests transport with different interfaces and data formats.')

parser.add_argument('--formats', '-f', help='comma-separated list of data formats to use', type=str, default='binary')
parser.add_argument('--interfaces', '-i', help='comma-separated list of interfaces to use', type=str,default='mpi,zeromq,cephfs')
parser.add_argument('--chunksize', type=int, default=250000, help='Size of chunks in which data is split, in bytes. Setting it to zero causes the whole data to be sent at once.')
parser.add_argument('--files', '-F', help='comma-separated list of files to transfer', type=str, default='testdata')

args=parser.parse_args()
formats = args.formats.split(',')
tests = args.interfaces.split(',')
files = args.files.split(',')
#for form in formats 
#  print form

#tests = {"mpi"} #, "zeromq", "cephfs"}
# "cephfs"}
#files = {"testdata"}

for f in files :
  for t in tests :
    if t != 'mpi':
      fo = open("testdata", "r")
      print ("Name of the file: ", fo.name)
      print ("Closed or not : ", fo.closed)
      print ("Opening mode : ", fo.mode)
      print ("Softspace flag : ", fo.softspace)
      driver(t,fo,args)
      fo.close()
    else:
      from mpi4py import MPI
      comm = MPI.COMM_WORLD
      rank = comm.Get_rank()
      if rank==0:
        fo = open("testdata", "r")
        print ("Name of the file: ", fo.name)
        print ("Closed or not : ", fo.closed)
        print ("Opening mode : ", fo.mode)
        print ("Softspace flag : ", fo.softspace)
        driver(t,fo,args)
        fo.close()
      else:
        fo = None
        driver(t,fo,args)
