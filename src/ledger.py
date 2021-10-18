import os

class Ledger:
    def __init__(self, modules_map):
        self.modules_map = modules_map
        self.speculated_state = {}
        self.LRU_commited_cache = {}
        self.committed_txn_ids = set()
        self.pending_txn_ids = set()

    def speculate(self,prev_block_id, block_id, txn):
        self.speculated_state[block_id] = {
            "payload": txn,
            "prev_block_id": prev_block_id
        }
        self.pending_txn_ids.add(txn[3])


    def commit(self, id):
        txns = []
        while self.speculated_state.get(id, None) is not None:
            state = self.speculated_state.pop(id)
            if state["payload"] and len(state["payload"]) and state["payload"][0] != "dummy":
                self.LRU_commited_cache[id] = state["payload"]
                txns.insert(0,state["payload"])
            id = state["prev_block_id"]

        for txn in txns:
            self.persist_txn(txn)

    def pending_state(self, block_id):
        return self.speculated_state.get(block_id, None)

    def get_committed_block(block_id):
        return self.LRU_commited_cache.get(block_id, None)

    def persist_txn(self, txn):
        if txn is None:
            return
        if txn[0] == "dummy":
            return
        payload = txn if len(txn) > 0 else None 
        if payload[3] not in self.committed_txn_ids:
            self.committed_txn_ids.add(payload[3])
        if payload[3] in self.pending_txn_ids:
            self.pending_txn_ids.remove(payload[3])

        self.modules_map['latest_committed_payload'] = payload
        payload = str(txn) + "\n"
        file_path = f'../ledgers/{self.modules_map["config"]["config_num"]}/ledger_{str(self.modules_map["config"]["id"])}.txt'
        file = open(file_path, "a+")

        file.write(payload)

        file.flush()
        os.fsync(file.fileno())
        file.close()
