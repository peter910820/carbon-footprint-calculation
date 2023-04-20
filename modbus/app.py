import tkinter as tk
from tkinter import ttk
import sys
from tkinter.constants import *
from pymodbus.client.serial import *
import time

def protocol_select(event):
    if protocol.current() == 2:
        com.configure(state = "disable")
    else:
        com.configure(state = "readonly")
    return

def go_func():
    print(stopbits.get())
    return

def modbus_read():
    DEVICE_ID = 1
    client = ModbusSerialClient(
        method = protocol.get(), port = com.get(),baudrate = int(baudrate.get()),
        stopbits = int(stopbits.get()), bytesize = int(bytesize.get()), parity = parity.get(), timeout = 1)

    if not client.connect():
        print("!Error! Fail to connect to modbus slave")
        sys.exit()

    while True:
        result = client.read_holding_registers(1,8,DEVICE_ID)
        try:
            print(result.registers)
            text.configure(text = result.registers)
        except:
            print(result.function_code)
        time.sleep(1)

window = tk.Tk()
window.title('Modbus tester')
window.geometry('500x600')
window.resizable(False, False)

protocol_text = tk.Label(text="協定")
protocol_text.pack()

protocol = ttk.Combobox(state='readonly')
protocol.pack(fill="x")
protocol['value'] = ('rtu', 'ASCII', 'TCP/IP')
protocol.bind('<<ComboboxSelected>>', protocol_select)

com_text = tk.Label(text="PORT")
com_text.pack()

com = ttk.Combobox(state='readonly')
com.pack(fill="x")
com['value'] = ('COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9')

functionCode_text = tk.Label(text="Function Code")
functionCode_text.pack()

functionCode = ttk.Combobox(state='readonly')
functionCode.pack(fill="x")
functionCode['value'] = ('Read Holding Registers (03)','Read Input Registers (04)')

baudrate_text =  tk.Label(text="baudrate")
baudrate_text.pack()

baudrate = ttk.Combobox(state='readonly')
baudrate.pack(fill="x")
baudrate['value'] = ('1200','2400','4800','9600','115200','19200','38400')

stopbits_text =  tk.Label(text="Stopbits")
stopbits_text.pack()

stopbits = tk.Entry()
stopbits.pack(fill="x")
#--------------------------------------------#
bytesize_text =  tk.Label(text="Bytesize")
bytesize_text.pack()

bytesize = tk.Entry()
bytesize.pack(fill="x")

parity_text =  tk.Label(text="Parity")
parity_text.pack()

parity = tk.Entry()
parity.pack(fill="x")

go = tk.Button(text = "Read", command = modbus_read)
go.pack()

text =  tk.Label(text="")
text.pack()

window.mainloop()