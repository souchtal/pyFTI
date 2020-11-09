import socket

def FTI_Topology(FTI_Conf, FTI_Exec,
        FTI_Topo):
	nameList = [None] * FTI_Topo.nbNodes
	nodeList = [None] * FTI_Topo.nbNodes * FTI_Topo.nodeSize
	# have to specify the sizes of the arrays
	#for (i = 0; i < FTI_Topo->nbProc; i++) :
	for i in range(FTI_Topo.nbProc):
        nodeList[i] = -1
    
    res = FTI_BuildNodeList(FTI_Conf, FTI_Exec, FTI_Topo, nodeList,
     nameList)
    if (res == FTI_NSCS) :
        # del nameList);
        # del nodeList);
        del nameList
        del nodeList

        return FTI_NSCS

    if FTI_Exec.reco == 1 or FTI_Exec.reco == 2 :
    	res = FTI_ReorderNodes(FTI_Conf, FTI_Topo, nodeList, nameList)
    	if (res == FTI_NSCS) :
	        del nameList
	        del nodeList
        	return FTI_NSCS

    FTI_Exec.globalComm.Barrier()

    if (FTI_Topo.myRank == 0 and ((FTI_Exec.reco == 0) or \
     (FTI_Exec.reco == 3))) :
        res = FTI_SaveTopo(FTI_Conf, FTI_Topo, nameList)
        if (res == FTI_NSCS) :
            del nameList
	        del nodeList

            return FTI_NSCS
        
    distProcList = [None] * FTI_Topo.nbNodes
    userProcList = [None] * (FTI_Topo.nbProc - (FTI_Topo.nbNodes * FTI_Topo.nbHeads))
    
    mypos = -1
    c = 0

    # for (i = 0; i < FTI_Topo->nbProc; i++) :
    for i in range(FTI_Topo.nbProc): 
        if (FTI_Topo.myRank == nodeList[i]) :
            mypos = i
        
        if ((i % FTI_Topo.nodeSize != 0) or (FTI_Topo.nbHeads == 0)) :
            userProcList[c] = nodeList[i]
            c = c + 1
        
   
    if (mypos == -1) :
        del userProcList
        del distProcList
        del nameList
        del nodeList

        return FTI_NSCS
    
    FTI_Topo.nodeRank = mypos % FTI_Topo.nodeSize
    if (FTI_Topo.nodeRank == 0 and FTI_Topo.nbHeads == 1) :
        FTI_Topo.amIaHead = 1
    else :
        FTI_Topo.amIaHead = 0
    
    FTI_Topo.nodeID = mypos / FTI_Topo.nodeSize
    FTI_Topo.headRank = nodeList[(mypos / FTI_Topo.nodeSize) *
     FTI_Topo.nodeSize]
    FTI_Topo.sectorID = FTI_Topo.nodeID / FTI_Topo.ggroupSize
    posInNode = mypos % FTI_Topo.nodeSize
    FTI_Topo.groupID = posInNode

    # for (i = 0; i < FTI_Topo->nbNodes; i++) :
    for i in range(FTI_Topo.nbNodes):
        distProcList[i] = nodeList[(FTI_Topo.nodeSize * i) + posInNode]
    
    res = FTI_CreateComms(FTI_Conf, FTI_Exec, FTI_Topo, userProcList,
     distProcList, nodeList)

    if (res == FTI_NSCS) :
        del userProcList
        del distProcList
        del nameList
        del nodeList

        return FTI_NSCS
    
    del userProcList
    del distProcList
    del nameList
    del nodeList

    return FTI_SCES



def FTI_BuildNodeList(FTI_Conf, FTI_Exec,
        FTI_Topo, nodeList, nameList):
	lhn = [None] * FTI_Topo.nbProc

	if not FTI_Conf.test :
        # NOT local test
        #gethostname(lhn + (FTI_Topo->myRank * FTI_BUFS), FTI_BUFS);
        lhn + FTI_Topo.myRank = socket.gethostname()

    else :
        #snprintf(lhn + (FTI_Topo->myRank * FTI_BUFS), FTI_BUFS, "node%d",
        # FTI_Topo->myRank / FTI_Topo->nodeSize);  
        lhn + FTI_Topo.myRank = "node"+str(FTI_Topo.myRank / FTI_Topo.nodeSize)

    hname = []
    #strncpy(hname, lhn + (FTI_Topo->myRank * FTI_BUFS), FTI_BUFS - 1);
    hname[0] = lhn + FTI_Topo.myRank
    FTI_Exec.globalComm.allgather(hname)

    for i in range(FTI_Topo.nbProcs):
    	hname = lhn + i
    	found = 0
    	pos = 0

    	while (pos < nbNodes) and (found == 0) :
    		if nameList[pos] == hname :
    			found = 1
    		else:
    			pos = pos + 1

    	if found :
    		p = pos * FTI_Topo.nodeSize
    		while p < pos * FTI_Topo.nodeSize + FTI_Topo.nodeSize :
    			if nodeList[p] == -1 :
                    nodeList[p] = i
                    break
                else :
                    p = p + 1
                
        else:
        	nameList[pos] = hname
        	nodeList[pos * FTI_Topo.nodeSize] = i
        	nbNodes = nbNodes + 1

	for i in range(FTI_Topo.nbProc) :
		if nodeList[i] == -1 :
            print("Node "+str(i / FTI_Topo.nodeSize)+ \
            	" has no "+str(FTI_Topo.nodeSize)+" processes")
            del lhn
            return FTI_NSCS
        
    del lhn
    return FTI_SCES



def FTI_ReorderNodes(FTI_Conf, FTI_Topo,
        nodeList, nameList):
	print("TODO")
	nl = [None] * FTI_Topo.nbProc
	old = [None] * FTI_Topo.nbNodes
	new = [None] * FTI_Topo.nbNodes

	for i in range(FTI_Topo.nbNodes):
		old[i] = -1
        new[i] = -1
	
    mfn = FTI_Conf.metadDir + '//Topology.fti'
    print("Loading FTI topology file " + mfn + " to reorder nodes...")

    if not os.access(mfn, os.R_OK):
    	print("Topo not accessible")
    	del nl
    	del old
    	del new

    	return FTI_NSCS

  	# Get the old order of nodes
  	for i in range(FTI_Topo.nbNodes):
  		# configparser
  		config = configparser.ConfigParser()
        config.read(mfn)
        # config['basic']['ckpt_dir']
  		string = "Topology:"+str(i)
  		tmp = config[string]
  		string = tmp

  		for j in range(FTI_Topo.nbNodes):
  			string2 = nameList + (j * FTI_BUFS)
  			if string[0:FTI_BUFS] == string2[0:FTI_BUFS]:
  				old[j] = i
                new[i] = j
                break

        j = 0
        for i in range(FTI_Topo.nbNodes):
        	if (new[i] == -1) :
            # search for an old node not present in the new list..
	            while (old[j] != -1) :
	                j = j + 1
	            
	            # and set matching IDs
	            old[j] = i
	            new[i] = j
	            j = j + 1
        
        for i in range(FTI_Topo.nbProc):
        	nl[i] = nodeList[i]

      	for i in range(FTI_Topo.nbNodes):
      		for j in range(FTI_Topo.nodeSize):
      			nodeList[(i * FTI_Topo.nodeSize) + j] = nl[(new[i] * FTI_Topo.nodeSize) + j]

      	del nl
      	del old
      	del new

      	return FTI_SCES

def FTI_SaveTopo(FTI_Conf, FTI_Topo,
 	nameList):
	print("Trying to load configuration file "+FTI_Conf.cfgFile+" to create topology")
	config = configparser.ConfigParser()
    config.read(FTI_Conf.cfgFile)

    config.add_section('topology')

    for (i = 0; i < FTI_Topo->nbNodes; i++) {
        char mfn[FTI_BUFS];
        strncpy(mfn, nameList + (i * FTI_BUFS), FTI_BUFS - 1);
        snprintf(str, FTI_BUFS, "topology:%d", i);
        iniparser_set(ini, str, mfn);
    

	return FTI_SCES


def FTI_CreateComms(FTI_Conf, FTI_Exec,
        FTI_Topo, userProcList,
        distProcList, nodeList):

	origGroup = FTI_Exec.globalComm.Get_group()
	if FTI_Topo.amIaHead :
		# MPI_Group_incl(origGroup, FTI_Topo->nbNodes * FTI_Topo->nbHeads,
  		# distProcList, &newGroup);
  		FTI_Exec.globalComm.Create_group()

  		# MPI_Comm_create(FTI_Exec->globalComm, newGroup, &FTI_COMM_WORLD);
  		FTI_Exec.globalComm.Create(newGroup, FTI_COMM_WORLD)

  		for i in range(FTI_Topo.nbHeads, FTI_Topo.nodeSize) :
  			src = nodeList[(FTI_Topo.nodeID * FTI_Topo.nodeSize) + i]
  			# FTI_Exec.globalComm.recv(buf, )

  	else : 
  		# MPI_Group_incl
  		FTI_Exec.globalComm.Create(newGroup, FTI_COMM_WORLD)
  		if FTI_Topo.nbHeads == 1 :
            # MPI_Send(&(FTI_Topo->myRank), 1, MPI_INT, FTI_Topo->headRank,
            #  FTI_Conf->generalTag, FTI_Exec->globalComm);
        	# FTI_Exec.globalComm.send(buf, )

    FTI_Topo.splitRank = FTI_COMM_WORLD.Get_rank()
    buf = FTI_Topo.sectorID * FTI_Topo.groupSize
    group = []

    for i in range(FTI_Topo.groupSize) :
    	group[i] = distProcList[buf + i]


    # MPI_Comm_group(FTI_Exec->globalComm, &origGroup);
    # MPI_Group_incl(origGroup, FTI_Topo->groupSize, group, &newGroup);
    # MPI_Comm_create(FTI_Exec->globalComm, newGroup, &FTI_Exec->groupComm);
    # MPI_Group_rank(newGroup, &(FTI_Topo->groupRank));
    # FTI_Topo->right = (FTI_Topo->groupRank + 1) % FTI_Topo->groupSize;
    # FTI_Topo->left = (FTI_Topo->groupRank + FTI_Topo->groupSize - 1) %
    #  FTI_Topo->groupSize;
    # MPI_Group_free(&origGroup);
    # MPI_Group_free(&newGroup);


    origGroup = FTI_Exec.globalComm.Get_group()
    # MPI_Group_incl
    FTI_Exec.globalComm.Create(newGroup, FTI_Exec.groupComm)
    # MPI_Group_rank
    FTI_Topo.right = (FTI_Topo.groupRank + 1) % FTI_Topo.groupSize
    FTI_Topo.left = (FTI_Topo.groupRank + FTI_Topo.groupSize - 1) % \
     FTI_Topo.groupSize

    # MPI_Group_free(&origGroup);
    # MPI_Group_free(&newGroup);

	return FTI_SCES


