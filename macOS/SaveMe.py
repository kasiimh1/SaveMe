import subprocess
import os
import sys
import glob

#requires
#brew install --HEAD usbmuxd brew install --HEAD libimobiledevice brew install --HEAD ideviceinstaller

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

hashes = '27325c8258be46e69d9ee57fa9a8fbc28b873df434e5e702a8b27999551138ae','3a88b7c3802f2f0510abc432104a15ebd8bd7154' ,'15400076bc4c35a7c8caefdcae5bda69c140a11bce870548f0862aac28c194cc','603be133ff0bdfa0f83f21e74191cf6770ea43bb'

savePath = os.getcwd()

if (os.path.isdir(savePath + '/SaveMe-Tickets') is False):
    try:
        os.mkdir(savePath + '/SaveMe-Tickets')
    except FileExistsError:
        print('\n\n[*] Skipping creating SaveMe folder as it already exists')

savePath = savePath + '/SaveMe-Tickets'

os.chdir(bundle_dir)
print('\n\nSaveMe v0.9 by Kasiimh1')
print('[*] Connect Device To Start..')
input('[*] Press ENTER when Device is connected > ')
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
ecid = ecid[13:]
ecid = ecid.replace(' ','')


#check if the device is already cached otherwise continue to fetch the remaining data....

popen = subprocess.Popen('./ideviceinfo | grep HardwarePlatform: ', shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
platform, stdErrValue = communicateRes
platform = platform.strip()
platform = platform[18:]

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

print('[*] ' + enterRecovery.strip())
input('[*] Press ENTER when Device is in Recovery Mode > ')

popen = subprocess.Popen('./igetnonce', stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
communicateRes = popen.communicate()
igetNonceOuput, stdErrValue = communicateRes
igetNonceOuput = igetNonceOuput.split('\n')

for s in igetNonceOuput:
    if s.startswith('ApNonce='):
        apnonce = s
        apnonce = apnonce.replace('ApNonce=','')

if (platform.find('t8020') == 0 or platform.find('t8027') == 0 or platform.find('t8030') == 0):
    print('[*] Detected A12/13(X) Device')
else:
    for x in hashes:
        if (apnonce == x) is True:
            print('[*] Detected Non A12/13(X) Device')
            print('[*] Device ApNonce matches the default unc0ver or chimera generator')
            break;
        else:
            print('[*] Detected Non A12/13(X) Device')
            print('[*] Device ApNonce does not match the unc0ver or chimera generator')
            break;
    
print('[D] Device Model = ' + deviceid)
print('[D] Device UDID = ' + udid)
print('[D] BoardConfig = ' + boardid)
print('[D] ECID = ' + ecid)
print('[D] ApNonce = ' + apnonce)

iosversion = input('[D] Enter the iOS version to save the ticket for > ')

if (os.path.isdir(savePath + '/' + ecid) is False):
    try:
        os.mkdir(savePath + '/' + ecid)
    except FileExistsError:
        print('[*] Skipping creating ECID folder as %s it already exists' %ecid)

savePath = savePath + '/' + ecid

if (os.path.isdir(savePath + '/' + iosversion) is False):
    try:
        os.mkdir(savePath + '/' + iosversion)
    except FileExistsError:
        print('[*] Skipping creating iOS version folder as %s it already exists' %ecid)

savePath = savePath + '/' + iosversion

tsscheckerArgs = './tsschecker -d %s' %deviceid + ' -e %s' %ecid + ' --boardconfig %s' %boardid + ' --ios %s' %iosversion + ' --apnonce %s' %apnonce + ' -s --save-path %s' %savePath
popen = subprocess.Popen([tsscheckerArgs], shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')

# print('[*] Checking ticket against device in Recovery Mode')
input('[*] Press Enter When File is Saved > ')

ticket = ''
for file in glob.glob(os.path.join(savePath, "*.shsh2")):
    ticket = file

# print('[*] Checking this ticket ' + ticket)
# popen = subprocess.Popen('./irecovery -n', shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
# input('[*] Press ENTER when Device is Booted Up > ')
# popen = subprocess.Popen('./futurerestore -w -t %s ' %ticket, shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
# communicateRes = popen.communicate()
# ticketCheck, stdErrValue = communicateRes
# print('\n\n[*] %s' %ticketCheck)

popen = subprocess.Popen('./irecovery -n', shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')
print('[*] Exiting Recovery Mode')
if (ticket != None) is True:
    print('[*] File Save as ' + ticket)
else:
    print('Problem occurred when saving SHSH ticket')
print('[*] Exiting')
