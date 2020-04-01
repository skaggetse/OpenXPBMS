#
#  ____                _  _____  ___  __  _______
# / __ \___  ___ ___  | |/_/ _ \/ _ )/  |/  / __/
#/ /_/ / _ \/ -_) _ \_>  </ ___/ _  / /|_/ /\ \  
#\____/ .__/\__/_//_/_/|_/_/  /____/_/  /_/___/  
#    /_/                                         
#
#
# This script requires a USB to RS485 adapter terminated with a Tyco AMP connector.
# It was tested on Windows using an FTDI cable. It will print battery voltage and temperature data for battery 1 to the console.
# This code is released under GPLv3 and comes with no warrany or guarantees. Use at your own risk!

import serial
import libscrc

sPort = 'COM3'
payloadW = [0x00,0x00,0x01,0x01,0xc0,0x74,0x0d,0x0a,0x00,0x00]
payload1 = [0x01,0x03,0x00,0x3F,0x00,0x09,0xB5,0xC0,0x0d,0x0a]
payload2 = [0x02,0x03,0x00,0x3f,0x00,0x09,0xB5,0xF3,0x0d,0x0a]
payloadV = [0x01,0x03,0x00,0x45,0x00,0x09,0x94,0x19,0x0d,0x0a]
payloadT = [0x01,0x03,0x00,0x50,0x00,0x07,0x04,0x19,0x0d,0x0a]

s = serial.Serial(
    port = sPort,
    baudrate=9600,
    parity=serial.PARITY_MARK,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
s.write(serial.to_bytes(payloadW))
#print("Woke up serial device")
s.flush()
s.close()

print(serial.to_bytes(payload1))

s = serial.Serial(
    port = sPort,
    baudrate=115200,
    parity=serial.PARITY_MARK,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
s.write(serial.to_bytes(payloadV))
outputV = s.readline()
s.write(serial.to_bytes(payloadT))
outputT = s.readline()
s.write(serial.to_bytes(payload1))
output1 = s.readline()
s.write(serial.to_bytes(payload2))
output2 = s.readline()
s.close()




volts=[(outputV[9] * 256) + outputV[10],
    (outputV[11] * 256) + outputV[12],
    (outputV[13] * 256) + outputV[14],
    (outputV[15] * 256) + outputV[16]
]
volts.append(volts[0]+volts[1]+volts[2]+volts[3])

temps=[(outputT[5] * 256) + outputT[6],
    (outputT[7] * 256) + outputT[8],
    (outputT[9] * 256) + outputT[10],
    (outputT[11] * 256) + outputT[12],
    (outputT[3] * 256) + outputT[4]
]
print(outputV)
for value in volts: 
    print(value)
print(outputT)
for value in temps: 
    print(value)

allData1=[
    "[0]ModulID: ",
    output1[0],
    "[4]SOC: ",
    (output1[4] / 255),
    "[7-8]PCB Temp: ",
    (output1[7] * 256) + output1[8],
    "[9-10]Module V: ",
    (output1[9] * 256) + output1[10],
    "[11-12]High Cell Temp: ",
    (output1[11] * 256) + output1[12],
    "[12-14]Low Cell Temp: ",
    (output1[13] * 256) + output1[14],
    "[15-16]High Cell V: ",
    (output1[15] * 256) + output1[16],
    "[17-18]Low Cell V: ",
    (output1[17] * 256) + output1[18],
    "Whole Response: "
]
for value in allData1: 
    print(value)
print(output1)

allData2=[
    "[0]ModulID: ",
    output2[0],
    "[4]SOC: ",
    (output2[4] / 255),
    "[7-8]PCB Temp: ",
    (output2[7] * 256) + output2[8],
    "[9-10]Module V: ",
    (output2[9] * 256) + output2[10],
    "[11-12]High Cell Temp: ",
    (output2[11] * 256) + output2[12],
    "[12-14]Low Cell Temp: ",
    (output2[13] * 256) + output2[14],
    "[15-16]High Cell V: ",
    (output2[15] * 256) + output2[16],
    "[17-18]Low Cell V: ",
    (output2[17] * 256) + output2[18],
    "Whole Response: "
]
for value in allData2: 
    print(value)
print(output2)