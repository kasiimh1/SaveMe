UPDATE v0.6 - SaveMe The Easiest SHSH saver for macOS

Requirements before using 
- install brew
After installing brew run the following commands

1. brew install --HEAD usbmuxd 
2. brew install --HEAD libimobiledevice 
3. brew install --HEAD ideviceinstaller
This should fix issues when not displaying device info

New in this update
1. Fixes wrong ECID and saving path
2. Adds new folder structure when saving tickets (unique per device and firmware)
3. Removed irecovery as it didn't work for some users on High Sierra 
4. Switched back to igetnonce
5. Detects Processor Type ie A12(X) or not 
6. If non A12(X) device it checks the generated nonce against Chimera's and Unc0vers default generators
7. Displays saved ticket path  
8. Migrated to FutureRestore for exiting Recovery Mode as irecovery was removed as mentioned above
9. Biggest feature last, now you're able to check saved Ticket against device's generator with FutureRestore

How to use
1. Download from this link
2. chmod +x the file if it says permission denied 
3. open the binary in terminal 
4. connect your device and press enter
5. wait for it to reboot into recovery mode and press enter
6. enter the iOS version (Non OTA currently signed firmwares only) and press enter
7. wait for file to be saved and press enter again once it appears in your folder where you downloaded the program to
8. read the screen and see if the ticket matches the generator set on device
9. wait for it to reboot
10. Enjoy your newly saved tickets for future use

Screenshots
-  New Folder Structure
- Ticket comparing to devices set generator
- A12(X) device check
- Non A12(X) device check

Shout out to the following people for helping with testing and contributions 
1. /u/tk_ios
2. /u/frakman1
3. /u/ForceBru
4. u/maelxich

Uses the following tools
- FutureRestore https://github.com/s0uthwest/futurerestore
- igetnonce https://github.com/s0uthwest/igetnonce
- libimobiledevice - ideviceenterrecovery, ideviceinfo https://github.com/libimobiledevice
- tsschecker https://github.com/s0uthwest/tsschecker

Future Updates?
- I could possibly compile this for Windows users if that's something you guys would like
- img4tool - check if the saved ticket is valid 
