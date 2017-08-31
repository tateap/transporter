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
#  MPI
#  conduit
#  CephFS
#  ceph rados
#  lustre
#  ZeroMQ
#  TCP
#  libfabric

from drivers import driver

formats = ["binary"]

#for form in formats 
#  print form
tests = {"zeromq", "cephfs"}
# "cephfs"}
files = {"testdata"}

for f in files :
   for t in tests : 
       fo = open("testdata", "r")
       print "Name of the file: ", fo.name
       print "Closed or not : ", fo.closed
       print "Opening mode : ", fo.mode
       print "Softspace flag : ", fo.softspace
       driver(t,fo)
       fo.close()
