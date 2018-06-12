from .languages_map import languages_map


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


class Exe:
    def __init__(self, map):
        self.id = map['id']
        self.language = map['language']
        self.timeExecuted = map['timeExecuted']
        if languages_map[map['language']]['compilable']:
            self.compilable = True
            self.compile_out = map['compile-out']
            self.compile_err = map['compile-err']
            self.compile_retcode = map['compile-retcode']
            if self.compile_retcode == 0:
                self.run = True
                self.run_out = map['run-out']
                self.run_err = map['run-err']
                self.run_retcode = map['run-retcode']
            else:
                self.run = False
        else:
            self.compilable = False
            self.run = True
            self.run_out = map['run-out']
            self.run_err = map['run-err']
            self.run_retcode = map['run-retcode']
