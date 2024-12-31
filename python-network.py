import network
import ESP8266WebServer
import wemotor
from machine import I2C, Pin

motor = wemotor.Motor()

def left():
    motor.move(0, 50)
    
def right():
    motor.move(50, 0)
    
def handleCmd(socket, args):
    if 'output' in args:
        if args['output'] == 'L':
            left()
        elif args['output'] == 'R':
            right()
        ESP8266WebServer.ok(socket, "200", "OK")
    else:
        ESP8266WebServer.ok(socket, "400", "ERR")
        
LED = Pin(2, Pin.OUT, value = 1)

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('FLAG','12345678')

while not sta.isconnected():
    pass

LED.value(0)

ESP8266WebServer.begin(80)
ESP8266WebServer.onPath("/Race", handleCmd)
ESP8266WebServer.setDocPath("/car")
print("伺服器位址：" +sta.ifconfig()[0])

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='LAB07-'+str(sta.ifconfig()[0]))

while True:
    ESP8266WebServer.handleClient()
    motor.avoidTimeout()