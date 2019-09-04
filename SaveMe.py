import subprocess
import os

print("Connect Device To Start..\n")
igetNonceArgs = ("../igetnonce")

popen = subprocess.Popen(igetNonceArgs, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
communicateRes = popen.communicate()
igetNonceOuput, stdErrValue = communicateRes
igetNonceOuput = igetNonceOuput.split("\n")

ecid = ""
boardid = ""
deviceid = ""
apnonce = ""
iosversion = 0

for s in igetNonceOuput:
    if s.startswith("ECID="):
        ecid = s
        ecid = ecid.replace("ECID=","")
        ecid = ecid[:13]

    if s.startswith("ApNonce="):
        apnonce = s
        apnonce = apnonce.replace("ApNonce=","")

    if s.startswith("Identified device as "):
        boardid = s
        boardid = boardid.replace("Identified device as ","")
        boardid = boardid.replace("in normal mode...","")
        deviceid = boardid[8:]
        boardid = boardid[:6]
        
print("Device Model = " + deviceid)
print("BoardConfig = " + boardid)
print("ECID = " + ecid)
print("ApNonce = " + apnonce)

print("Enter the iOS version to save the ticket for")
iosversion = raw_input()

tsscheckerArgs = '../tsschecker -d %s' %deviceid + ' -e %s' %ecid + ' --boardconfig %s' % (boardid) + ' --ios %s' % (iosversion) + ' --apnonce %s' % (apnonce) + ' -s --save-path ' + (os.getcwd()) + '/'

popen = subprocess.Popen([tsscheckerArgs], shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
communicateRes = popen.communicate()
tsscheckerOutput, stdErrValue = communicateRes

print(tsscheckerOutput)
