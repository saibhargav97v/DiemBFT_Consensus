# DiemBFT_Consensus
DiemBFT v4 Consensus Algorithm implementation in DistAlgo and Python.


# Platform :
* Python: Python 3.7.11   
* Package manager : Miniconda.   
* DistAlgo : Cloned from https://github.com/DistAlgo/distalgo.git and ran setup.py 
	* Version : pyDistAlgo==1.1.0b15  
* Operating system Productname : macOS	  
	* OS ProductVersion: 11.5.2	  
	* OS BuildVersion:   20G95		  
* Type of Host : Personal Laptop	  
	
# Workload generation : 
* src/run.da instantiates Runner processes which are config driven and spawns the clients and validators 
* Configs are read from src/config.da   
* Da files for client and validator are client.da and validator.da respectively.  
* Multiple client processes send transactions asynchronously like "transactions_C0_1" where C0 is the ClientID 
		and 1 indicates it's message number (txn_id or the sequence number is presented using ClientID_MessageNumber)   
* Each client waits for f + 1 commit acknowledgements for each of it's transactions 
		where f is the number of faulty nodes in the system. 
* Once it receives f + 1 commit acks, it sends a 'done' message to it's parent 
		which is the **Run** class that instantiated it. 
* ledger.da, pacemaker.da, leaderelection.da, safety.da, mempool.da, blocktree.py 
		modules implementations are in separate files. 
	
# Timeouts :
* Client timeout : Different choice for different configs. Varies from 8 - 100 secs.
* Validator timeout : Choice of function is 4 * Delta where Delta is 2 secs.

# Bugs and Limitations :
* Clients keep collecting acknowledgements from all validators and terminates once it receives sufficient(f+1) commit acks. 
		If it times out, it retransmits all the transactions to all the validators.
* Sending of 2 dummy transactions by each client to facilitate the commit of last two transactions. 
* Clients not waiting for committed acknowledgements after each transaction. This is due to the fact that for one transaction to commit we need two more dummy / next transactions. So either two dummies are to be sent for each client transaction and receive ack to proceed further. 
Since this might increase the round numbers unnecessarily. We chose to not wait for acks after each transaction. The implementation ensures that the transactions are done in Fifo order.
* Not sending hashes with client acknowledgements (Just sending the signed messages to verify)
* Unsure about the implementation of Merkle tree
* Using only Round Robin for leader election and not using reputation leaders

# Main files :
* Client source : DiemBFT_Consensus/src/client.da
* Validator source : DiemBFT_Consensus/src/validator.da and DiemBFT_Consensus/src/validator_fi.da (Fault Injected validator)

# Code size :
* Numbers of non-blank non-comment lines of code (LOC) : 907
* Obtained from : git ls-files | xargs cat | grep -v ^$ | wc -l
* Percentage lines for just the algorithm : 79% (907-182/907)

# Language feature usage :
 * Python list comprehension : 4 across files
 * Python dictionary comprehension : 2 across files
 * Python set comprehension : 4 across files
 * DistAlgo quantifications : 2 await(each()) quantifications used in run.da
 * DistAlgo await statements : 5 await statements
 * Number of receive handlers : 3 Receive handlers used overall. 2 in validator.da and 1 in client.da
