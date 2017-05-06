from usched import Sched
from utime import sleep
from machine import Pin

def stop(fTim, objSch):
    # Stop the scheduler after fTim seconds
    yield fTim
    objSch.stop()

def flash(pin, time):
    led = Pin(pin, Pin.OUT)
    while True:
        led.value(not led.value())
        yield time

def test():
    sched = Sched(True)
    sched.add_thread(flash(0, 0.5))
    sched.add_thread(flash(2, 0.25))
    sched.add_thread(stop(5.6, sched))
    sched.run()

def signalStart():
    led0 = Pin(0, Pin.OUT)
    led2 = Pin(2, Pin.OUT)
    led0.high()
    for x in range(4):
        led0.value(not led0.value())
        led2.value(not led2.value())
        sleep(0.5)

if __name__ == "__main__":
    signalStart()

    while True:
        test()
        sleep(5)
