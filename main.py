import sys
from Adb_Handler import Adb_Handler as adbHandler
from Server import Server as server

def main():
    devices = adbHandler.getDeviceList(adbHandler)
    if len(devices) > 0:
        server.start(server, host='0.0.0.0', port=5000, key='SHARED_KEY_HERE', deviceId=devices[0])
        print('Server started. enter q to exit')
        while 1:
            if input('\n> ').lower().startswith('q'):
                server.stop(server)
                break

if __name__ == '__main__':
    main()
