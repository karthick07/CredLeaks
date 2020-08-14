
import os
import re
import json


words = [r'java\b',r'php\b',r'python\b','boolean',r'bool\b',r'byte\b',r'char\b',r'float\b',r'int\b', r'object\b'
         r'void\b',r'struct\b',r'namespace\b',r'class\b',r'function\b',r'static\b',r'var\b',r'printf\b',r'package\b'
         r'implements\b',r'override\b',r'#define\b',r'#include\b',r'def\b',r'declare\b',r'lambda\b',r'switch\b',r'null\b'
         r'javascript\b',r'import\b',r'config\b',r'error\b',r'print\b',r'err\b',r'script\b',r'echo\b']

rx = re.compile('|'.join(words), flags=re.I)
fpath = os.path.abspath(os.path.curdir)


for root, dirs, files in os.walk(fpath):
    for filename in files:
        if not filename.endswith('.py'):
            with open(fpath+'/'+filename, 'rb') as file:
                #data = file.read(4096)
                data = json.load(file)

            for match in rx.finditer(str(data['raw_paste'])):
                #os.remove(fpath+filename)
                print("keyword based hits:"+filename)
                break

