# This file defines all APIs of FTI
# and all the necessary data structures/classes

import os
from mpi4py import MPI

# CONSTANTS
FTI_BUFS = 256
FTI_DEFAULT_MAX_VAR_ID = 2147483647 # to be replaced by something more convenient.
FTI_LIMIT_MAX_VAR_ID = 100*1024
FTI_WORD = 16

# debug 
FTI_EROR = 4
FTI_WARN = 3
FTI_IDCP = 5
FTI_INFO = 2
FTI_DBUG = 1


# FTI structures
# class Params():
#     def __init__(self):
#         self.var1 : int = None
#         self.var2 : str = None

# FTIT_mqueue

class FTIT_globalDataset():
	def __init__(self):
		self.initialized : bool = None
		self.rank = None
		self.id = None
		self.varId = None
		self.numSubSets = None

class FTIT_type():
    def __init__(self):
    	self.id = None
    	self.size = None


class FTIT_dimension():
	def __init__(self):
		self.ndims = None
		self.count = [None] * 32


class FTIT_attribute():
	def __init__(self):
		self.dim : FTIT_dimension = None
		self.name : str = None


class FTIT_Datatype():
	def __init__(self):
		self.id = None
        self.size = None


class FTIT_dataset():
	def __init__(self):
		self.eleSize = None
		self.rank = None
		self.dimLength = [None] * 32
		self.recovered : bool = None
		self.isDevicePtr : bool = None
		self.count = None
		self.size = None
		self.sizeStored = None
		self.filePos = None
		self.attribute : FTIT_attribute = None
		self.type : FTIT_Datatype= None
		self.idChar : str = None
		self.name : str = None


class FTIT_configuration():
	def __init__(self):
		self.stagingEnabled : bool = None
		self.dcpFtiff : bool = None
		self.dcpPosix : bool = None
		self.keepL4Ckpt : bool = None
		self.keepHeadsAlive : bool = None
		self.dcpMode;
		self.dcpBlockSize;
		self.cfgFile : str = None
		self.saveLastCkpt = None
		self.verbosity = None
		self.blockSize = None
		self.transferSize = None
		self.maxVarId = None
		self.ckptTag = None
		self.stageTag = None
		self.finalTag = None
		self.generalTag = None
		self.test = None
		self.l3WordSize = None
		self.ioMode = None
		self.stageDir : str = None
		self.localDir : str = None
		self.glbalDir : str = None
		self.metadDir : str = None
		self.lTmpDir : str = None
		self.gTmpDir : str = None
		self.mTmpDir : str = None
		self.cHostBufSize = None
		self.suffix : str = None

class FTIT_checkpoint():
	def __init__(self):
		self.dir : str = None
		self.L4Replica : str = None
		self.dcpDir : str = None
		self.archDir : str = None
		self.archMeta : str = None
		self.metaDir : str = None
		self.dcpName : str = None
		self.isDcp : bool = None
		self.recoIsDcp : bool = None
		self.hasDcp : bool = None
		self.hasCkpt : bool = None
		self.isInline = None
		self.ckptIntv = None
		self.ckptCnt = None
		self.ckptDcpIntv = None
		self.ckptDcpCnt = None
		self.localReplica : bool = None

class FTIT_injection():
	def __init__(self):
		self.rank = None
		self.index = None
		self.position = None
		self.number = None
		self.frequency = None
		self.counter = None
		self.timer = None

class FTIT_topology():
	def __init__(self):
		self.nbProc = None
		self.nbNodes = None
		self.myRank = None
		self.splitRank = None
		self.nodeSize = None
		self.nbHeads = None
		self.nbApprocs = None
		self.groupSize = None
		self.sectorID = None
		self.nodeID = None
		self.groupID = None
		self.amIaHead = None
		self.headRank = None
		self.headRankNode = None
		self.nodeRank = None
		self.groupRank = None
		self.right = None
		self.left = None
		self.body : [None] * FTI_BUFS

class FTIT_metadata():
	def __init__(self):
		self.level;
		self.ckptId;
		self.ckptIdL4;
		self.maxFs;
		self.fs;
		self.pfs;
		self.ckptFile[FTI_BUFS];

class FTIT_execution():
	def __init__(self):
		self.id : str = None
		self.reco = None
		self.ckptLvel = None
		self.ckptIntv = None
		self.lastCkptLvel = None
		self.wasLastOffline = None
		self.iterTime = None
		self.lastIterTime = None
		self.meanIterTime = None
		self.globMeanIter = None
		self.totalIterTime = None
		self.syncIterMax = None
		self.minuteCnt = None
		self.hasCkpt : bool = None
		self.ckptCnt = None
		self.ckptIcnt = None
		self.ckptId = None
		self.ckptNext = None
		self.ckptLast = None
		self.ckptSize = None
		self.nbVar = None
		self.nbVarStored = None
		self.nbGroup = None
		self.initSCES = None
		self.integrity : str = None
		#self.mqueue : FTIT_mqueue = None
		self.ckptMeta : FTIT_metadata = None
		self.datatypes : FTIT_DataTypes = None
		self.globalDatasets : FTIT_globalDataset = None
		self.globalComm = None
		self.groupComm = None
		self.nodeComm = None
		self.fastForward = None


# APIs

def FTI_Init():
	print("lol")


def FTI_Print(msg, priority):
	if priority < FTI_Conf.verbosity:
        return
    if not msg:
     	return

    if priority == FTI_EROR:
    	print("\033[91m{}\033[00m" .format(msg))

    elif priority == FTI_WARN:
    	print("\033[93m{}\033[00m" .format(msg))

    elif priority == FTI_INFO:
    	if (FTI_Topo.splitRank == 0):
    		print("\033[92m{}\033[00m" .format(msg))

    elif priority == FTI_IDCP:
    	if (FTI_Topo.splitRank == 0):
    		print("\033[96m{}\033[00m" .format(msg))

    elif priority == FTI_DBUG:
    	print(msg)


