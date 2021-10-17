import os

class Ledger:
    def __init__(self, modules_map):
        self.modules_map = modules_map
        self.committed_txns = {}

    def speculate(self, prev_block_id, block_id, txns):
        pass

    def pending_state(self, block_id:int):
        pass

    def commit(self, txn):
        if txn is None:
            return
        if txn[0] == "dummy":
            return
        payload = txn if len(txn) > 0 else None 
        self.committed_txns[payload[3]] = payload
        self.modules_map['latest_committed_payload'] = payload
        payload = str(txn) + "\n"
        file_path = f'../ledgers/{self.modules_map["config"]["config_num"]}/ledger_{str(self.modules_map["config"]["id"])}.txt'
        file = open(file_path, "a+")

        file.write(payload)

        file.flush()
        os.fsync(file.fileno())
        file.close()


    def committed_block(self, block_id:int):
        return 1