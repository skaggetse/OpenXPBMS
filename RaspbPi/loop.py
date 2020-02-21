import serial
import libscrc
import time

# SETUP
sPort = 'COM3'
batteries = 2
hVoltLimit = 3300
lVoltLimit = 3286


payloadW = [0x00,0x00,0x01,0x01,0xc0,0x74,0x0d,0x0a,0x00,0x00]

s = serial.Serial(
    port = sPort,
    baudrate=9600,
    parity=serial.PARITY_MARK,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
s.write(serial.to_bytes(payloadW))
# print("Woke up serial device")
s.flush()
s.close()
time.sleep(.100)

payload1 = [0x03,0x00,0x3F,0x00,0x09]
end = [0x0d,0x0a] 

s = serial.Serial(
    port = sPort,
    baudrate=115200,
    parity=serial.PARITY_MARK,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

battery = 0
readCellbank = 1
error = 0

lista=list()
SOC=list()
moduleVolt=list()
hVolt=list()
lVolt=list()
hTemp=list()
lTemp=list()
PCBTemp=list()
lst=list()

while ( readCellbank == 1 ):
    print('--------------------------------- START READ ----------------------------------')
    count = 0
    while ( battery < batteries):
        print("Reading battery no ", battery)
        battery = battery + 1
        payload1.insert(0,battery)
        crc = libscrc.modbus(bytes(payload1))
        crc = list(crc.to_bytes(2,'little'))
        payload = payload1 + crc + end

        s.write(serial.to_bytes(payload))
        output = s.readline()
        try:
            allData1=[
                "[0]ModulID: ",
                output[0],
                "[4]SOC: ",
                (output[4] / 255),
                "[7-8]PCB Temp: ",
                (output[7] * 256) + output[8],
                "[9-10]Module V: ",
                (output[9] * 256) + output[10],
                "[11-12]High Cell Temp: ",
                (output[11] * 256) + output[12],
                "[12-14]Low Cell Temp: ",
                (output[13] * 256) + output[14],
                "[15-16]High Cell V: ",
                (output[15] * 256) + output[16],
                "[17-18]Low Cell V: ",
                (output[17] * 256) + output[18],
            ]
            SOC.append(allData1[3])
            moduleVolt.append(allData1[7])
            PCBTemp.append(allData1[5])
            hTemp.append(allData1[9])
            lTemp.append(allData1[11])
            hVolt.append(allData1[13])
            lVolt.append(allData1[15])
            count = count + 1
        except IndexError:
            error = error + 1
            battery = battery - 1
            print("Error, reading battery no", battery, "again.")
        # for value in allData1: 
        #     print(value)
        payload1.pop(0)
        time.sleep(.200)
    print("No of RS485 Errors:",error)
    print("Lowest SOC:",min(SOC))
    print("Total Pack Voltage:",sum(moduleVolt))
    print("Highest PCB Temperature:",max(PCBTemp))
    print("Lowest PCB Temperature:",min(PCBTemp))
    print("Highest Cell Temperature:",max(hTemp))
    print("Lowest Cell Temperature:",min(lTemp))
    print("Highest Cell Voltage:",max(hVolt))
    print("Lowest Cell Voltage:",min(lVolt))
    if hVoltLimit < max(hVolt):
        print("Shutdown High Volt")
        m = max(hVolt)
        print(m)
        print([i for i, j in enumerate(hVolt) if j == m])
        # readCellbank = 0
    elif min(lVolt) < lVoltLimit:
        print("Shutdown Low Volt")
        l = max(hVolt)
        print(l)
        print([i for i, j in enumerate(hVolt) if j == l])
        # readCellbank = 0
    SOC=list()
    moduleVolt=list()
    hVolt=list()
    lVolt=list()
    hTemp=list()
    lTemp=list()
    PCBTemp=list()
    battery=0
