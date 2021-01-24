import sys
import inspect
BULLET_FAIL    ="[\033[91m+\033[0m]"
BULLET_SUCCESS ="[\033[92m+\033[0m]"
BULLET_WARN    ="[\033[93m+\033[0m]"
BULLET_INFO    ="[\033[94m+\033[0m]"
BULLET_ALL     ="[\033[34m+\033[0m]"

LOGGING_FAIL=0
LOGGING_SUCC=1
LOGGING_WARN=2
LOGGING_INFO=3
LOGGING_ALL =4

verbosity=0
clamp=100

def pprint(message,level=LOGGING_FAIL):
    if(verbosity>=level):
        _pprint(message,level)

def _pprint(message, level=LOGGING_FAIL):
    if(verbosity>=2):
        frame = inspect.stack()[2]
        frame_info = " \033[93m[" + frame.filename.split('\\')[-1].split('.')[0] + ":" + frame.function + "]\033[0m"
    else:
        frame_info=""

    if(len(message)>clamp):
        message = message[0:clamp-6] + "..."
    elif(verbosity>=2):
        message += "\033[90m" + "_" * (clamp-len(message)) + "\033[0m"
    
    
    if(level==LOGGING_FAIL):
        sys.stderr.write(f"{BULLET_FAIL} {message}{frame_info}\n")
    elif(level==LOGGING_SUCC):
        sys.stdout.write(f"{BULLET_SUCCESS} {message}{frame_info}\n")
    elif(level==LOGGING_WARN):
        sys.stdout.write(f"{BULLET_WARN} {message}{frame_info}\n")
    elif(level==LOGGING_INFO):
        sys.stdout.write(f"{BULLET_INFO} {message}{frame_info}\n")
    else:
        sys.stdout.write(f"{BULLET_ALL} {message}{frame_info}\n")
