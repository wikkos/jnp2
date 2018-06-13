import shlex
import time
import json
import subprocess
import sys


languages_map = {
    'C' : {
        'ext' : '.c',
        'image' : 'jnp2_runner_c',
        'compilable' : True,
        'compile' : 'gcc -std=c11 file.c -o file',
        'run' : './file',
    },
    'CPP17' : {
        'ext' : '.cc',
        'image' : 'jnp2_runner_cpp',
        'compilable' : True,
        'compile' : 'g++ -std=c++17 file.cc -o file',
        'run' : './file',
    },
    'PYTHON3' : {
        'ext' : '.py',
        'image' : 'jnp2_runner_c',
        'compilable' : False,
        'run' : 'python file.py',
    },
}


# not proud of it, but it works
def checkFilesArePresent(language):
    filesArePresent = False
    while not filesArePresent:
        try:
            file = open('file' + languages_map[language]['ext'])
            file.close()
            file = open('input')
            file.close()
            filesArePresent = True
        except:
            time.sleep(3)


def execute(dict, language, command):
    if command == 'run':
        input = open('input')
    else:
        input = None
    process = subprocess.Popen(
        shlex.split(languages_map[language][command]),
        stdin=input,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if command == 'run':
        input.flush()
        input.close()
    out, err = process.communicate(timeout=90)
    dict[command + '-out'] = out.decode('utf-8')
    dict[command + '-err'] = err.decode('utf-8')
    dict[command + '-retcode'] = process.returncode


def start(language):
    data = {}
    checkFilesArePresent(language)

    if languages_map[language]['compilable']:
        execute(data, language, 'compile')
        if data['compile-retcode'] == 0:
            execute(data, language, 'run')
        else:
            data['run-out'] = ""
            data['run-out'] = ""
            data['run-retcode'] = -1
    else:
        execute(data, language, 'run')

    print(json.dumps(data))


start(sys.argv[1])
