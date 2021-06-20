import sys
import subprocess
import re
import os

class Adb_Handler:
    command = 'service call isms 6 i32 0 s16 "com.android.mms.service" s16 "null" s16 "[receiver]" s16 "null" s16 "[msg]" s16 "null" s16 "null" s16 "null" s16 "null" s16 "null"'
    
    def adbExists(self):
        if os.name == 'nt':
            cmd = subprocess.run(['where', 'adb'], stdout=subprocess.PIPE)
        else:
            cmd = subprocess.run(['which', 'adb'], stdout=subprocess.PIPE)
        result = cmd.stdout.decode('utf-8') 
        return (len(result) > 0 and (result.splitlines()[0] != 'adb not found' or result.splitlines()[0] != 'INFO: Could not find files for the given pattern(s).'))

    def getDeviceList(self):
        if not self.adbExists(self):
            return []

        cmd = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
        result = cmd.stdout.decode('utf-8').splitlines()
        result = result[1:len(result) - 1]
        devices = []

        for device in result:            
            devices.append(re.split(r'\t+', device.rstrip('\t'))[0])

        return devices

    def sendSms(self, deviceId, receiver, msg):
        command = self.command.replace('[receiver]', receiver).replace('[msg]', msg)
        cmd = subprocess.run(
            [
                'adb', 
                '-s', 
                deviceId, 
                'shell', 
                command
            ], 
            stdout=subprocess.PIPE
        )
        return (cmd.stdout.decode('utf-8').splitlines()[0] == 'Result: Parcel(00000000    \'....\')')