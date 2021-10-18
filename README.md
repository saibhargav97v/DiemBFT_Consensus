# DiemBFT_Consensus
DiemBFT v4 Consensus Algorithm implementation in DistAlgo and Python.


# Platform :
	* Python: Python 3.7.11   
	* Package manager : Miniconda.   
	* DistAlgo : Cloned from https://github.com/DistAlgo/distalgo.git and ran setup.py   
	* Operating system Productname : macOS	  
		* OS ProductVersion: 11.5.2	  
		* OS BuildVersion:   20G95		  
	* Type of Host : Personal Laptop	  
	
# Workload generation : 
	* src/main instantiates Runner processes which are config driven and does the setup of clients and validators 
	* Configs are read from config.da   
	* Da files for client and validator are client.da and validator.da respectively.  
	* Multiple client processes send transactions asynchronously like "transactions_C0_1" where C0 is the ClientID and 1 indicates it's message number (txn_id or the sequence number is presented using ClientID_MessageNumber)   
	* Each client waits for f + 1 commit acknowledgements for each of it's transactions 
	where f is the number of faulty nodes in the system. 
	* Once it receives f + 1 commit acks, it sends a 'done' message to it's parent 
	which is the **Run** class that instantiated it. 
	* ledger.da, pacemaker.da, leaderelection.da, safety.da, mempool.da, blocktree.py 
	modules implementations are in separate files. 
	
# Timeouts :
	* Client timeout : Different choice for different configs. Usually 5-6 secs.
	* Validator timeout : Choice of function is 4 * Delta where Delta is 2 secs.

# Bugs and Limitations :
	* Leader election ?
	* Clients keep collecting acknowledgements from all validators and terminates once it receives sufficient(f+1) commit acks. If it times out, it retransmits all the transactions again to all the validators.
	* Sending of 2 dummy transactions by each client to facilitate the commit of last two transactions.  

# Main files :
	* Client source : DiemBFT_Consensus/src/client.da
	* Validator source : DiemBFT_Consensus/src/validator.da and DiemBFT_Consensus/src/validator_fi.da (Fault Injected validator)
	* Workload generation has other modules file location.

# Code size :
	* Numbers of non-blank non-comment lines of code (LOC) :
	* Obtained from : 
	* Percentage lines for just the algorithm : 

# Language feature usage :
 * Python list comprehension : 4 across files
 * Python dictionary comprehension : 2 across files
 * Python set comprehension : 4 across files
 * DistAlgo quantifications : 2 await(each()) quantifications used in run.da
 * DistAlgo await statements : 5 await statements
 * Number of receive handlers : 3 Receive handlers used overall. 2 in validator.da and 1 in client.da

# 
