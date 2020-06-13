UPDATE v1.0 - SaveMe The Easiest SHSH saver for macOS!

This is a complete rewrite with new features!

Requirements before using for macOS
- SaveMe v1.0 now handles installing brew and the dependencies you just need to specify the arg when running be patient while it runs

Run: `SaveMe -i`

___
SaveMe 1.0 args
___
SaveMe: SHSH saver for macOS by Kasiimh1

optional arguments:
  -h, --help  show this help message and exit
  -a          Add Device To Cache List (-d needed)
  -c          Check Currently Signed iOS Versions
  -d          Fetch Information From Device
  -f          Save SHSH2 Tickets For Cached Devices (-c needed)
  -g G        Specifiy Custom Generator
  -i          Install SaveMe Dependencies
  -p          Print Cached Devices
  -s S        Set Custom SHSH2 Save Path
  -t          Save SHSH2 Ticket
  -v V        Set iOS Version For Saving Tickets
___

- New Features
1. Fetches device info and saves it to a cached device list
2. Set version to save ticket for saving
3. Allows setting path for saving tickets too
4. Print Cached Devices 
5. Print currently signed firmwares
6. Specify a generator, must be already set on device! (expects unc0ver's 0x1111111111111111)
7. Save currently signed firmwares from cached device list! (device does not need to be connected)

- Planned Features
1. Print currently signed BETA iOS versions
2. Add ticket checking with imgtool4
3. Add FutureRestore support automating restoring if device is connected and SHSH2 file exists! 
4. IPSW downloader for device when connected (and arg set)
5. Downloading of SEP and BBFW (if needed) for FutureRestore restores 

- Unknown 
1. Not sure if it works on newer iPads and new iPhone SE 2

- Tested 
1. iPhone11,2
2. iPad7,3

- Screenshots

1. (https://github.com/kasiimh1/SaveMe/blob/master/macOS/Screenshots/Screenshot%202020-06-13%20at%2012.20.21.png)
2. (https://github.com/kasiimh1/SaveMe/blob/master/macOS/Screenshots/Screenshot%202020-06-13%20at%2012.42.03.png)
3. (https://github.com/kasiimh1/SaveMe/blob/master/macOS/Screenshots/Screenshot%202020-06-13%20at%2012.42.29.png)

Uses the following tools
- libimobiledevice - ideviceenterrecovery, ideviceinfo, irecovery https://github.com/libimobiledevice
- tsschecker https://github.com/tihmstar/tsschecker
