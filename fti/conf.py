import os
import sys
import configparser
from fti import *

def FTI_ReadConf(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt,
        FTI_Inje):
	print("Reading configuration file.." + FTI_Conf.cfgFile)
    if os.path.isfile(FTI_Conf.cfgFile) is False:
        print("Configuration file not found")
        sys.exit(2001)
    else:
        config = configparser.ConfigParser()
        config.read(FTI_Conf.cfgFile)
        FTI_Conf.localDir =  None if not config.get('basic', 'ckpt_dir') else config['basic']['ckpt_dir']
        FTI_Conf.glbalDir = None if not config.get('basic', 'glbl_dir') else config['basic']['glbl_dir'] 
        FTI_Conf.metadDir = None if not config.get('basic', 'meta_dir') else config['basic']['meta_dir'] 

        FTI_Ckpt[1].ckptIntv = -1 if not config.get('basic', 'ckpt_l1') else config['basic']['ckpt_l1']
        FTI_Ckpt[2].ckptIntv = -1 if not config.get('basic', 'ckpt_l2') else config['basic']['ckpt_l2'] 
        FTI_Ckpt[3].ckptIntv = -1 if not config.get('basic', 'ckpt_l3') else config['basic']['ckpt_l3']
        FTI_Ckpt[4].ckptIntv = -1 if not config.get('basic', 'ckpt_l4') else config['basic']['ckpt_l4'] 
        FTI_Exec.fastForward = -1 if not config.get('advanced', 'fast_forward') else config['advanced']['fast_forward'] 

        FTI_Ckpt[1].isInline = 1
        FTI_Ckpt[2].isInline = 1 if not config.get('basic', 'inline_l2') else config['basic']['inline_l2']
        FTI_Ckpt[3].isInline = 1 if not config.get('basic', 'inline_l3') else config['basic']['inline_l3']
        FTI_Ckpt[4].isInline = 1 if not config.get('basic', 'inline_l4') else config['basic']['inline_l4']

        FTI_Ckpt[1].ckptCnt  = 1;
	    FTI_Ckpt[2].ckptCnt  = 1;
	    FTI_Ckpt[3].ckptCnt  = 1;
	    FTI_Ckpt[4].ckptCnt  = 1;

	    FTI_Conf.keepHeadsAlive = 0 if not config.get('basic', 'keep_heads_alive') else config['basic']['keep_heads_alive'] 

        if config['basic']['max_var_id'] > FTI_LIMIT_MAX_VAR_ID:
        	print("...error msg...")
      		FTI_Conf.maxVarId = FTI_DEFAULT_MAX_VAR_ID
        else:
        	FTI_Conf.maxVarId = config['basic']['max_var_id'] 

        FTI_Conf.verbosity = -1 if not config.get('basic', 'verbosity') else config['basic']['verbosity']
        FTI_Conf.saveLastCkpt = 0 if not config.get('basic', 'keep_last_ckpt') else config['basic']['keep_last_ckpt']
        FTI_Conf.keepL4Ckpt = 0 if not config.get('basic', 'keep_l4_ckpt') else config['basic']['keep_l4_ckpt']
        FTI_Conf.blockSize = -1 if not config.get('advanced', 'block_size') else config['basic']['keep_l4_ckpt'] * 1024
        FTI_Conf.transferSize = -1 if not config.get('advanced', 'transfer_size') else config['advanced']['transfer_size'] * 1024 * 1024
        FTI_Conf.ckptTag = 711 if not config.get('advanced', 'ckpt_tag') else config['advanced']['ckpt_tag']
        FTI_Conf.stageTag = 406 if not config.get('advanced', 'stage_tag') else config['advanced']['stage_tag']
        FTI_Conf.finalTag = 3107 if not config.get('advanced', 'final_tag') else config['advanced']['final_tag']
        FTI_Conf.generalTag = 2612 if not config.get('advanced', 'general_tag') else config['advanced']['general_tag']

        FTI_Conf.test = -1 if not config.get('advanced', 'local_test') else config['advanced']['local_test']
        FTI_Conf.ioMode = 0 if not config.get('basic', 'ckpt_io') else config['basic']['ckpt_io'] + 1000

    	FTI_Conf->l3WordSize = FTI_WORD

    	# Reading/setting execution metadata
    	FTI_Exec.nbVar = 0;
	    FTI_Exec.minuteCnt = 0;
	    FTI_Exec.ckptCnt = 1;
	    FTI_Exec.ckptIcnt = 0;
	    FTI_Exec.ckptId = 0;
	    FTI_Exec.ckptLvel = 0;
	    FTI_Exec.ckptIntv = 1;
	    FTI_Exec.wasLastOffline = 0;
	    FTI_Exec.ckptNext = 0;
	    FTI_Exec.ckptLast = 0;
	    FTI_Exec.syncIter = 1;

	    FTI_Exec.syncIterMax = -1 if not config.get('basic', 'max_sync_intv') else config['basic']['max_sync_intv']
	    FTI_Exec.lastIterTime = 0;
    	FTI_Exec.totalIterTime = 0;
    	FTI_Exec.meanIterTime = 0;
    
    	FTI_Exec.reco = 0 if not config.get('restart', 'failure') else config['restart']['failure']

    	# Reading/setting topology metadata
	    FTI_Topo.nbHeads = 0 if not config.get('basic', 'head') else config['basic']['head']
	    FTI_Topo.groupSize = -1 if not config.get('basic', 'group_size') else config['basic']['group_size']
	    FTI_Topo.nodeSize = -1 if not config.get('basic', 'node_size') else config['basic']['node_size'] 
	    FTI_Topo.nbApprocs = FTI_Topo.nodeSize - FTI_Topo.nbHeads;
	    FTI_Topo.nbNodes = FTI_Topo.nbProc / FTI_Topo.nodeSize if (FTI_Topo.nodeSize) else 0


	    # Reading/setting injection parameters
	    FTI_Inje.rank = 0 if config.get('injection', 'rank') else config['injection']['head']
	    FTI_Inje.index = 0 if config.get('injection', 'index') else config['injection']['index']
	    FTI_Inje.position = 0 if config.get('injection', 'position') else config['injection']['position']
	    FTI_Inje.number = 0 if config.get('injection', 'number') else config['injection']['number']
	    FTI_Inje.frequency = -1 if config.get('injection', 'frequency') else config['injection']['frequency']

	    # Barrier
	    comm.Barrier()

	    # return FTI_SCES
	    return FTI_SCES


#def FTI_TestConfig():


def FTI_TestDirectories(FTI_Conf, FTI_Topo):
	print("checking the local dir ..." + FTI_Conf.localDir)
	os.makedirs(FTI_Conf.localDir, mode=0777)

	if FTI_Topo.myRank == 0:
		# Checking metadata directory
		print("Checking the metadata directory " + FTI_Conf.metadDir)
		os.makedirs(FTI_Conf.metadDir, mode=0777)

		# Checking global directory
		print("Checking the metadata directory " + FTI_Conf.glbalDir)
		os.makedirs(FTI_Conf.glbalDir, mode=0777)
	# Barrier
    comm.Barrier()

    # return FTI_SCES
    return FTI_SCES

def FTI_CreateDirs(FTI_Conf, FTI_Exec,
        FTI_Topo, FTI_Ckpt):
	fn = FTI_Conf.metadDir+'/'+FTI_Exec.id
	FTI_Conf.metadDir = fn
	FTI_Conf.mTmpDir = fn+'/tmp'
	FTI_Ckpt[1].metaDir = fn+'/l1'
	FTI_Ckpt[2].metaDir = fn+'/l2'
	FTI_Ckpt[3].metaDir = fn+'/l3'
	FTI_Ckpt[4].metaDir = fn+'/l4'
	FTI_Ckpt[4].archMeta = fn+'/l4_archive'


	# Create global checkpoint timestamp directory

	# fn = FTI_Conf.glbalDir
	FTI_Conf.glbalDir = FTI_Conf.glbalDir+'/'+FTI_Exec.id
	os.makedirs(FTI_Conf.glbalDir, mode=0777)
    FTI_Conf.gTmpDir = FTI_Conf.glbalDir + '/tmp'
    FTI_Ckpt[4].dir = FTI_Conf->glbalDir + '/l4'
    FTI_Ckpt[4].archDir = FTI_Conf->glbalDir + '/l4_archive'



    if (FTI_Conf.keepL4Ckpt) :
    	os.makedirs(FTI_Ckpt[4].archDir, mode=0777)
    	os.makedirs(FTI_Ckpt[4].archMeta, mode=0777)
    
    if (FTI_Conf.test) :
    	fn = FTI_Conf.localDir + '/node' + str(FTI_Topo.myRank / FTI_Topo.nodeSize)
    	os.makedirs(fn, mode=0777)
    else:
    	fn = FTI_Conf.localDir

    FTI_Conf.localDir = fn + '/' + FTI_Exec.id
    os.makedirs(FTI_Conf.localDir, mode=0777)

    FTI_Conf.lTmpDir = FTI_Conf.localDir +'/tmp'
    FTI_Ckpt[1].dir = FTI_Conf.localDir + '/l1'
    FTI_Ckpt[2].dir = FTI_Conf.localDir + '/l2'
    FTI_Ckpt[3].dir = FTI_Conf.localDir + '/l3'
    FTI_Ckpt[4].L4Replica = FTI_Conf.localDir + '/lL4Dir'

    return FTI_SCES;


def FTI_TestConfig(FTI_Conf, FTI_Topo,
        FTI_Ckpt, FTI_Exec):
	if FTI_Topo.nbHeads != 0 and FTI_Topo.nbHeads != 1:
		print("warning")
		return FTI_NSCS
	if FTI_Topo.nbProc % FTI_Topo.nodeSize != 0:
		print("warning")
		return FTI_NSCS
	if FTI_Topo.nbNodes % FTI_Topo.groupSize != 0:
		print("warning")
		return FTI_NSCS

	# Check if Reed-Salomon and L2 checkpointing is requested.
	L2req = 1 if FTI_Ckpt[2].ckptIntv > 0 else 0
	RSreq = 1 if FTI_Ckpt[3].ckptIntv > 0 else 0
	if FTI_Topo.groupSize < 2 and (L2req or RSreq):
		print("warning")
		return FTI_NSCS

	if FTI_Topo.groupSize >= 32 and RSreq:
		print("warning")
		return FTI_NSCS

	if FTI_Conf.verbosity > 3 or FTI_Conf.verbosity < 1:
		print("warning")
		return FTI_NSCS

	if FTI_Conf.blockSize > (2048 * 1024) or FTI_Conf.blockSize < (1 * 1024):
		print("warning")
		return FTI_NSCS

	if FTI_Conf.keepHeadsAlive and FTI_Topo.nbHeads == 0:
		print("warning")
		return FTI_NSCS

	if FTI_Exec.fastForward < 1 or FTI_Exec.fastForward > 10:
		print("warning")
		return FTI_NSCS

	if FTI_Exec.fastForward < 10 and FTI_Exec.fastForward > 1:
		print("warning")

	if FTI_Conf.transferSize > (1024 * 1024 * 64) or FTI_Conf.transferSize < (1024 * 1024 * 8):
		print("warning")
		FTI_Conf.transferSize = 16 * 1024 * 1024

	if FTI_Conf.test != 0 and FTI_Conf.test != 1:
		print("warning")
		return FTI_NSCS

	if FTI_Conf.saveLastCkpt != 0 && FTI_Conf.saveLastCkpt != 1:
		print("warning")
		return FTI_NSCS

	for i in range(1,5):
		if FTI_Ckpt[i].ckptIntv == 0:
			FTI_Ckpt[i].ckptIntv = -1
		if FTI_Ckpt[i].isInline != 0 and FTI_Ckpt[i].isInline != 1:
            FTI_Ckpt[i].isInline = 1;
        
        if FTI_Ckpt[i].isInline == 0 and FTI_Topo.nbHeads != 1:
            print("warning")
            return FTI_NSCS;

    if FTI_Conf.ioMode == FTI_IO_POSIX:
    	print("selected posix")
    elif FTI_Conf.ioMode == FTI_IO_IME:
    	print("selected ime")
    elif FTI_Conf.ioMode == FTI_IO_MPI:
    	print("selected mpi io")
    elif FTI_Conf.ioMode == FTI_IO_FTIFF:
    	print("selected ftiff")
    elif FTI_Conf.ioMode == FTI_IO_HDF5:
    	print("selected hdf5")
    else:
    	FTI_Conf.ioMode = FTI_IO_POSIX
    	print("posix default")

    # check variate processor restart settings
    if FTI_Exec.reco == 3:
    	if FTI_Conf.ioMode != FTI_IO_HDF5:
    		print("warning")
    		FTI_Exec.reco = 0

    return FTI_SCES


def FTI_LoadConf(FTI_Conf, FTI_Exec,
        FTI_Topo, FTI_Ckpt, FTI_Inje):
	if FTI_ReadConf(FTI_Conf, FTI_Exec, FTI_Topo, FTI_Ckpt, FTI_Inje) == FTI_NSCS:
		return FTI_NSCS

	if FTI_TestConfig(FTI_Conf, FTI_Topo, FTI_Ckpt, FTI_Exec) == FTI_NSCS:
		return FTI_NSCS

	if FTI_TestDirectories(FTI_Conf, FTI_Topo) == FTI_NSCS:
		return FTI_NSCS

	if FTI_CreateDirs(FTI_Conf, FTI_Topo) == FTI_NSCS:
		return FTI_NSCS

	return FTI_SCES