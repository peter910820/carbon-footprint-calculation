from pymodbus.client.serial import ModbusSerialClient
import time, requests, json

DEVICE_ID = 0x1
def modbus_read():
    client = ModbusSerialClient( method = 'rtu', port = 'COM3',baudrate = 9600,
    stopbits = 1, bytesize = 8, parity = 'N', timeout = 1)

    if not client.connect():
        print("!Error! Fail to connect to modbus slave")
        exit()

    while True:
        result = client.read_holding_registers(1,8,DEVICE_ID)
        try:
            pr = {
               "name": str(result.registers)
            }
            print(result.registers)
            requests.post("https://carbon-footprint-calculation.onrender.com/sd",json.dumps(pr))
        except:
            print(result.function_code)
            print("error!")
        time.sleep(10)
        # PPM*(16.04/22.4)*25*0.000001
if __name__ == "__main__":
    modbus_read()