import network
import ESP8266WebServer # 匯入網站模組
import wemotor
from machine import I2C, Pin
import time

motor = wemotor.Motor()

# 左轉
def left():
    motor.move(0, 150)
    time.sleep(0.5)
    stop()
    
# 右轉
def right():
    motor.move(150, 0)
    time.sleep(0.5)
    stop()
    
# 前進
def front():
    motor.move(150, 150)
    time.sleep(0.5)
    stop()
    
# 後退
def back():
    stop()
    time.sleep(0.2)
    motor.move(-150, -150)
    time.sleep(0.5)
    stop()
    
def stop():
    motor.move(0, 0)
# 處理 /Race 指令的函數
def handleCmd(socket, args):
    if 'output' in args:
        if args['output'] == 'L':   # 左轉
            left()
        elif args['output'] == 'R': # 右轉
            right()
        elif args['output'] == 'F': # 前進
            front()
        elif args['output'] == 'B': # 後退
            back()
        elif args['output'] == 'S': # 停止
            stop()
        
        # 手動構造 HTTP 重定向響應
        response = "HTTP/1.1 302 Found\r\n"
        response += "Location: /car.html\r\n"
        response += "Connection: close\r\n\r\n"
        socket.send(response.encode())
    else:
        ESP8266WebServer.err(socket, "400", "ERR")

# 處理 car.html 的函數
def handleCarHtml(socket, args):
    try:
        with open("car.html", "r") as file:
            html = file.read()
        ESP8266WebServer.ok(socket, "200", html)
    except Exception as e:
        ESP8266WebServer.err(socket, "500", "File not found!")

# 處理 home.html 的函數
def handleHomeHtml(socket, args):
    try:
        with open("home.html", "r") as file:
            html = file.read()
        ESP8266WebServer.ok(socket, "200", html)
    except Exception as e:
        ESP8266WebServer.err(socket, "500", "File not found!")

# 處理 timer.html 的函數
def handleTimerHtml(socket, args):
    try:
        with open("timer.html", "r") as file:
            html = file.read()
        ESP8266WebServer.ok(socket, "200", html)
    except Exception as e:
        ESP8266WebServer.err(socket, "500", "File not found!")

# 處理 caculator.html 的函數
def handleCaculatorHtml(socket, args):
    try:
        with open("cacultor.html", "r") as file:
            html = file.read()
        ESP8266WebServer.ok(socket, "200", html)
    except Exception as e:
        ESP8266WebServer.err(socket, "500", "File not found!")


# 處理 to-do-list-app.html 的函數
def handleToDoListHtml(socket, args):
    try:
        with open("to-do-list-app.html", "r") as file:
            html = file.read()
        ESP8266WebServer.ok(socket, "200", html)
    except Exception as e:
        ESP8266WebServer.err(socket, "500", "File not found!")

LED = Pin(2, Pin.OUT, value = 1)    # 關閉內建 LED 燈

sta = network.WLAN(network.STA_IF)  # 開啟工作站介面
sta.active(True)                    # 啟用無線網路
sta.connect('FLAG', '12345678')     # 連結無線網路

# 等待無線網路連上
while not sta.isconnected():
    pass

LED.value(0)                        # 開啟內建 LED 燈

ESP8266WebServer.begin(80)          # 啟用網站
ESP8266WebServer.onPath("/", handleCarHtml)  # 根目錄對應 car.html
ESP8266WebServer.onPath("/home", handleHomeHtml) # 根目錄對應 home.html
ESP8266WebServer.onPath("/timer", handleHomeHtml) # 根目錄對應 timer.html
ESP8266WebServer.onPath("/caculator", handleHomeHtml) # 根目錄對應 caculator.html
ESP8266WebServer.onPath("/to-do-list-app", handleHomeHtml) # 根目錄對應 to-do-list-app.html
# 指定處理指令的函式 Race
ESP8266WebServer.onPath("/Race", handleCmd)
print("伺服器位址：" + sta.ifconfig()[0]) # 顯示網站的 IP 位址

# 建立 AP
ap = network.WLAN(network.AP_IF)
ap.active(True)
# AP 名稱為 IP 位址
ap.config(essid='LAB06-'+str(sta.ifconfig()[0]))

while True:
    ESP8266WebServer.handleClient() # 檢查是否收到新指令
    motor.avoidTimeout()            # 避免 time.out