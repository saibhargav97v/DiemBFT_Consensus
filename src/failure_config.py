from collections import namedtuple 
FailureConfig = namedtuple('FailureConfig', ['failures', 'seed'], defaults=(None)) 

Failure = namedtuple('Failure', ['src', 'dest', 'msg_type', 'round', 'prob', 'fail_type', 'val', 'attr'],
defaults=(None,None)) 