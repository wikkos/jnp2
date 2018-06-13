languages_map = {
    'C' : {
        'ext' : '.c',
        'image' : 'jnp2_runner_c',
        'compilable' : True,
        'compile' : 'gcc -std=c11 file.c -o file',
        'run' : './file <input',
    },
    'CPP17' : {
        'ext' : '.cc',
        'image' : 'jnp2_runner_cpp',
        'compilable' : True,
        'compile' : 'g++ -std=c++17 file.cc -o file',
        'run' : './file <input',
    },
    'PYTHON3' : {
        'ext' : '.py',
        'image' : 'jnp2_runner_c',
        'compilable' : False,
        'run' : 'python file.py',
    },
}
