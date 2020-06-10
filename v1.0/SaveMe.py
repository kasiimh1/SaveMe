import sys, os, argparse, subprocess, json, csv, requests

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
    print('[I] Installing liblist')
    os.system('brew install --HEAD libplist')
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

def printCachedDevices():
    file = os.path.expanduser(args.s + '/SaveMe-Tickets/SaveMe-Devices')
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for i in csv_reader:
            print("------------------------------------------------------------------------")
            print("-- Found Device --")
            print("[D] Name: " + i['name'])
            print("[D] Model: " + i['model'])
            print("[D] UDID: " + i['udid'])
            print("[D] ECID: " + i['ecid'])
            print("[D] BoardID: " + i['boardid'])
            print("[D] Platform: " + i['platform'])
            print("[D] Generator: " + i['generator'])
            print("[D] APNonce: " + i['apnonce'])
        print("------------------------------------------------------------------------")

def signedVersionChecker(model):
    signedReq = requests.get("https://api.ipsw.me/v4/device/" + model + "?type=ipsw")
    print("-- Checking Currently Signed iOS Versions --")
    print("[A] IPSW.me API Response Code: ["+ str(signedReq.status_code) + "]")
    ret = 0
    if signedReq.status_code == 200:
        print("-- Server Response --")
        api = json.loads(signedReq.text)
        apiLength = len(api['firmwares'])
        for i in range(apiLength):
            if args.c == True and api['firmwares'][i]['signed'] == True:
                print("[V] iOS", api['firmwares'][i]['version'], "is currently being signed for the:", api['identifier'])

            if api['firmwares'][i]['version'] == args.v and api['firmwares'][i]['signed'] == True:
                print("[V] iOS", api['firmwares'][i]['version'], "is currently being signed for the:", api['identifier'])
                ret = 1
                break
            if api['firmwares'][i]['version'] == args.v and api['firmwares'][i]['signed'] != True:
                print("[V] iOS", api['firmwares'][i]['version'], "is currently NOT being signed for the:", api['identifier'])
                ret = -1
                break
    return ret

def writeDevicesToOutput(data, path):
    f = open(path + "/SaveMe-Devices", "a")
    f.write(data)
    f.close()

defaultHashes = '27325c8258be46e69d9ee57fa9a8fbc28b873df434e5e702a8b27999551138ae','3a88b7c3802f2f0510abc432104a15ebd8bd7154',
'15400076bc4c35a7c8caefdcae5bda69c140a11bce870548f0862aac28c194cc','603be133ff0bdfa0f83f21e74191cf6770ea43bb'

parser = argparse.ArgumentParser(description='SaveMe: SHSH saver for macOS')
parser.add_argument('-a', help='Add Device To Cache List (-d needed)', action='store_true')
parser.add_argument('-c', help='Check Currently Signed iOS Versions', action='store_true') #works
parser.add_argument('-d', help='Fetch Information From Device', action='store_true') # works
parser.add_argument('-i', help='Install SaveMe Dependencies', action='store_true') # works
parser.add_argument('-g', help='Specifiy Custom Generator') #works
parser.add_argument('-p', help='Print Cached Devices', action='store_true') # works
parser.add_argument('-s', help='Set Custom SHSH2 Save Path', default='~/Desktop/') #works
parser.add_argument('-t', help='Save SHSH2 Ticket', action='store_true') #works
parser.add_argument('-v', help='Set iOS Version For Saving Tickets') #works

args = parser.parse_args()
while exit != True:
    print('\nSaveMe v1.0 by Kasiimh1')

    if args.i != False:
        installDependencies()

    if args.p == True:
            printCachedDevices()
            sys.exit(-1)

    if args.c == True:
        signedVersionChecker("iPhone11,2")
        sys.exit(-1)

    args.output = os.path.expanduser(args.s)
    savePath = args.output

    if (os.path.isdir(savePath + 'SaveMe-Tickets') is False):
        try:
            os.mkdir(savePath + 'SaveMe-Tickets')
        except FileExistsError:
            print('\n\n[*] Skipping creating SaveMe folder as it already exists')

    savePath = savePath + 'SaveMe-Tickets'
    os.chdir(bundle_dir)
    input('[*] Press ENTER when Device is connected > ')
    #os.chdir(os.getcwd() + '/SupportFiles/')
    udid = deviceExtractionTool('ideviceinfo', 16, 'UniqueDeviceID: ', False)
    ecid = deviceExtractionTool('ideviceinfo', 13, 'UniqueChipID: ', True)
    platform = deviceExtractionTool('ideviceinfo', 18, 'HardwarePlatform: ', False)
    product = deviceExtractionTool('ideviceinfo', 13, 'ProductType: ', False)
    user = deviceExtractionTool('ideviceinfo', 12, 'DeviceName: ', False)
    boardid = deviceExtractionTool('ideviceinfo', 15, 'HardwareModel: ', False)
    APNonce = None
    generator = "0x1111111111111111"

    if udid != None and args.d == True:
        print("[*] Fetching Infromation From Device")                
        print("-- Device Information --")                
        print('[D] Found ' + user)
        print('[D] Device is:', product)
        print('[D] BoardID is:', boardid)
        print('[D] Found Device: UDID:', udid)
        print('[D] ECID:', ecid)
        print('[D] Device Platform:', platform)

    if args.a == True:
        print("-- Adding Device To Cached List --")                
        if args.g == None:
            print("[*] Using Unc0ver's Generator!")
            generator = "0x1111111111111111"
        else:
            print("[*] User Using Custom Generator!")
            generator = args.g

        data = '\n"' + user + '","' + boardid + '","' + product + '","' + generator + '","' + ecid + '","' + udid + '","' + platform + '","' + APNonce + '"'

        writeDevicesToOutput(data, savePath)
        print('[*] Thanks for using SaveMe v1.0, Exiting Program')
        sys.exit(-1)

    if args.t == True:
        print("-- Saving SHSH2 Ticket --")    
        if args.v == None:
            args.v = input('[*] Enter iOS Version To Save Ticket For: ')
        else:
            print('[*] iOS Version Saving SHSH2 Ticket For', args.v)

        print('-- Fetching APNonce From Recovery Mode --')
        input('[*] Press Enter To Enter Recovery Mode ')
        deviceEnterRecMode(udid)
        input('[*] Press ENTER when Device is in Recovery Mode > ')
        APNonce = deviceExtractApNonce()
        print('[*] Found APNonce in Recovery Mode:', APNonce)
        print('[*] Exiting Recovery Mode')
        os.system('./irecovery -n')

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
        print('[*] File should be in:', savePath)
        command = 'open ' + savePath
        os.system(command)

    if input("Use SaveMe again? (y/n)? ").lower().strip() == 'y':
        exit = False
        args.v = None
        check = False
    else:
        exit = True
        print('[*] Thanks for using SaveMe v1.0, Exiting Program')
        sys.exit(-1)                