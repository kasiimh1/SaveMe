import sys, os, argparse, subprocess, json, csv, requests, webbrowser, paramiko, getpass
from shutil import copyfile

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

def dumpDeviceTicket(saveTicketPath):
    print("[*] Saving to: %s" %saveTicketPath)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ip = input("Enter Devices IP: ")
    password = getpass.getpass("root@" + ip + "'s password: ")
    ssh.connect(ip, port=22, username='root', password = password)
    print("Installing Dependancies")
    os.system("scp img4tool_192_iphoneos-arm.deb root@"+ ip + ":img4tool_192_iphoneos-arm.deb")
    os.system("scp libssl1.1_1.1.1g_iphoneos-arm.deb root@"+ ip + ":libssl1.1_1.1.1g_iphoneos-arm.deb")
    os.system("scp libgeneral_31_iphoneos-arm.deb root@"+ ip + ":libgeneral_31_iphoneos-arm.deb")
    os.system("scp libimg4tool0_192_iphoneos-arm.deb root@"+ ip + ":libimg4tool0_192_iphoneos-arm.deb")
    os.system("scp libplist3_2.2.0_iphoneos-arm.deb root@"+ ip + ":libplist3_2.2.0_iphoneos-arm.deb")
    os.system("ssh root@"+ ip + " dpkg -i libplist3_2.2.0_iphoneos-arm.deb")
    os.system("ssh root@"+ ip + " dpkg -i libssl1.1_1.1.1g_iphoneos-arm.deb")
    os.system("ssh root@"+ ip + " dpkg -i libgeneral_31_iphoneos-arm.deb")
    os.system("ssh root@"+ ip + " dpkg -i libimg4tool0_192_iphoneos-arm.deb")
    os.system("ssh root@"+ ip + " dpkg -i img4tool_192_iphoneos-arm.deb")
    print("Dumping Ticket from iOS FileSystem")
    stdin, stdout, stderr = ssh.exec_command("cat /dev/rdisk1 | dd of=dump.raw bs=256 count=$((0x4000)) &> /dev/null")
    print("Converting Dump to Ticket")
    os.system("ssh root@"+ ip + " img4tool --convert -s dumped.shsh dump.raw")
    print("Copying Dump to machine")
    os.system("scp root@"+ ip + ":dumped.shsh %s/dumped.shsh" %saveTicketPath)
    if args.o:
            subprocess.run(['explorer', os.path.realpath('%s/dumped.shsh' %saveTicketPath)])

def requestDeviceTicket(d_id, d_ecid, d_boardid, d_ios, d_apnonce, d_save, d_ota):
    process = subprocess.Popen('tsschecker.exe -d %s' %d_id + ' -e %s' %d_ecid + ' --boardconfig %s' %d_boardid + ' --ios %s' %d_ios + ' --apnonce %s' %d_apnonce + ' -s --save-path %s' %d_save + ' %s' %d_ota, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    if args.l:
        output = process.communicate()
        stdOutput, stdErrValue = output
        stdOutput = stdOutput.strip()
        print(stdErrValue)
        print(stdOutput)

def deviceExtractionTool(binaryName, stripValue, grepValue, replace):
    command = binaryName + ' | findstr ' + grepValue
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    output = process.communicate()
    stdOutput, stdErrValue = output
    stdOutput = stdOutput.strip()
    stdOutput = stdOutput[stripValue:]
    if replace == True:
        stdOutput = stdOutput.replace(' ', '')
    return dataReturn(stdOutput, stdErrValue)

def deviceEnterRecMode(udid):
    command = 'ideviceenterrecovery.exe ' + udid
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    output = process.communicate()
    stdOutput, stdErrValue = output
    stdOutput = stdOutput.strip()
    return dataReturn(stdOutput, stdErrValue)

def deviceExtractApNonce():
    process = subprocess.Popen('irecovery.exe -q | findstr NONC', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    output = process.communicate()
    stdOutput, stdErrValue = output
    stdOutput = stdOutput.split('\n')
    data = dataReturn(stdOutput, stdErrValue)
    for s in data:
        if s.startswith('NONC: '):
            data = s
            data = data.replace('NONC: ','')
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

def createSavePath(ecid, version):
    path = args.s + 'SaveMe-Tickets/' + ecid + '/'
    file = os.path.expanduser(path)
    if os.path.isdir(file) is False:
        try:
            os.mkdir(file)
        except FileExistsError:
                print('[*] Skipping creating ECID folder as %s it already exists' %ecid)

    if os.path.isdir(file + version) is False:
        try:
            os.mkdir(file + version)
        except FileExistsError:
            print('[*] Skipping creating iOS version folder as %s it already exists' %ecid)

def saveTicketsForCachedDevices(version):
    file = os.path.expanduser(args.s + 'SaveMe-Tickets/SaveMe-Devices')
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
            print("-- Saving Ticket For Cached Device -- ")
            createSavePath(i['ecid'], version)  
            if not i['boardid'].find("J105aAP") == True and not i['boardid'].find("J42dAP") == True and not i['boardid'].find("K66AP") == True and not i['boardid'].find("J33IAP") == True and not i['boardid'].find("J33AP") == True:
                print("[*] --------------------------- DEVICE NEEDS REGULAR BLOBS -------------------------------------")
                ota = ''
                requestDeviceTicket(i['model'], i['ecid'], i['boardid'], version, i['apnonce'],  args.s + 'SaveMe-Tickets/' + i['ecid'] + '/' + version + '/', ota)
            if i['boardid'].find("J105aAP") or i['boardid'].find("J42dAP") or i['boardid'].find("K66AP") or i['boardid'].find("J33IAP") or i['boardid'].find("J33AP"):
                print("[*] --------------------------- DEVICE NEEDS OTA BLOBS -------------------------------------")
                ota = ' -o'
                requestDeviceTicket(i['model'], i['ecid'], i['boardid'], version, i['apnonce'],  args.s + 'SaveMe-Tickets/' + i['ecid'] + '/' + version + '/', ota)
            if args.o:
                subprocess.run(['explorer', os.path.realpath(args.s + 'SaveMe-Tickets/' + i['ecid'] + '/' + version + '/' )])
        print("------------------------------------------------------------------------")
    
def signedVersionChecker(model):
    ret = None
    signedReq = requests.get("https://api.ipsw.me/v4/device/" + model + "?type=ipsw")
    print("-- Checking Currently Signed iOS Versions --")
    print("[A] IPSW.me API Response Code: ["+ str(signedReq.status_code) + "]")
    if signedReq.status_code == 200:
        print("-- Server Response --")
        api = json.loads(signedReq.text)
        apiLength = len(api['firmwares'])
        for i in range(apiLength):
            if args.c == True and api['firmwares'][i]['signed'] == True or args.v == None and api['firmwares'][i]['signed'] == True:
                print("[V] iOS", api['firmwares'][i]['version'], "is currently being signed for the:", api['identifier'])
                if args.f == True:
                    saveTicketsForCachedDevices(api['firmwares'][i]['version'])
                if args.t == True:
                    ret = api['firmwares'][i]['version']

            if api['firmwares'][i]['version'] == args.v and api['firmwares'][i]['signed'] == True:
                print("[V] iOS", api['firmwares'][i]['version'], "is currently being signed for the:", api['identifier'])
                break
            
            if api['firmwares'][i]['version'] == args.v and api['firmwares'][i]['signed'] != True:
                print("[V] iOS", api['firmwares'][i]['version'], "is currently NOT being signed for the:", api['identifier'])
                break
    return ret

def writeDevicesToOutput(data, path):
    f = open(path + "/SaveMe-Devices", "a")
    f.write(data)
    f.close()

def openFolder(savePath):
    print('[*] File should be in:', savePath)
    os.system('open ' + savePath)

def fetchAPNonce(udid):
    print('-- Fetching APNonce From Recovery Mode --')
    deviceEnterRecMode(udid)
    input('[*] Press ENTER when Device is in Recovery Mode > ')
    APNonce = deviceExtractApNonce()
    print('[*] Found APNonce in Recovery Mode:', APNonce)
    print('[*] Exiting Recovery Mode')
    os.system('irecovery.exe -n')
    return APNonce

# defaultHashes = '27325c8258be46e69d9ee57fa9a8fbc28b873df434e5e702a8b27999551138ae','3a88b7c3802f2f0510abc432104a15ebd8bd7154',
# '15400076bc4c35a7c8caefdcae5bda69c140a11bce870548f0862aac28c194cc','603be133ff0bdfa0f83f21e74191cf6770ea43bb'

parser = argparse.ArgumentParser(description='SaveMe: SHSH saver for macOS by Kasiimh1')
parser.add_argument('-a', help='Add Device To Cache List (-d needed)', action='store_true')
parser.add_argument('-c', help='Check Currently Signed iOS Versions (uses iPhone11,2 by default) or use -m to specify model', action='store_true') 
parser.add_argument('-d', help='Fetch Information From Device', action='store_true')
parser.add_argument('-f', help='Save SHSH2 Tickets For Cached Devices (-c needed)', action='store_true') 
parser.add_argument('-g', help='Specifiy Custom Generator')
parser.add_argument('-l', help='Debug Log for TSSChecker', action='store_true')
parser.add_argument('-o', help='Open Folder after Tickets are Saved', action='store_true')
parser.add_argument('-p', help='Print Cached Devices', action='store_true')
parser.add_argument('-m', help='Set Device Model e.g. iPhone11,2 (used with -c)')
parser.add_argument('-s', help='Set Custom SHSH2 Save Path', default=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/'))
parser.add_argument('-t', help='Save SHSH2 Ticket', action='store_true')
parser.add_argument('-v', help='Set iOS Version For Saving Tickets')
parser.add_argument('-x', help='Dump Ticket from Device', action='store_true')

args = parser.parse_args()
print('\nSaveMe v1.2 by Kasiimh1')

if args.p == True:
    if os.path.isfile(os.path.expanduser(args.s) + '/SaveMe-Tickets/SaveMe-Devices'):
        printCachedDevices()
    else:
        print('-- No Cached Device File Found, use -a -d to add device!')
    sys.exit(-1)
if args.c == True:
    if args.m:
        signedVersionChecker(args.m)
    else:
        signedVersionChecker("iPhone11,2")
    sys.exit(-1)

args.output = os.path.expanduser(args.s)
savePath = args.output

if (os.path.isdir(savePath) is False):
    try:
        os.mkdir(savePath)
    except FileExistsError:
        print('\n\n[*] Skipping creating save path folder as it already exists')

if (os.path.isdir(savePath + 'SaveMe-Tickets') is False):
    try:
        os.mkdir(savePath + 'SaveMe-Tickets')
    except FileExistsError:
        print('\n\n[*] Skipping creating SaveMe folder as it already exists')

savePath = savePath + 'SaveMe-Tickets'
os.chdir(bundle_dir)

if args.x:
    print("[*] Dumping Ticket from Device!")
    os.chdir(os.getcwd() + '/SupportFiles/')
    dumpDeviceTicket(savePath)

if args.a and args.d:
    input('[*] Press ENTER when Device is connected > ')
    os.chdir(os.getcwd() + '/SupportFiles/')
    udid = deviceExtractionTool('ideviceinfo.exe', 16, 'UniqueDeviceID: ', False)
    ecid = deviceExtractionTool('ideviceinfo.exe', 13, 'UniqueChipID: ', True)
    platform = deviceExtractionTool('ideviceinfo.exe', 18, 'HardwarePlatform: ', False)
    product = deviceExtractionTool('ideviceinfo.exe', 13, 'ProductType: ', False)
    user = deviceExtractionTool('ideviceinfo.exe', 12, 'DeviceName: ', False)
    boardid = deviceExtractionTool('ideviceinfo.exe', 15, 'HardwareModel: ', False)
    APNonce = None
    generator = None

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
    if not os.path.isfile(os.path.expanduser(args.s) + '/SaveMe-Tickets/SaveMe-Devices'):
        try:
            copyfile('SaveMe-Devices', '%s' %savePath + '/SaveMe-Devices')
        except FileExistsError:
            print('\n\n[*] Skipping creating SaveMe-Devices file as it already exists')
    if args.g == None:
        print("[*] Using Unc0ver's Generator!")
        generator = "0x1111111111111111"
    else:
        print("[*] User Using Custom Generator!")
        generator = args.g

    APNonce = fetchAPNonce(udid)
    data = '\n"' + user + '","' + boardid + '","' + product + '","' + generator + '","' + ecid + '","' + udid + '","' + platform + '","' + APNonce + '"'
    writeDevicesToOutput(data, savePath)
    print('[*] Thanks for using SaveMe v1.0, Exiting Program')
    sys.exit(-1)

if args.t == True:
    print("-- Saving SHSH2 Ticket --")    
    signedOS = signedVersionChecker(product)

    if (signedOS) != None:
        if args.v == None:
            print("-- No iOS Version Set, Defaulting To Latest iOS Version Being Signed! --")
            print("-- iOS " + signedOS + " is Signed, Defaulting To That Versions --")
        else:
            print('[*] iOS Version Saving SHSH2 Ticket For', args.v)
        APNonce = fetchAPNonce(udid)
        createSavePath(ecid, signedOS)
        savePath = savePath + '/' + ecid + '/' + signedOS + '/'
        requestDeviceTicket(product, ecid, boardid, signedOS, APNonce, savePath)
        if args.o:
            subprocess.run(['explorer', os.path.realpath(savePath)])
        print('[*] Thanks for using SaveMe v1.0, Exiting Program')
    else:
        print("-- Error iOS Version Not Signed --")
    sys.exit(-1)  

if not args.a and not args.c and not args.d and not args.f and not args.l and not args.p and not args.t and not args.x:
    parser.print_help()
    sys.exit(-1)  