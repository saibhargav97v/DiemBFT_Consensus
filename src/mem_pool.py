from collections import deque
import logging

class MemPool:
    def __init__(self, modules) -> None:
        self.modules = modules
        self.commands = []

    def add_command_to_mempool(self, client_command):

        # Handling deduplicates by checking ledger's committed_Txns and Mem_pool 

        txn_id = client_command[3]
        already_received_command = False
        if client_command[0] != "dummy":
            if txn_id in self.modules['ledger'].committed_txn_ids:
                already_received_command = True
 
            if txn_id in self.modules['ledger'].pending_txn_ids:
                already_received_command = True
        
            for item in self.commands:  
                if txn_id in item:
                    already_received_command = True
                    break
        
        if not already_received_command:
            self.commands.append(client_command)
        else:
            logging.info(f"Already Received {client_command} at Validator{self.modules['config']['id']}")

    def is_empty(self):
        return len(self.commands) == 0

    def get_transaction(self):
        if not self.is_empty():
            return self.commands.pop(0)
        return None
    
    def update_mempool(self, payload):
        for item in self.commands:
            if item[0] == payload[0] and item[1] == payload[1] and item[2] == payload[2]:
                self.commands.remove(item)
                break