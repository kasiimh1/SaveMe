import sys, os, argparse, subprocess

frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

replace = False
exit = False

def installDependencies():
    print('[I] Installing Brew.sh')
    os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"')
    print('[I] Installing usbmuxd')
    os.system('brew install --HEAD usbmuxd')
    print('[I] Installing libimobiledevice')
    os.system('brew install --HEAD libimobiledevice')
    print('[I] Installing ideviceinstaller')
    os.system('brew install --HEAD ideviceinstaller')
    print('[I] Finished Installing Dependencies, Exiting....')
    sys.exit(-1)   

def requestDeviceTicket(d_id, d_ecid, d_boardid, d_ios, d_apnonce, d_save):
    tsscheckerArgs = './tsschecker -d %s' %d_id + ' -e %s' %d_ecid + ' --boardconfig %s' %d_boardid + ' --ios %s' %d_ios + ' --apnonce %s' %d_apnonce + ' -s --save-path %s' %d_save
    print(tsscheckerArgs)
    subprocess.Popen([tsscheckerArgs], shell = True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf8')

def deviceExtractionTool(binaryName, stripValue, grepValue, replace):
    command = './' + binaryName + ' | grep ' + grepValue
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    output = process.communicate()
    stdOutput, stdErrValue = output
    stdOutput = stdOutput.strip()
    stdOutput = stdOutput[stripValue:]
    if replace == True:
        stdOutput = stdOutput.replace(' ', '')
    return dataReturn(stdOutput, stdErrValue)

def deviceEnterRecMode(udid):
    command = './ideviceenterrecovery ' + udid
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    output = process.communicate()
    stdOutput, stdErrValue = output
    stdOutput = stdOutput.strip()
    return dataReturn(stdOutput, stdErrValue)

def deviceExtractApNonce():
    process = subprocess.Popen('./igetnonce', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    output = process.communicate()
    stdOutput, stdErrValue = output
    stdOutput = stdOutput.split('\n')
    data = dataReturn(stdOutput, stdErrValue)
    for s in data:
        if s.startswith('ApNonce='):
            data = s
            data = data.replace('ApNonce=','')
    return data 

def dataReturn(output, error):
    ret = None
    if error != None:
        ret = error
    if output != None:
        ret = output       
    return ret

defaultHashes = '27325c8258be46e69d9ee57fa9a8fbc28b873df434e5e702a8b27999551138ae','3a88b7c3802f2f0510abc432104a15ebd8bd7154',
'15400076bc4c35a7c8caefdcae5bda69c140a11bce870548f0862aac28c194cc','603be133ff0bdfa0f83f21e74191cf6770ea43bb'

parser = argparse.ArgumentParser(description='SaveMe: SHSH saver for macOS')
#parser.add_argument('-a', help='Add New Devices To Cache List')
#parser.add_argument('-c', help='Print Cached Devices')
#parser.add_argument('-d', help='Enable Debug Output Logs', action='store_true')
parser.add_argument('-i', help='Install SaveMe Dependencies', action='store_true')
parser.add_argument('-g', help='Use Custom SHSH2 Generator')
parser.add_argument('-n', help='Use Custom SHSH2 Nonce')
parser.add_argument('-u', help='Grab nonce from Userland')
parser.add_argument('-r', help='Grab nonce from Recovery Mode')
parser.add_argument('-s', help='Set Custom SHSH2 Save Path', default='~/Desktop/')
parser.add_argument('-v', help='Set iOS Version For Saving Tickets ')

args = parser.parse_args()
print('\nSaveMe v1.0 by Kasiimh1')
if args.i != False:
    installDependencies()
while exit != True:
    args.output = os.path.expanduser(args.s)
    savePath = args.output

    if (os.path.isdir(savePath + 'SaveMe-Tickets') is False):
        try:
            os.mkdir(savePath + 'SaveMe-Tickets')
        except FileExistsError:
            print('\n\n[*] Skipping creating SaveMe folder as it already exists')

    savePath = savePath + 'SaveMe-Tickets'
    os.chdir(bundle_dir)
    if args.v == None:
        args.v = input('[*] Enter iOS Version To Save Ticket For: ')

    print('[*] iOS version set to save for is', args.v)
    print('[*] Connect Device To Start..')

    if args.r == None and args.u == None:
        print('[*] No Nonce Extraction Method Was Set!')
        print('[*] Defaulting to Recovery Mode Nonce Extraction (Rebooting Device)')
        input('[*] Press ENTER when Device is connected > ')
        #os.chdir(os.getcwd() + '/SupportFiles/')
        udid = deviceExtractionTool('ideviceinfo', 16, 'UniqueDeviceID: ', False)
        ecid = deviceExtractionTool('ideviceinfo', 13, 'UniqueChipID: ', True)
        platform = deviceExtractionTool('ideviceinfo', 18, 'HardwarePlatform: ', False)
        product = deviceExtractionTool('ideviceinfo', 13, 'ProductType: ', False)
        user = deviceExtractionTool('ideviceinfo', 12, 'DeviceName: ', False)
        boardid = deviceExtractionTool('ideviceinfo', 15, 'HardwareModel: ', False)

        if udid != None:
            print('[D] Found ' + user)
            print('[D] Device is:', product)
            print('[D] BoardID is:', boardid)
            print('[D] Found Device: UDID:', udid)
            print('[D] ECID:', ecid)
            print('[D] Device Platform:', platform)
            print('[*] Entering Recovery Mode Now!')
            deviceEnterRecMode(udid)
            input('[*] Press ENTER when Device is in Recovery Mode > ')
            APNonce = deviceExtractApNonce()
            print('[*] Found APNonce in Recovery Mode:', APNonce)

            if (platform.find('t8020') == 0 or platform.find('t8027') == 0 or platform.find('t8030') == 0):
                print('[*] Detected A12/13(X) Device')
            else:
                for x in defaultHashes:
                    if (APNonce == x) is True:
                        print('[*] Detected Non A12/13(X) Device')
                        print('[*] Device ApNonce matches the default unc0ver or chimera generator')
                        break
                    else:
                        print('[*] Detected Non A12/13(X) Device')
                        print('[*] Device ApNonce does not match the unc0ver or chimera generator')
                        break

            if (os.path.isdir(savePath + '/' + ecid) is False):
                try:
                    os.mkdir(savePath + '/' + ecid)
                except FileExistsError:
                        print('[*] Skipping creating ECID folder as %s it already exists' %ecid)
            savePath = savePath + '/' + ecid

            if (os.path.isdir(savePath + '/' + args.v) is False):
                try:
                    os.mkdir(savePath + '/' + args.v)
                except FileExistsError:
                    print('[*] Skipping creating iOS version folder as %s it already exists' %ecid)
            savePath = savePath + '/' + args.v
                
            requestDeviceTicket(product, ecid, boardid, args.v, APNonce, savePath)
            print('[*] Exiting Recovery Mode')
            os.system('./irecovery -n')
            print('[*] File should be in:', savePath)
            command = 'open ' + savePath
            os.system(command)
            if input("Use SaveMe again? (y/n)? ").lower().strip() == 'y':
                exit = False
                args.v = None
            else:
                exit = True
                print('[*] Thanks for using SaveMe v1.0, Exiting Program')
                sys.exit(-1)                
    else:
        print('Error No Device Found, Try again!')
        if input("Retry (y/n)? ").lower().strip() == 'y':
            exit = False
        if input("Retry (y/n)? ").lower().strip() == 'n':
            exit = True
            print('[*] Thanks for using SaveMe v1.0, Exiting Program')
            sys.exit(-1)