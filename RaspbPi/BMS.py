import serial
import libscrc
import time
import statistics
import BMSsettings
import RPi.GPIO as GPIO
import logging
if BMSsettings.debug == False:
    import curses
    import tui

payloadW = [0x00,0x00,0x01,0x01,0xc0,0x74,0x0d,0x0a,0x00,0x00]

now = time.time()
lasttime = now

s = serial.Serial(
    port = BMSsettings.sPort,
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


payloadBMS = [0x03,0x00,0x3F,0x00,0x09]
footer = [0x0d,0x0a] 

s = serial.Serial(
    port = BMSsettings.sPort,
    baudrate=115200,
    parity=serial.PARITY_MARK,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Setup GPIO pins for relay on/off
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)

# Function relay on
def chargeEnable():
    GPIO.output(16,GPIO.HIGH)
# Function relay off
def chargeShutdown():
    GPIO.output(16,GPIO.LOW)

# Startup with relay on
#print("Charge Enable")
chargeEnable()

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename= BMSsettings.path + 'batterylog.log',
                    filemode='w')


def sHEX(hexstr):
    if hexstr > 32767:
        hexstr = hexstr - 65536
    return hexstr

battery = 0
readCellbank = 1
error = 0
reading = str()

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
    while ( battery < BMSsettings.batteries):
        battery = battery + 1
        # print("Reading battery no ", battery)
        payloadBMS.insert(0,battery)
        crc = libscrc.modbus(bytes(payloadBMS))
        crc = list(crc.to_bytes(2,'little'))
        payload = payloadBMS + crc + footer

        s.write(serial.to_bytes(payload))
        output = s.readline()
        fullData = False
        #If LF occurs in values and message is broken, look for more bytes and add until buffer is empty
        while fullData == False:

            if s.in_waiting > 0:
                output = output + s.readline()
                fullData = False
            else:
                fullData = True
                break
        
        # print("Payload: ", payload)
        # print("Response: ", output)

        # Calculate expected CRC    
        responsecrc = libscrc.modbus(output[:-4])
        responsecrc = responsecrc.to_bytes(2,'little')

        # If CRC matches, continue
        if responsecrc == output[21:-2]:
            SOC.append((output[4] / 256))
            current.append(sHEX((output[5] * 256) + output[6]))
            moduleVolt.append((output[9] * 256) + output[10])
            PCBTemp.append(sHEX((output[7] * 256) + output[8]))
            hTemp.append(sHEX((output[11] * 256) + output[12]))
            lTemp.append(sHEX((output[13] * 256) + output[14]))
            hVolt.append((output[15] * 256) + output[16])
            lVolt.append((output[17] * 256) + output[18])

        # If CRC differs, clear buffer and read module again
        else:
            output = list()
            s.reset_input_buffer()
            error = error + 1
            # print("CRC Mismatch, clearing buffer & reading battery no", battery, "again.")
            battery = battery - 1

        payloadBMS.pop(0) #Remove Slave no from payload
        time.sleep(.100)

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

    if BMSsettings.hVoltLimit < max(hVolt):
        chargeShutdown()
        # print("Shutdown High Volt")
        # m, hVcell = None
        # m = max(hVolt)
        # print(m)
        # hVcell = [i for i, j in enumerate(hVolt) if j == m]

    elif min(lVolt) < BMSsettings.lVoltLimit:
        chargeShutdown()
        # print("Shutdown Low Volt")
        # l = min(lVolt)
        # print(l)
        # print([i for i, j in enumerate(hVolt) if j == l])

    battery=0

    output_SOC=round((min(SOC)*100))
    if BMSsettings.batteries > 2: # Added a new way to calculate current
        current.sort()
        reliableCurrent = current[1:-1]
    else:
        reliableCurrent = current
    output_reliableCurrent=round((statistics.mean(reliableCurrent)/100),1)
    output_moduleVolt=round((sum(moduleVolt)/1000))
    output_hPCBTemp=round((max(PCBTemp)/1000),1)
    output_lPCBTemp=round((min(PCBTemp)/1000),1)
    output_hTemp=round((max(hTemp)/1000),1)
    output_lTemp=round((min(lTemp)/1000),1)
    output_hVolt=max(hVolt)
    output_lVolt=min(lVolt)

    output_log = [output_SOC, output_reliableCurrent, output_moduleVolt, output_hVolt, output_hTemp, output_hPCBTemp, output_lVolt, output_lVolt, output_lPCBTemp]

    logging.info(output_log)

    # Update TUI
    if BMSsettings.debug == False:

        tui.screen.attron(curses.A_BOLD)
        tui.screen.addstr(tui.centerrow(1,1), tui.centercol(str(output_SOC),1), str(output_SOC))
        tui.screen.addstr(tui.centerrow(1,1), tui.centercol(str(output_reliableCurrent),2), str(output_reliableCurrent))
        tui.screen.addstr(tui.centerrow(1,1), tui.centercol(str(output_moduleVolt),3), str(output_moduleVolt))
        tui.screen.addstr(tui.centerrow(1,2), tui.centercol(str(output_hVolt),1), str(output_hVolt))
        tui.screen.addstr(tui.centerrow(1,2), tui.centercol(str(output_hTemp),2), str(output_hTemp))
        tui.screen.addstr(tui.centerrow(1,2), tui.centercol(str(output_hPCBTemp),3), str(output_hPCBTemp))
        tui.screen.addstr(tui.centerrow(1,3), tui.centercol(str(output_lVolt),1), str(output_lVolt))
        tui.screen.addstr(tui.centerrow(1,3), tui.centercol(str(output_lTemp),2), str(output_lTemp))
        tui.screen.addstr(tui.centerrow(1,3), tui.centercol(str(output_lPCBTemp),3), str(output_lPCBTemp))
        tui.screen.attroff(curses.A_BOLD)

        reading = reading + "."
        if reading == "....":
            reading = str()
        tui.screen.addstr((tui.hthirds*3)-1, (tui.wthirds*3)-13, " READING    ")
        tui.screen.addstr((tui.hthirds*3)-1, (tui.wthirds*3)-5, reading)
        tui.screen.addstr((tui.hthirds*3)-1, 7, str(error) + " ")
        tui.screen.refresh()

        key = tui.screen.getch()
        if key == ord('q'):
            break

#Reset window
if BMSsettings.debug == False:
    # clear the screen
    tui.screen.clear()

    # reverse terminal settings
    curses.nocbreak()
    tui.screen.keypad(False)
    curses.echo()

    # close the application
    curses.endwin()

chargeShutdown()
print("Program terminated, charge shutdown")