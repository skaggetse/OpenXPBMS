import blynklib
# import blynklib_mp as blynklib # micropython import

BLYNK_AUTH = '1iGFzl578wznCUNvchiyCZgfFVHIKo17' #insert your Auth Token here
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)

# advanced options of lib init
# from __future__ import print_function
# blynk = blynklib.Blynk(BLYNK_AUTH, server='blynk-cloud.com', port=80, ssl_cert=None,
#                        heartbeat=10, rcv_buffer=1024, log=print)

# Lib init with SSL socket connection
# blynk = blynklib.Blynk(BLYNK_AUTH, port=443, ssl_cert='<path to local blynk server certificate>')
# current blynk-cloud.com certificate stored in project as 
# https://github.com/blynkkk/lib-python/blob/master/certificate/blynk-cloud.com.crt
# Note! ssl feature supported only by cPython

# register handler for Virtual Pin V22 reading by Blynk App.
# when a widget in Blynk App asks Virtual Pin data from server within given configurable interval (1,2,5,10 sec etc) 
# server automatically sends notification about read virtual pin event to hardware
# this notification captured by current handler 
@blynk.handle_event('read V22')
def read_virtual_pin_handler(pin):

    # your code goes here
    # ...
    # Example: get sensor value, perform calculations, etc
    sensor_data = '23'
    critilcal_data_value = '24'

    # send value to Virtual Pin and store it in Blynk Cloud 
    blynk.virtual_write(pin, sensor_data)

    # you can define if needed any other pin
    # example: blynk.virtual_write(24, sensor_data)

    # you can perform actions if value reaches a threshold (e.g. some critical value)
    if sensor_data >= critilcal_data_value

        blynk.set_property(pin, 'color', '#FF0000') # set red color for the widget UI element 
        blynk.notify('Warning critical value') # send push notification to Blynk App 
        blynk.email(<youremail@email.com>, 'Email Subject', 'Email Body') # send email to specified address

# main loop that starts program and handles registered events
while True:
    blynk.run()

