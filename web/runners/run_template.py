import shlex
import time
import json
import subprocess

from .languages_map import languages_map


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
    process = subprocess.Popen(
        [shlex.split(languages_map[language][command])],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = process.communicate(timeout=90)
    dict[command + '-out'] = out
    dict[command + '-err'] = err
    dict[command + '-retcode'] = process.returncode

def start(language):
    data = {}
    checkFilesArePresent(language)

    if languages_map[language]['compilable']:
        execute(data, language, 'compile')
        if data['compiler-retcode'] == 0:
            execute(data, language, 'run')
    else:
        execute(data, language, 'run')

    print(json.dumps(data))
