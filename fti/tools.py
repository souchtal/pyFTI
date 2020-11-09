import os
import shutil
from fti import *


def FTI_RmDir(path, flag):
    if flag :
        print("removing dir and its files " + path)
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print("deleted file:" + file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    shutil.rmtree(path, ignore_errors=True)
    print("deleted directory:" + path)

    return FTI_SCES

def FTI_Clean(FTI_Conf, FTI_Topo,
         FTI_Ckpt, level):

    globalFlag = not FTI_Topo.splitRank

    nodeFlag = 1 if (((not FTI_Topo.amIaHead) and ((FTI_Topo.nodeRank - FTI_Topo.nbHeads) == 0)) or (FTI_Topo.amIaHead)) else 0


    if (level == 0) :
        FTI_RmDir(FTI_Conf.mTmpDir, globalFlag and notDcpFtiff)
        FTI_RmDir(FTI_Conf.gTmpDir, globalFlag and notDcp)
        FTI_RmDir(FTI_Conf.lTmpDir, nodeFlag and notDcp)
    

    # Clean last checkpoint level 1
    if (level >= 1) :
        FTI_RmDir(FTI_Ckpt[1].metaDir, globalFlag and notDcpFtiff)
        FTI_RmDir(FTI_Ckpt[1].dir, nodeFlag and notDcp)
    

    # Clean last checkpoint level 2
    if (level >= 2) :
        FTI_RmDir(FTI_Ckpt[2].metaDir, globalFlag and notDcpFtiff)
        FTI_RmDir(FTI_Ckpt[2].dir, nodeFlag and notDcp)
    

    # Clean last checkpoint level 3
    if (level >= 3) :
        FTI_RmDir(FTI_Ckpt[3].metaDir, globalFlag and notDcpFtiff)
        FTI_RmDir(FTI_Ckpt[3].dir, nodeFlag and notDcp)
    

    # Clean last checkpoint level 4
    if (level == 4 or level == 5) :
        FTI_RmDir(FTI_Ckpt[4].metaDir, globalFlag and notDcpFtiff)
        FTI_RmDir(FTI_Ckpt[4].dir, globalFlag and notDcp)
        FTI_RmDir(FTI_Ckpt[4].L4Replica, nodeFlag)
        # rmdir(FTI_Conf.gTmpDir)
        shutil.rmtree(FTI_Conf.gTmpDir, ignore_errors=True)
    
    if ((FTI_Conf.dcpPosix or FTI_Conf.dcpFtiff) and level == 5) :
        FTI_RmDir(FTI_Ckpt[4].dcpDir, not FTI_Topo.splitRank);
    

    # If it is the very last cleaning and we DO NOT keep the last checkpoint
    if (level == 5) :
        # rmdir(FTI_Conf.lTmpDir)
        # rmdir(FTI_Conf.localDir)
        # rmdir(FTI_Conf.glbalDir)
        shutil.rmtree(FTI_Conf.lTmpDir, ignore_errors=True)
        shutil.rmtree(FTI_Conf.localDir, ignore_errors=True)
        shutil.rmtree(FTI_Conf.glbalDir, ignore_errors=True)

        buf = FTI_Conf.metadDir + '/Topology.fti'
        os.unlink(buf)

        buf = FTI_Conf.metadDir + '/Checkpoint.fti'
        os.unlink(buf)

        shutil.rmtree(FTI_Conf.metadDir, ignore_errors=True)

    # If it is the very last cleaning and we DO keep the last checkpoint
    if (level == 6) :
        shutil.rmtree(FTI_Conf.lTmpDir, ignore_errors=True)
        shutil.rmtree(FTI_Conf.localDir, ignore_errors=True)
    
    return FTI_SCES

def FTI_FreeTypesAndGroups(FTI_Exec):
    # memset(&FTI_Exec->datatypes, 0, sizeof(FTIT_DataTypes));
    FTI_Exec.datatypes = None


def FTI_InitExecVars(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt, FTI_Inje):
    # set all to 0
    # set all the class objects to 0 along with their attributes 
    # esp FTI_Exec.id
    FTI_Exec.id = 0
    FTI_Exec.reco = 0



def FTI_InitGroupsAndTypes(FTI_Exec):
    FTI_Exec.datatypes = 0


    FTI_Exec.nbGroup = 1

    # TRY_ALLOC(FTI_Exec->datatypes.types, FTIT_Datatype, TYPES_MAX) :

    FTI_Exec.datatypes.types = [None] * TYPES_MAX
    for i in range(TYPES_MAX) :
        FTI_Exec.datatypes.types[i] = FTIT_Datatype()
    

    FTI_CHAR = FTI_InitType_opaque(sizeof(char));
    FTI_SHRT = FTI_InitType_opaque(sizeof(short));
    FTI_INTG = FTI_InitType_opaque(sizeof(int));
    FTI_LONG = FTI_InitType_opaque(sizeof(long));
    FTI_UCHR = FTI_InitType_opaque(sizeof(unsigned char));
    FTI_USHT = FTI_InitType_opaque(sizeof(unsigned short));
    FTI_UINT = FTI_InitType_opaque(sizeof(unsigned int));
    FTI_ULNG = FTI_InitType_opaque(sizeof(unsigned long));
    FTI_SFLT = FTI_InitType_opaque(sizeof(float));
    FTI_DBLE = FTI_InitType_opaque(sizeof(double));
    FTI_LDBE = FTI_InitType_opaque(sizeof(long double));

    FTI_Exec.datatypes.nprimitives = FTI_Exec.datatypes.ntypes

    return FTI_SCES

