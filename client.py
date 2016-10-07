from ethereum import utils

# A very simplistic client for both the Host and the Respondent

class QClient:
    def __init__(self, client_id, contract, state):
        self.id = client_id
        self.pub_addr = utils.privtoaddr(client_id)
        self.contract = contract
        self.contr_state = state

    def host(self, q_str, bid):
        return self.contract.host(q_str, value=bid, sender=self.id)

    def vote(self, acli):
        return self.contract.vote(self.pub_addr, acli.pub_addr, sender=self.id)
    
    def reward(self, ):
        return self.contract.reward(self.pub_addr, sender=self.id)

    def print_bal(self, stri):
        print stri, self.contr_state.block.get_balance(self.pub_addr)

class AClient:
    def __init__(self, client_id, contract, state):
        self.id = client_id
        self.pub_addr = utils.privtoaddr(client_id)
        self.contract = contract
        self.contr_state = state

    def join(self, qcli, ans_str, bid):
        return self.contract.join(qcli.pub_addr, ans_str, value=bid, sender=self.id)

    def vote(self, qcli, acli):
        return self.contract.vote(qcli.pub_addr, acli.pub_addr, sender=self.id)

    def reward(self, qcli):
        return self.contract.reward(qcli.pub_addr, sender=self.id)

    def print_bal(self, stri):
        print stri, self.contr_state.block.get_balance(self.pub_addr)