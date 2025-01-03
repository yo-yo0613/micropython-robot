import network
import ESP8266WebServer # 匯入網站模組
import wemotor
from machine import I2C, Pin
import time

motor = wemotor.Motor()

# 左轉
def left():
    motor.move(0, 50)
    
# 右轉
def right():
    motor.move(50, 0)
    
# 直走
def front():
    motor.move(40, 40)

# 退後
def back():
    motor.move(-40, -40)
    
# 停止
def stop():
    motor.move(0, 0)

    
# 處理 /Race 指令的函式
def handleCmd(socket, args):
    #檢查是否有 output 參數
    if 'output' in args:
        if args['output'] == 'L':   # 若 output 參數值為 'L'
            left()                  # 左轉
            print('左轉')
        elif args['output'] == 'R': # 若 output 參數值為 'R'
            right()                 # 右轉
            print('右轉')
        elif args['output'] == 'F':
            front()
            print('前進')
        elif args['output'] == 'B':
            back()
            print('後退')
        elif args['output'] == 'S':
            stop()
            print('停止')
        time.sleep(1)
        #  回應 OK 給瀏覽器
        ESP8266WebServer.ok(socket, "200", "OK")
    else:
        #  回應 ERR 給瀏覽器
        ESP8266WebServer.err(socket, "400", "ERR")
        
LED = Pin(2, Pin.OUT, value = 1)    # 關閉內建 LED 燈

sta = network.WLAN(network.STA_IF)  # 開啟工作站介面
sta.active(True)                    # 啟用無線網路
sta.connect('FLAG', '12345678')     # 連結無線網路

# 等待無線網路連上
while not sta.isconnected():
    pass

LED.value(0)                        # 開啟內建 LED 燈

ESP8266WebServer.begin(80)          # 啟用網站
# 指定處理指令的函式 Race
ESP8266WebServer.onPath("/Pace", handleCmd)
print("伺服器位址：" + sta.ifconfig()[0]) # 顯示網站的 IP 位址

# 建立 AP
ap = network.WLAN(network.AP_IF)
ap.active(True)
# AP 名稱為 IP 位址
ap.config(essid='LAB06-'+str(sta.ifconfig()[0]))

while True:
    ESP8266WebServer.handleClient() # 檢查是否收到新指令
    motor.avoidTimeout()            # 避免 time.out