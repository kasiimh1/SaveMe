# SaveMe
 Grab Device ECID, ApNonce, BoardConfig and iPhoneID from device and grab signed SHSH via TSSChecker
 
 UPDATE - Removed igetnonce replaced with ideviceinfo, rewrote the args and use grep for grabbing the values and strip the return values to remove white spaces both leading and trailing.

 Now grabs NONC: from recovery mode using irecovery and fixed model names breaking the request (tested   with iPad5,3)
 Fixed the boardconfig of the iPhone11,6 being cut off 
 Now grabs ApNonce from Recovery Mode. (ApNone set in NVRAM)

Thanks To Tihmstar & S0uthwest and the creators of iRecovery & Libmobiledevice for

- tsschecker
- ideviceinfo
- irecovery
- ideviceenterrecovery
