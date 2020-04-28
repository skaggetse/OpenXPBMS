import blynklib
# import blynklib_mp as blynklib # micropython import

BLYNK_AUTH = '1iGFzl578wznCUNvchiyCZgfFVHIKo17' #insert your Auth Token here
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)

blynk.virtual_write(3,'0.1') # Send the value 0.1 to a display widget on V3


blynk.run()

