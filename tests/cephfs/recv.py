import zmq
import time

start = time.time()

#  Spin while a lock file exists or no file found

while True:
    try:
        open("/ceph/atate/transporter/lockfile", "r")
    except IOError:
        break

while True:
    try:
        open("/ceph/atate/transporter/testdata", "r")
    except IOError:
        continue
    else:
        print("found")
        break

# read and pull lines of the file into list

import os

fsize = os.path.getsize("/ceph/atate/transporter/testdata")

gbytes = fsize / 1000 / 1000 / 1000

f  =  open("/ceph/atate/transporter/testdata", "r")
a = []
for line in f:
    a.append(line)

end = time.time()
walltime  = end - start
rate = gbytes/walltime

print ("CEPHFS (RECV): %f GB in %f sec rate=%f GB/s" % (gbytes,walltime,rate))
