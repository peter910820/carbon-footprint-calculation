from pymodbus.client.serial import ModbusSerialClient
import json
import requests
import time

DEVICE_ID = 0x1
def modbus_read():
    username = input('請輸入你在系統上的使用者名稱: ')
    port = input('請輸入COM: ')
    timer = int(input('請輸入多久要傳一次值: '))
    client = ModbusSerialClient( 
    method = 'rtu', 
    port = port,
    baudrate = 9600,
    stopbits = 1, 
    bytesize = 8, 
    parity = 'N', 
    timeout = 1)

    if not client.connect():
        print("ERROR: 'Cannot connect to modbus slave'")
        exit()

    while True:
        result = client.read_holding_registers(1,1,DEVICE_ID)
        data = int(hex(result.registers[0]), 16)*0.0409*24.5*25*0.000001
        try:
            pr = {
                "username": username,
                "data": str(data)
            }
            print(data)
            requests.post("https://carbon-footprint-calculation.onrender.com/sd",json.dumps(pr))
        except:
            print("error!")
        time.sleep(timer)
if __name__ == "__main__":
    modbus_read()

    