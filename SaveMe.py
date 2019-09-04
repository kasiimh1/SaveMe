import subprocess
import os
import sys

import sys, os
frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

savePath = '~/Desktop'

os.chdir(bundle_dir)
print('Connect Device To Start..\n')

os.chdir(os.getcwd() + '/SupportFiles/')

popen = subprocess.Popen('./igetnonce', stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
igetNonceOuput, stdErrValue = communicateRes
igetNonceOuput = igetNonceOuput.split('\n')

ecid = ''
boardid = ''
deviceid = ''
apnonce = ''
iosversion = 0

for s in igetNonceOuput:
    if s.startswith('ECID='):
        ecid = s
        ecid = ecid.replace('ECID=','')
        ecid = ecid[:13]

    if s.startswith('ApNonce='):
        apnonce = s
        apnonce = apnonce.replace('ApNonce=','')

    if s.startswith('Identified device as '):
        boardid = s
        boardid = boardid.replace('Identified device as ','')
        boardid = boardid.replace('in normal mode...','')
        deviceid = boardid[8:]
        boardid = boardid[:6]
        
print('Device Model = ' + deviceid)
print('BoardConfig = ' + boardid)
print('ECID = ' + ecid)
print('ApNonce = ' + apnonce)
print('Enter the iOS version to save the ticket for')

iosversion = input()

tsscheckerArgs = './tsschecker -d %s' %deviceid + ' -e %s' %ecid + ' --boardconfig %s' % (boardid) + ' --ios %s' % (iosversion) + ' --apnonce %s' % (apnonce) + ' -s --save-path ' + (savePath)

popen = subprocess.Popen([tsscheckerArgs], shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
tsscheckerOutput, stdErrValue = communicateRes

print('File saved at path ' + savePath)
print('Exiting')
