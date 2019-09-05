import subprocess
import os
import sys
import time
import argparse
import re
import glob

correct_shsh_hashes = '27325c8258be46e69d9ee57fa9a8fbc28b873df434e5e702a8b27999551138ae', '3a88b7c3802f2f0510abc432104a15ebd8bd7154'

frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description='SaveMe: SHSH saver for macOS')
parser.add_argument('ios_version', help='The version of iOS you want to save blobs for. Examples: 12.4, 12.4.1')
parser.add_argument('--output', '-o', help='Where to save the blobs.', default='~/Desktop')
parser.add_argument('--debug', action='store_true', help='Enable debug output.', default=False)

args = parser.parse_args()

args.output = os.path.expanduser(args.output)

os.chdir(bundle_dir)
os.chdir(os.getcwd() + '/SupportFiles/')

print('[SETUP]')
print(f'\tSaving blobs for iOS version {args.ios_version}')
print(f'\tWill be writing output to {args.output!r}')

input('\n\nConnect Device To Start. Press ENTER when done...')


def get_device_name(udid):
    process = subprocess.run(['./idevice_id', udid], capture_output=True, encoding='utf8')

    if process.returncode:
        print(f'Could not get device name: {process.stderr!r}', file=sys.stderr)
        return None

    return process.stdout.strip()


def recognize_device():
    print('Trying to recognize device...')

    process = subprocess.run(['./idevice_id', '-l'], capture_output=True, encoding='utf8')

    if process.returncode:
        print(f'Could not recognize device: {process.stderr!r}', file=sys.stderr)
        return None

    udids = set(process.stdout.splitlines())

    if len(udids) == 0:
        print("Error identifying your device. Please make sure it's connected and iTunes identifies it.", file=sys.stderr)
        return None
    elif len(udids) > 1:
        print(f"Can only work with 1 device, but got {len(udid)}", file=sys.stderr)
        return None

    udid, = udids

    name = get_device_name(udid)

    if name is None:
        return None

    return udid, name


def run_command_or_exit(arguments, capture=True):
    process = subprocess.run(arguments, capture_output=True, encoding='utf8') if capture else subprocess.run(arguments)

    if process.returncode:
        print(f"Error running {arguments[0]!r}.\nError message:\n{process.stderr}", file=sys.stdout)
        sys.exit(-3)

    return process

udid_data = recognize_device()
while udid_data is None:
    if input("Retry (y/N)? ").lower().strip() != 'y':
        print('Failed to find device!', file=sys.stderr)
        sys.exit(-1)

    udid_data = recognize_device()

udid, name = udid_data

print(f'Identified device as {name!r} with UDID={udid}')

process = run_command_or_exit(['./ideviceenterrecovery', udid], False)
input("Press ENTER once the device has rebooted")

print('Querying device info (ECID, ddevice ID, board ID, ApNonce)...')
process = run_command_or_exit(['./igetnonce'])


info = {
    'ECID': None,
    'board ID': None,
    'device ID': None,
    'ApNonce': None
}

for line in process.stdout.lower().splitlines():
    if line.startswith('ecid='):
        info['ECID'] = line[5:].strip()
    elif line.startswith('identified'):
        m = re.match(r'identified\s+device\s+as\s+([^,]+)\s*,\s*([^ ]+)\s*in\s+recovery\s+mode\.\.\.\s*', line)
        if not m:
            print(f'Failed to extract board ID and device ID from line provided by "igetnonce": {line!r}', file=sys.stderr)
            sys.exit(3)

        info['board ID'], info['device ID'] = m.groups()
    elif line.startswith('apnonce='):
        info['ApNonce'] = line[8:].strip()

hasError = False
for name, value in info.items():
    if value is None:
        print(f"Failed to extract {name}", file=sys.stdout)
        if name != 'ApNonce':
            hasError = True

if hasError:
    sys.exit(4)

if info['ApNonce'] is None:
    print('Retrying to request ApNonce with a different tool...')
    process = run_command_or_exit(['./irecovery', '-q'])

    for line in process.stdout.splitlines():
        m = regex.match(r'^NONC:\s*(.+)$', line)
        if not m:
            print(f"Failed to extract ApNonce from line {line}", file=sys.stderr)
            sys.exit(5)

        info['ApNonce'] = m.group()

if info['ApNonce'] is None:
    print("Failed to extract ApNonce. No idea why", file=sys.stderr)
    sys.exit(6)
        
print('Device Model: ', info['device ID'])
print('Device UDID:  ', udid)
print('BoardConfig:  ', info['board ID'])
print('ECID:         ', info['ECID'])
print('ApNonce:      ', info['ApNonce'])

print(f'\nSaving blobs for iOS version {args.ios_version} to path {args.output}...')

tsscheckerArgs = './tsschecker', '-d', info['device ID'], '-e', info['ECID'], '--boardconfig', info['board ID'], '--ios', args.ios_version,\
                 '--apnonce', info['ApNonce'], '-s', '--save-path', args.output

if args.debug:
    print(f'[DEBUG] tsschecker command: ', tsscheckerArgs)
# tsscheckerArgs = './tsschecker -d %s' %deviceid + ' -e %s' %ecid + ' --boardconfig %s' %boardid + ' --ios %s' %iosversion + ' --apnonce %s' %apnonce + ' -s --save-path ' + savePath

process = subprocess.run(tsscheckerArgs)

if process.returncode:
    print(f"Error running 'tsschecker'.", file=sys.stdout)
    sys.exit(-4)

print('tsschecker run, but we still need to check if the blobs use the correct generator (0x1111111111111111)!\nExiting recovery mode...')
process = run_command_or_exit(['./irecovery', '-n'])

integer_ECID = int(info["ECID"], 16)
print(f'Device should have exited recovery mode.\nChecking generator for ECID decimal {integer_ECID} (the same as hexadecimal {info["ECID"]})...')

SHSH2 = glob.glob(os.path.join(args.output, f'{integer_ECID}_*.shsh2'))
if not SHSH2:
    print(f'Could not locate SHSH2 file for ECID', info['ECID'], f'in path {args.output}!', file=sys.stderr)
    sys.exit(-6)

hasError = 0
for file_path in SHSH2:
    _, file_name = os.path.split(file_path)

    name, _ = file_name.rsplit('.', 1)
    name, Hash = name.rsplit('_', 1)

    if Hash in correct_shsh_hashes:
        print(f'[OK] Correct generator for file {file_path!r}')
    else:
        print(f'[ERROR] Wrong generator for file {file_path!r}', file=sys.stderr)
        hasError += 1

if hasError:
    print(f'{hasError} blobs were saved with the wrong generator', file=sys.stderr)
else:
    print('\tGREAT! All SHSH2 blobs have been saved with the correct generator (0x1111111111111111)')
