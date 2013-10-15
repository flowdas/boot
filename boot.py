#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bootstrap a python project

Usage::
    git init
    curl -O https://raw.github.com/flowdas/boot/master/boot.py
    python boot.py
"""
__version__ = "1.0a1"

import sys
import os
import urlparse
import urllib
import hashlib
import subprocess
import string

if sys.version_info < (2, 6):
    print('ERROR: %s' % sys.exc_info()[1])
    print('ERROR: this script requires Python 2.6 or greater.')
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.join(os.getcwd(),__file__))
VENV_EXE = 'venv\\Scripts\\python.exe' if sys.platform == 'win32' else 'venv/bin/python'

def samefile(path1, path2):
    return os.path.normpath(path1) == os.path.normpath(path2)

def fetch(url, hash):
    filename = os.path.join(BASE_DIR,os.path.basename(urlparse.urlparse(url).path))
    if not os.path.exists(filename):
        urllib.urlretrieve(url, filename)
    f = open(filename, 'rb')
    digest = hashlib.sha1(f.read()).hexdigest()
    f.close()
    if digest != hash:
        print('ERROR: %s' % filename)
        print('ERROR: SHA1 digest mispatch.')
        sys.exit(1)

def create(path, content):
    if not os.path.exists(path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

def install_venv():
    fetch(
        'https://raw.github.com/pypa/virtualenv/1.10.1/virtualenv.py',
        '37ee18c4b66bbbf967a93565812e0c53fe342f92',
        )
    fetch(
        'https://pypi.python.org/packages/source/s/setuptools/setuptools-1.1.6.tar.gz',
        '4a8863e8196704759a5800afbcf33a94b802ac88',
        )
    fetch(
        'https://pypi.python.org/packages/source/p/pip/pip-1.4.1.tar.gz',
        '9766254c7909af6d04739b4a7732cc29e9a48cb0',
        )
    subprocess.call([sys.executable, 'virtualenv.py', '-q', 'venv'])

SETUP_PY = """# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup_requires = [
    ]

install_requires = [
    ]

dependency_links = [
    ]

setup(
    name='Boot-Generated-Project',
    version='1.0a1',
    description='',
    author='',
    author_email='',
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    dependency_links=dependency_links,
    scripts=[],
    entry_points={
        'console_scripts': [
            ],
        },
    )
"""

MANIFEST_IN = """include boot.py
"""

GITIGNORE = """.DS_Store
*.py[co]
*.sublime-workspace
/venv/
/build/
/dist/
*.egg-info/
/virtualenv.py
/setuptools-*.tar.gz
/pip-*.tar.gz
"""

def setup_git():
    if not os.path.exists('.git'):
        return
    if os.path.exists('.gitignore'):
        dirty = False
        data = open('.gitignore').read()
        if data and data[-1:] != '\n':
            data += '\n'
        olds = map(string.strip, data.split('\n'))
        for patt in map(string.strip,GITIGNORE.split('\n')):
            if patt not in olds:
                data += patt + '\n'
                dirty = True
        if dirty:
            f = open('.gitignore', 'wt')
            f.write(data)
            f.close()
    else:
        create('.gitignore', GITIGNORE)

def install_setup():
    create('setup.py', SETUP_PY)
    create('MANIFEST.in', MANIFEST_IN)
    subprocess.call([VENV_EXE, 'setup.py', '-q', 'develop'])

def main():
    os.chdir(BASE_DIR)
    if not samefile(sys.executable, VENV_EXE):
        install_venv()
    install_setup()
    setup_git()
    if not samefile(sys.executable, VENV_EXE):
        if sys.platform == 'win32':
            command = 'venv\\Scripts\\activate'
        else:    
            command = 'source venv/bin/activate'
        print('Now you can run "%s"' % command)

if __name__=='__main__':
    main()
