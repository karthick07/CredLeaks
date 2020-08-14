__author__ = "Karthick Thambidurai"
__status__ = "Prototype"
from subprocess import call
import time
import os
import re
import json
import processPastes


# Currently the output format in pastehunter is set to json hence the path is pointed to the respective directory
dpath = os.path.abspath(os.path.curdir) + '/temp'
os.chdir(dpath)

#The keywords used to filter files by MIME types and generic source code terms can be updated as per the requirements.
try:
    # Invoking a shell command that searches for common MIME types and removes corresponding pastes from output ('json') directory
    call('''
    find -type f -exec bash -c '
      for f; do
        file=$(file -- "$f")
        if [[ $file =~ ^$f:\ ("C source"|"Python script"|"python source"|"node script"|"shell script"|\
        "swift script"|"Algol 68 source"|"assembler source"|"perl script"|"Bourne-Again shell script"|
        "C++ source"|"core file"|"DCL command file"|"DOS batch file"|"exported SGML"|"Java source"|
        "diff output"|"GIF image data"|"Lisp"|"Lua bytecode"|"makefile script"|"MGR bitmap"|\
        "Objective-C source"|"Pascal source"|"Perl5"|"PGP message"|"PHP script|"POSIX shell script|\
        "Ruby script"|"SMTP mail"|"Windows Registry text"|"XML 1.0") ]]; then
             rm -- "$f"
        fi
      done
    ' bash {} +
    ''', shell=True)
    time.sleep(1)

    # Remove files in the output directory if it matches common source code keywords listed below
    words = [r'(?<!\S)java+(?!\S)', r'php\b', r'(?<!\S)python+(?!\S)', r'(?<!\S)boolean+(?!\S)', r'xml\b',
             r'(?<!\S)bool+(?!\S)', r'(?<!\S)byte+(?!\S)', r'(?<!\S)char+(?!\S)', r'(?<!\S)float+(?!\S)',
             r'(?<!\S)int+(?!\S)', r'(?<!\S)object+(?!\S)', r'(?<!\S)void+(?!\S)', r'(?<!\S)struct+(?!\S)',
             r'(?<!\S)namespace+(?!\S)', r'(?<!\S)class+(?!\S)', r'(?<!\S)function+(?!\S)', r'(?<!\S)static+(?!\S)',
             r'(?<!\S)var+(?!\S)', r'(?<!\S)printf+(?!\S)', r'(?<!\S)package+(?!\S)', r'(?<!\S)implements+(?!\S)',
             r'(?<!\S)override+(?!\S)', r'(?<!\S)#define+(?!\S)', r'(?<!\S)#include+(?!\S)', r'(?<!\S)def+(?!\S)',
             r'(?<!\S)declare+(?!\S)',
             r'(?<!\S)lambda+(?!\S)', r'null\b', r'(?<!\S)javascript+(?!\S)', r'logger\b',
             r'(?<!\S)import+(?!\S)', r'(?<!\S)config+(?!\S)', r'(?i)error\b', r'print\b', r'(?<!\S)echo+(?!\S)']

    rx = re.compile('|'.join(words), flags=re.I)
    fpath = os.path.abspath(os.path.curdir)

    for root, dirs, files in os.walk(fpath):
        for filename in files:
            if not filename.endswith('.py'):
                with open(fpath + '/' + filename, 'rb') as file:
                    data = json.load(file)

                for match in rx.finditer(str(data['raw_paste'])):
                    os.remove(fpath + '/' + filename)
                    break


except Exception as e:
    print("Exception occured in prefilter " +e.message)

#In certain cases all the files in the output directory may be source code files and are removed.
#In those scenarios a check is made to see if the directory is empty and if empty the rest of the process is not carried out
dir_contents = os.listdir('.')
if dir_contents:
    processPastes.process()
    processPastes.predict_pii()
else:
    print('All pastes in the current run are source code files hence an empty directory. Exiting')
    exit()








