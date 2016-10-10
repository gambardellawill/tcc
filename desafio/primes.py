# *-* coding: utf-8 -*-

# Use: mpirun -np 4 -machinefile ../api/machinefile python primes.py -n nceiling

from mpi4py import MPI as mpi
import numpy as np
import sys
import math

comm = mpi.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def vectorSize(numOfProcesses,sequenceSize, rankNumber):
    remainder = sequenceSize%numOfProcesses

    if remainder == 0:
        return sequenceSize/numOfProcesses
    else:
        if rankNumber < remainder:
            #print math.ceil(sequenceSize/numOfProcesses)
            return math.ceil(sequenceSize/numOfProcesses)
        else:
            #print math.floor(sequenceSize/numOfProcesses)
            return math.floor(sequenceSize/numOfProcesses)

print "I'm process number %d" % rank

nceiling = None
mainSieve = None
workerSieve = None
workerSieveBuffer = None
msBuffer = None
displs = []
counts = []

if rank==0:
    cmdargs = sys.argv
    nceiling = int(cmdargs[2])
    mainSieve = np.arange(2,nceiling,dtype=np.float)

nceiling = comm.bcast(nceiling, root=0)
print "I'm process number %d and the ceiling number is %d" % (rank,nceiling)


if rank == 0:
    for x in range(0,size):
        counts.append(vectorSize(float(size),float(nceiling-1),x))
        if x == 0:
            displs.append(0)
        #elif x == size-1:
        #    displs.append(displs[x-1])
        else:
            print counts[x-1]+displs[x-1]
            displs.append(counts[x-1]+displs[x-1])

    counts = tuple(counts)
    print counts

    displs = tuple(displs)
    print displs

workerSieve = np.zeros(vectorSize(float(size),float(nceiling-1),rank))
workerSieveBuffer = np.getbuffer(np.zeros(vectorSize(float(size),float(nceiling-1),rank)))
#print len(workerSieve)

comm.Barrier()

if rank == 0:
    msBuffer = buffer(mainSieve)

if rank == size-1:
    print workerSieve

comm.Scatterv([msBuffer,counts,displs,mpi.DOUBLE],workerSieveBuffer, root=0)

workerSieve = np.frombuffer(workerSieveBuffer)

if rank == size-1:
    print workerSieve
#if rank == 3:
#    print "Process "+str(rank)+" has buffer with length "+str(len(workerSieve))

#comm.scatter(mainSieve,workerSieve,root=0)
