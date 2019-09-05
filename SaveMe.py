import subprocess
import os
import sys
import time

frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

udid = ''
ecid = ''
boardid = ''
deviceid = ''
apnonce = ''
iosversion = 0

savePath = '~/Desktop'

os.chdir(bundle_dir)
print('\n\n[*] Connect Device To Start..')
os.chdir(os.getcwd() + '/SupportFiles/')

popen = subprocess.Popen('./ideviceinfo | grep UniqueDeviceID: ', shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
udid, stdErrValue = communicateRes
udid = udid.strip()
udid = udid[16:]

popen = subprocess.Popen('./ideviceinfo | grep UniqueChipID: ', shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
ecid, stdErrValue = communicateRes
ecid = ecid.strip()
ecid = ecid[15:]

popen = subprocess.Popen('./ideviceinfo | grep ProductType: ', shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
deviceid, stdErrValue = communicateRes
deviceid = deviceid.strip()
deviceid = deviceid[13:]

popen = subprocess.Popen('./ideviceinfo | grep HardwareModel: ', shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
boardid, stdErrValue = communicateRes
boardid = boardid.strip()
boardid = boardid[15:]

popen = subprocess.Popen('./ideviceenterrecovery %s' %udid, shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
enterRecovery, stdErrValue = communicateRes
print('[*] ' + enterRecovery)

time.sleep(20) #some devices reboot faster than others

popen = subprocess.Popen('./irecovery -q', shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
apNonce, stdErrValue = communicateRes
apNonce = apNonce.split('\n')

for s in apNonce:
    if s.startswith('NONC:'):
        apnonce = s
        apnonce = apnonce.replace('NONC:','')
        
print('[D] Device Model = ' + deviceid)
print('[D] Device UDID = ' + udid)
print('[D] BoardConfig = ' + boardid)
print('[D] ECID = ' + ecid)
print('[D] ApNonce = ' + apnonce)
print('[D] Enter the iOS version to save the ticket for')

iosversion = input()

tsscheckerArgs = './tsschecker -d %s' %deviceid + ' -e %s' %ecid + ' --boardconfig %s' %boardid + ' --ios %s' %iosversion + ' --apnonce %s' %apnonce + ' -s --save-path ' + savePath

popen = subprocess.Popen([tsscheckerArgs], shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
popen = subprocess.Popen('./irecovery -n', shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')

print('[*] File saved at path ' + savePath)
print('[*] Exiting')
