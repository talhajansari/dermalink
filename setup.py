#!/usr/bin/python
import os, subprocess, sys
subprocess.call(['python', 'virtualenv.py', 'flask'])
if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'


extensions = [ext.strip() for ext in open('requirements.txt')]

for ext in extensions:
	subprocess.call([os.path.join('flask', bin, 'pip'), 'install', ext])	

if sys.platform == 'win32':
    subprocess.call([os.path.join('flask', bin, 'pip'), 'install', '--no-deps', 'lamson', 'chardet', 'flask-mail'])