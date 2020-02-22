import serial
import libscrc
import time
import statistics
import BMSsettings
import time
import curses

# initialize application
stdscr = curses.initscr()

# tweak terminal settings
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)

payloadW = [0x00,0x00,0x01,0x01,0xc0,0x74,0x0d,0x0a,0x00,0x00]

s = serial.Serial(
    port = BMSsettings.sPort,
    baudrate=9600,
    parity=serial.PARITY_MARK,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
s.write(serial.to_bytes(payloadW))
# print("Woke up serial device")
s.flush()
s.close()
time.sleep(.100)


payloadBMS = [0x03,0x00,0x3F,0x00,0x09]
footer = [0x0d,0x0a] 

s = serial.Serial(
    port = BMSsettings.sPort,
    baudrate=115200,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

battery = 0
readCellbank = 1
error = 0

while ( readCellbank == 1 ):

    SOC=list()
    current=list()
    moduleVolt=list()
    hVolt=list()
    lVolt=list()
    hTemp=list()
    lTemp=list()
    PCBTemp=list()
    # print('--------------------------------- START READ ----------------------------------')
    count = 0
    while ( battery < BMSsettings.batteries):
        # print("Reading battery no ", battery)
        battery = battery + 1
        payloadBMS.insert(0,battery)
        crc = libscrc.modbus(bytes(payloadBMS))
        crc = list(crc.to_bytes(2,'little'))
        payload = payloadBMS + crc + footer

        s.write(serial.to_bytes(payload))
        output = s.readline()
        try:
            # allData1=[
            #     "[0]ModulID: ",
            #     output[0],
            #     "[4]SOC: ",
            #     (output[4] / 255),
            #     "[7-8]PCB Temp: ",
            #     (output[7] * 256) + output[8],
            #     "[9-10]Module V: ",
            #     (output[9] * 256) + output[10],
            #     "[11-12]High Cell Temp: ",
            #     (output[11] * 256) + output[12],
            #     "[12-14]Low Cell Temp: ",
            #     (output[13] * 256) + output[14],
            #     "[15-16]High Cell V: ",
            #     (output[15] * 256) + output[16],
            #     "[17-18]Low Cell V: ",
            #     (output[17] * 256) + output[18],
            # ]
            SOC.append((output[4] / 255))
            current.append((output[5] * 256) + output[6])
            moduleVolt.append((output[9] * 256) + output[10])
            PCBTemp.append((output[7] * 256) + output[8])
            hTemp.append((output[11] * 256) + output[12])
            lTemp.append((output[13] * 256) + output[14])
            hVolt.append((output[15] * 256) + output[16])
            lVolt.append((output[17] * 256) + output[18])
            count = count + 1
        except IndexError:
            error = error + 1
            battery = battery - 1
            # print("Error, reading battery no", battery, "again.")
        # for value in allData1: 
        #     print(value)
        payloadBMS.pop(0)
    #     time.sleep(.200)
    # print("No of RS485 Errors:",error)
    # print("Lowest SOC:",min(SOC))
    # print("Median Current:",statistics.median(current))
    # print("Total Pack Voltage:",sum(moduleVolt))
    # print("Highest PCB Temperature:",max(PCBTemp))
    # print("Lowest PCB Temperature:",min(PCBTemp))
    # print("Highest Cell Temperature:",max(hTemp))
    # print("Lowest Cell Temperature:",min(lTemp))
    # print("Highest Cell Voltage:",max(hVolt))
    # print("Lowest Cell Voltage:",min(lVolt))
    # write something on the screen
    stdscr.addstr(2, 2, "State of Charge:" + str(min(SOC)*100))
    stdscr.addstr(4, 2, "Pack Voltage:" + str(sum(moduleVolt)/1000))
    stdscr.addstr(6, 2, "Current:" + str(statistics.median(current)))
    stdscr.addstr(8, 2, "Highest Cell Voltage:" + str(max(hVolt)))
    stdscr.addstr(10, 2, "Lowest Cell Voltage:" + str(min(lVolt)))
    stdscr.addstr(12, 2, "Highest Cell Temperature:" + str(max(hTemp)))
    stdscr.addstr(14, 2, "Lowest Cell Temperature:" + str(min(lTemp)))
    stdscr.addstr(16, 2, "Highest PCB Temperature:" + str(max(PCBTemp)))
    stdscr.addstr(18, 2, "Lowest PCB Temperature" + str(min(PCBTemp)))
    stdscr.addstr(20, 2, "No of read errors:" + str(error))


    # update the screen
    stdscr.refresh()

    if BMSsettings.hVoltLimit < max(hVolt):
        print("Shutdown High Volt")
        m = max(hVolt)
        print(m)
        print([i for i, j in enumerate(hVolt) if j == m])
        # readCellbank = 0
    elif min(lVolt) < BMSsettings.lVoltLimit:
        print("Shutdown Low Volt")
        l = max(hVolt)
        print(l)
        print([i for i, j in enumerate(hVolt) if j == l])
        # readCellbank = 0
    battery=0