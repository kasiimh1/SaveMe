Windows version now includes latest tsschecker with A14 support from here: https://github.com/DanTheMann15/tsschecker/releases
macOS version is still outdated at the time of writing. 

UPDATE v1.3 (Windows) - SaveMe The Easiest SHSH saver for macOS and Windows!

- New Features
1. Fetches device info and saves it to a cached device list
2. Set version to save ticket for saving
3. Allows setting path for saving tickets too
4. Print Cached Devices 
5. Print currently signed firmwares
6. Specify a generator, must be already set on device! (expects unc0ver's 0x1111111111111111)
7. Save currently signed firmwares from cached device list! (device does not need to be connected)
8. Dump ticket from iOS device (requires device to be jailbroken)

- Planned Features
1. Print currently signed BETA iOS versions
2. Add ticket checking with imgtool4
3. Add FutureRestore support automating restoring if device is connected and SHSH2 file exists! 
4. IPSW downloader for device when connected (and arg set)
5. Downloading of SEP and BBFW (if needed) for FutureRestore restores 

- Tested 
1. iPhone11,2
2. iPad7,3
3. AppleTV 4K

- Video Demo 
link (https://www.youtube.com/watch?v=RZzXPi1cncE)

- Screenshots

1. (https://github.com/kasiimh1/SaveMe/blob/master/macOS/Screenshots/Screenshot%202020-06-13%20at%2012.20.21.png)
2. (https://github.com/kasiimh1/SaveMe/blob/master/macOS/Screenshots/Screenshot%202020-06-13%20at%2012.42.03.png)
3. (https://github.com/kasiimh1/SaveMe/blob/master/macOS/Screenshots/Screenshot%202020-06-13%20at%2012.42.29.png)

Uses the following tools
- libimobiledevice - ideviceenterrecovery, ideviceinfo, irecovery https://github.com/libimobiledevice
- tsschecker https://github.com/tihmstar/tsschecker (macOS) and https://github.com/DanTheMann15/tsschecker/releases (Windows)
