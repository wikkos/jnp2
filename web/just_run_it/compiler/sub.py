class Sub:
    hmm = {
        0 : "RUNNING",
        1 : "EXECUTED",
        2 : "FAILED",
    }

    def __init__(self, map):
        self.id = map['id']
        self.language = map['language']
        self.timeExecuted = map['timeExecuted']
        self.status = self.hmm[map['status']]