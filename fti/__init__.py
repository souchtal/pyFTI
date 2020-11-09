# This file defines all APIs of FTI
# and all the necessary data structures/classes

import os
from mpi4py import MPI
from fti import tools
from fti import keymap
from fti import conf

# CONSTANTS
FTI_BUFS = 256
FTI_COMM_WORLD = None
# debug 
FTI_EROR = 4
FTI_WARN = 3
FTI_IDCP = 5
FTI_INFO = 2
FTI_DBUG = 1

FTI_DONE = 1
FTI_SCES = 0
FTI_NSCS = -1


# FTI structures
# class Params():
#     def __init__(self):
#         self.var1 : int = None
#         self.var2 : str = None

# FTIT_mqueue


class FTIT_Datatype():
    def __init__(self):
        self.id = None
        self.size = None  


class FTIT_DataTypes():
    def __init__(self):
        self.ntypes = None
        self.nprimitives = None
        self.primitive_offset = None
        self.types : FTIT_Datatype = None


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


class FTIT_dataset():
    def __init__(self):
        self.id = None
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
        self.dcpMode = None
        self.dcpBlockSize = None
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
        self.level = None
        self.ckptId = None
        self.ckptIdL4 = None
        self.maxFs = None
        self.fs = None
        self.pfs = None
        self.ckptFile : str = None

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


# Initialize class objects
FTI_Conf = FTIT_configuration()
FTI_Ckpt = [FTIT_checkpoint()] * 5
# for i in range(5):
#     FTI_Ckpt.append(FTIT_checkpoint())
FTI_Exec = FTIT_execution()
FTI_Topo = FTIT_topology()
# FTI_Data = FTIT_keymap()
FTI_Inje = FTIT_injection()


# APIs
def FTI_Init(configFile, globalComm):
    
    tools.FTI_InitExecVars(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt, FTI_Inje)
    
    FTI_Exec.globalComm = globalComm

    # MPI_Comm_rank(FTI_Exec.globalComm, &FTI_Topo.myRank);
    # MPI_Comm_size(FTI_Exec.globalComm, &FTI_Topo.nbProc);
    FTI_Topo.myRank = globalComm.Get_rank()
    FTI_Topo.nbProc = globalComm.Get_size()

    FTI_Conf.cfgFile = configFile
    FTI_Conf.verbosity = 1
    FTI_Exec.initSCES = 0
    # FTI_Inje.timer = MPI_Wtime()
    global FTI_COMM_WORLD
    FTI_COMM_WORLD = globalComm
    FTI_Topo.splitRank = FTI_Topo.myRank
    
    res = conf.FTI_LoadConf(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt, FTI_Inje)
    if res == FTI_NSCS :
      return FTI_NSCS

    res = FTI_Topology(FTI_Conf, FTI_Exec, FTI_Topo)
    if res == FTI_NSCS :
      return FTI_NSCS

    FTI_InitGroupsAndTypes(FTI_Exec)

    if (FTI_Topo.myRank == 0) :
        restart = FTI_Exec.reco if (FTI_Exec.reco != 3) else 0
        FTI_UpdateConf(FTI_Conf, FTI_Exec, restart)
    
    comm.Barrier() 

    FTI_Conf.suffix = "fti"

    # FTI_KeyMap(FTI_Data, sizeof(FTIT_dataset), FTI_Conf.maxVarId, true)

    # FTI_Exec.initSCES = 1;

    # # init metadata queue
    # FTI_MetadataQueue(FTI_Exec.mqueue)

    # if FTI_Topo.amIaHead :
    #   if FTI_Exec.reco:
    #       res = FTI_RecoverFiles(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt)
    #       if res != FTI_SCES :
    #           FTI_Exec.reco = 0
    #             FTI_Exec.initSCES = 2
    #     FTI_Listen(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt)
    #     return FTI_HEAD

    # else :
    #   if FTI_InitFunctionPointers(FTI_Conf.ioMode, FTI_Exec) :
    #         print("Cannot define the function pointers")
        
    #     if (FTI_Exec.reco) :
    #         res = FTI_RecoverFiles(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt)
            
    #         FTI_Exec.ckptCnt = FTI_Exec.ckptId
    #         FTI_Exec.ckptCnt = FTI_Exec.ckptCnt + 1
    #         if (res != FTI_SCES) :
    #             FTI_Exec.reco = 0;
    #             FTI_Exec.initSCES = 2;  
    #             print("FTI has been initialized.")
    #             return FTI_NREC
            
    #         FTI_Exec.hasCkpt = false if (FTI_Exec.reco == 3) else true
    #         if (FTI_Exec.reco != 3) :
    #           FTI_LoadMetaDataset(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt, FTI_Data)
        
        print("FTI has been initialized.")
        return FTI_SCES


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


def FTI_GetType(id):
    if (id < 0 or id >= FTI_Exec.datatypes.ntypes) :
      return None
    return FTI_Exec.datatypes.types[id]


# def FTI_Protect(id, ptr, count, tid):
#     if (FTI_Exec.initSCES == 0) :
#         print("FTI is not initialized.")
#         return FTI_NSCS
#     if (id > FTI_Conf.maxVarId) :
#         print("Id out of bounds Basic:max_var_id ="+str(FTI_Conf.maxVarId))
#         return FTI_NSCS

#     data = FTIT_dataset()
#     if (FTI_Data.get(data, id) != FTI_SCES) :
#         print("failed to protect variable")
#         return FTI_NSCS
    
#     if (data != None) :
#         prevSize = data.size
#         # GPU code later
#         memLocation = "CPU"
#         data.isDevicePtr = False
#         data.devicePtr = None   
#         data.ptr = ptr
#         data.count = count
#         data.type = FTI_GetType(tid)
#         if (data.type == None) :
#             print("Invalid data type handle on FTI_Protect.")
#             return FTI_NSCS
#         data.eleSize = data.type.size
#         data.size = data.type.size * count
#         data.dimLength[0] = count
#         FTI_Exec.ckptSize = FTI_Exec.ckptSize + ((data.type.size * count) - prevSize)
#         if len(data.idChar) == 0:
#             string = "Variable ID "+str(id)+" reseted. " + \
#               "(Stored In " + memLocation + ").  Current ckpt. size per rank is "+str(FTI_Exec.ckptSize / (1024.0 * 1024.0))+"MB."
#         else:
#             string = "Variable Named "+data.idChar+" with ID "+str(id)+" to" + \
#             " protect (Stored in "+ memLocation +"). Current ckpt. size per rank is "+str(FTI_Exec.ckptSize / (1024.0 * 1024.0))+"MB."

#         print(string)

#         if (data.recovered) :
#             if len(data.idChar) == 0:
#                 string = "Variable ID "+str(id)+" reseted. " + \
#                   "(Stored In " + memLocation + ").  Current ckpt. size per rank is "+str(FTI_Exec.ckptSize / (1024.0 * 1024.0))+"MB."
#             else:
#                 string = "Variable Named "+data.idChar+" with ID "+str(id)+" to" + \
#                 " protect (Stored in "+ memLocation +"). Current ckpt. size per rank is "+str(FTI_Exec.ckptSize / (1024.0 * 1024.0))+"MB."

#             print(string)
#             FTI_Exec.nbVar = FTI_Exec.nbVar + 1 
#             data.recovered = False

#         return FTI_SCES

#     # Id could not be found in datasets
#     data = []
#     data.append(FTIT_dataset())

#     data.id = id

#     # GPU code
#     memLocation = "CPU"
#     data.isDevicePtr = false
#     data.devicePtr = None
#     data.ptr = ptr # this needs to be removed


#     data.sharedData.dataset = None
#     data.count = count
#     data.type = FTI_GetType(tid)
#     if (data.type == NULL) :
#         print("Invalid data type handle on FTI_Protect.")
#         return FTI_NSCS
    
#     data.eleSize = data.type.size
#     data.size = data.type.size * count
#     data.rank = 1
#     data.dimLength[0] = data.count

#     data.name = "Dataset_"+str(id)
#     FTI_Exec.ckptSize = FTI_Exec.ckptSize + (data.type.size * count)


#     # append dataset to protected variables
#     if (FTI_Data.push_back(data, id) != FTI_SCES) :
#         string = "failed to append variable with id = '"+str(id)+"' to protected variable map."
#         print(string)
#         return FTI_NSCS
    

#     if (len(data.idChar) == 0) :
#         string = "Variable ID "+str(id)+" to protect (Stored in "+memLocation+"). Current ckpt. size per rank is "+str(FTI_Exec.ckptSize / (1024.0 * 1024.0))+"MB."
#     else :
#         string = "Variable Named "+data.idChar+" with ID "+str(id)+" to protect (Stored in "+memLocation+"). Current ckpt. size per rank is "+str(FTI_Exec.ckptSize / (1024.0 * 1024.0))+"MB."
    
#     FTI_Exec.nbVar = FTI_Exec.nbVar + 1
#     print(string)

#     return FTI_SCES


# def FTI_Checkpoint(id, level):
#     if (FTI_Exec.initSCES == 0) :
#         print("FTI is not initialized.")
#         return FTI_NSCS
    

#     if ((level < FTI_MIN_LEVEL_ID) or (level > FTI_MAX_LEVEL_ID)) :
#         print("Invalid level id! Aborting checkpoint creation...")
#         return FTI_NSCS
    
#     FTI_Exec.ckptMeta.ckptId = id

#     # start time MPI_Wtime t0
#     FTI_Exec.ckptMeta.level = level

#     # start time MPI_Wtime t1
#     res = FTI_WriteCkpt(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt, FTI_Data)

#     # start time MPI_Wtime t2
#     if not FTI_Ckpt[FTI_Exec.ckptMeta.level].isInline :
#         FTI_Exec.activateHeads(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt, res)

#     else :  
#         FTI_Exec.wasLastOffline = 0
#         if (res != FTI_SCES) :
#             FTI_Exec.ckptMeta.level = FTI_REJW - FTI_BASE
        
#         res = FTI_PostCkpt(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt)
#         if (res == FTI_SCES) :
#             FTI_Exec.ckptLvel = FTI_Exec.ckptMeta.level
        
#     if (not FTI_Exec.hasCkpt and (FTI_Topo.splitRank == 0) and (res == FTI_SCES)) :
#         res = FTI_UpdateConf(FTI_Conf, FTI_Exec, 1)
#         FTI_Exec.initSCES = 1
#         if (res == FTI_SCES) :
#             FTI_Exec.hasCkpt = true


#     MPI.Comm.Bcast(FTI_Exec.hasCkpt, 1, MPI_INT, 0)

#     # start time MPI_Wtime t3
#     if (res != FTI_SCES) :
#         string = "Checkpoint with ID "+str(FTI_Exec.ckptMeta.ckptId)+" at Level "+str(FTI_Exec.ckptMeta.level)+" failed."
#         print(string)
#         return FTI_NSCS
    
#     string = "Ckpt. ID "+str(FTI_Exec.ckptMeta.ckptId)+" (L"+str(FTI_Exec.ckptMeta.level)+") ("+str(FTI_Exec.ckptSize / (1024.0 * 1024.0))+" MB/proc) taken in "+str(t3 - t0)+\
#     " sec. (Wt:"+str(t1 - t0)+"s, Wr:"+str(t2 - t1)+"s, Ps:"+str(t3 - t2)+"s)"

#     print(string)

#     FTI_Exec.nbVarStored = FTI_Exec.nbVar
#     FTI_Exec.ckptId = FTI_Exec.ckptMeta.ckptId

#     # FTIT_dataset* data;
#     data = []

#     if (FTI_Data.data(data, FTI_Exec.nbVar) != FTI_SCES) :
#         print("failed to finalize FTI")
#         return FTI_NSCS
    
#     for k in range(FTI_Exec.nbVar):
#         data[k].sizeStored = data[k].size
    
#     return FTI_DONE


# def FTI_Recover():
#     if (FTI_Exec.initSCES == 0) :
#         print("FTI is not initialized.")
#         return FTI_NREC
    
#     if (FTI_Exec.initSCES == 2) :
#         print("No checkpoint files to make recovery.")
#         return FTI_NREC

#     # fn[FTI_BUFS];  // Path to the checkpoint file
#     # str[2*FTI_BUFS];  // For console output

#     data = []
#     if (FTI_Data.data(data, FTI_Exec.nbVarStored) != FTI_SCES) :
#         print("failed to recover")
#         return FTI_NREC
    

#     if (FTI_Exec.ckptLvel == 4) :
#         if (FTI_Ckpt[4].recoIsDcp and FTI_Conf.dcpPosix) :
#             print("TODO")
#         else :
#             # Try from L1
#             snprintf(fn, FTI_BUFS, "%s/Ckpt%d-Rank%d.%s", FTI_Ckpt[1].dir,
#              FTI_Exec.ckptId, FTI_Topo.myRank, FTI_Conf.suffix)

#             fn = FTI_Ckpt[1].dir + '/Ckpt' + str(FTI_Exec.ckptId) + '-Rank' + str(FTI_Topo.myRank) + '.' + FTI_Conf.suffix
#             if not os.access(fn, os.R_OK):
#                 # if no L1 files try from L4
#                 fn = FTI_Ckpt[4].dir+'/'+FTI_Exec.ckptMeta.ckptFile
            
        
#     else :
#         fn = FTI_Ckpt[FTI_Exec.ckptLvel].dir+'/'+FTI_Exec.ckptMeta.ckptFile

#     print("Trying to load FTI checkpoint file "+fn)


#     with open(fn, 'rb') as f:
#         try:
#             if (FTI_Data.data(data, FTI_Exec.nbVarStored) != FTI_SCES) :
#                 print("failed to recover")
#                 return FTI_NREC

#             #for (i = 0; i < FTI_Exec.nbVarStored; i++) :
#             for i in range(FTI_Exec.nbVarStored):
#                 filePos = data[i].filePos
#                 f.seek(filePos, 0) # SEEK_SET file beginning
#                 data[i].ptr = f.read(data[i].sizeStored)

#                 # fseek(fd, filePos, SEEK_SET);
#                 # fread(data[i].ptr, 1, data[i].sizeStored, fd);
#                 # if (ferror(fd)) :
#                 #     FTI_Print("Could not read FTI checkpoint file.", FTI_EROR);
#                 #     return FTI_NREC
    

#         except OSError: #
#            # handle error
#            print("Could not open FTI checkpoint file " + fn)
#            return FTI_NREC

#         finally:
#             f.close()


#     # f = open('file.txt', 'r')
#     # try:
#     #     # do stuff with f
#     # finally:
#     #     f.close()


#  #    if (FTI_Data->data(&data, FTI_Exec.nbVarStored) != FTI_SCES) {
#  #        FTI_Print("failed to recover", FTI_WARN);
#  #        return FTI_NREC;
#  #    }


#  #    for (i = 0; i < FTI_Exec.nbVarStored; i++) {
#  #        size_t filePos = data[i].filePos;
#  #        // strncpy(data[i].idChar, data[i].idChar, FTI_BUFS);
#  #        fseek(fd, filePos, SEEK_SET);
#  #        fread(data[i].ptr, 1, data[i].sizeStored, fd);
#  #        if (ferror(fd)) {
#  #            FTI_Print("Could not read FTI checkpoint file.", FTI_EROR);
#  #            fclose(fd);
#  #            return FTI_NREC;
#  #        }
#  #    }


#     FTI_Exec.reco = 0

#     return FTI_SCES



# def FTI_Finalize():
#     if FTI_Exec.initSCES == 0 :
#         print("warning")
#         return FTI_NSCS
#     comm.Barrier()

#     if (FTI_Topo.amIaHead) :
#         comm.Barrier()
#         FTI_Data.clear()
#         if not FTI_Conf.keepHeadsAlive :
#             # MPI_Finalize();
#             exit(0)
#         else :
#             return FTI_SCES

#     # application process
#     data = FTIT_dataset()
#     if FTI_Data.data(data, FTI_Exec.nbVar) != FTI_SCES :
#         print("warning")
#         return FTI_NSCS
    

#     if FTI_Exec.wasLastOffline == 1 :
#         lastLevel = 0
#         comm.recv(lastLevel, 1, MPI_INT, FTI_Topo.headRank,
#         FTI_Conf.generalTag, FTI_Exec.globalComm, MPI_STATUS_IGNORE)

#         if lastLevel != FTI_NSCS :                      
#             FTI_Exec.ckptLvel = lastLevel
        
    
#     if FTI_Topo.nbHeads == 1 :
#         value = FTI_ENDW
#         comm.send(value, 1, MPI_INT, FTI_Topo.headRank, FTI_Conf.finalTag,
#          FTI_Exec.globalComm)

#     if FTI_Topo.splitRank == 0 : 
#         FTI_UpdateConf(FTI_Conf, FTI_Exec, 0)
        
#     # Cleaning everything
#     FTI_Clean(FTI_Conf, FTI_Topo, FTI_Ckpt, 5)

#     FTI_FreeTypesAndGroups(FTI_Exec)

#     FTI_Data.clear()
#     comm.Barrier()
#     print("FTI is finalized")
#     return FTI_SCES
        

def FTI_InitType_opaque(size):
    new_id = FTI_Exec.datatypes.ntypes
    dtype = FTIT_Datatype()
    if not size :
        print("Types must have positive size")
        return FTI_NSCS

    if new_id >= TYPES_MAX :
        print("Maximum number of datatypes reached")
        return FTI_NSCS

    # Type initialization
    dtype = FTI_Exec.datatypes.types[new_id]
    dtype.id = new_id
    dtype.size = size
    dtype.structure = None

    FTI_Exec.datatypes.ntypes = FTI_Exec.datatypes.ntypes + 1
    return dtype.id

    