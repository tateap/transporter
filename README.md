# transporter
Hokey setup currently, 

we want to tests variety of input formats

HDF5
Conduit
NetCDF
ADIOS (perhaps)
...add more here

and variety of transport methods

MPI
cephFS
cephrados
ZeroMQ
flexpath
...add more here


Just run on JULIA

python transporter.py 

this should run the ZeroMQ and CephFS tests using SLURM on Compute nodes. 

