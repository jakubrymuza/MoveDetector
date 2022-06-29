import requests
import gpiod
import time

base = "http://localhost:5000"

chip = gpiod.Chip('gpiochip0')
led = chip.get_line(27)
led.request(consumer="consumer", type=gpiod.LINE_REQ_DIR_OUT)
led.set_value(0)

button = chip.get_line(25)
button.request(consumer="consumer", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

sensor = chip.get_line(18)
sensor.request(consumer="consumer", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

def IsAlarm():
    ans = requests.get(base + "/state")

    if "True" in str(ans.content):
        return True
    else: 
        return False

def detector():

    while True:

        if not sensor.get_value():
            continue

        print("wykryto ruch") #

        led.set_value(1) 

        requests.post(base + "/alarm")
        time.sleep(0.5)

        while IsAlarm():

            if not button.get_value():
                print("wykryto przycisk")
                requests.post(base + "/cancelled")
                break

            time.sleep(0.5)          


        led.set_value(0)
        print("alarm wylaczony")


if __name__ == '__main__':
    detector()
    