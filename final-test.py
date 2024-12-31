import network
import ESP8266WebServer
import wemotor
from machine import I2C, Pin
import time

result = ''
move = False

turn_time = 0

motor = wemotor.Motor()

def handleCmd(socket, args):
    global result, turn_time
    
    if 'output' in args:
        result = args['output']
        turn_time = time.ticks_ms()
        ESP8266WebServer.ok(socket, "200", "OK")
    else:
        #  回應 ERR 給瀏覽器
        ESP8266WebServer.err(socket, "400", "ERR")
        
LED = Pin(2, Pin.OUT, value = 1)

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('FLAG', '12345678')     # 連結無線網路
while(not sta.isconnected()):
    pass

LED.value(0)

ESP8266WebServer.begin(80)          # 啟用網站
# 指定處理指令的函式 Race
ESP8266WebServer.onPath("/Race", handleCmd)
print("伺服器位址：" + sta.ifconfig()[0]) # 顯示網站的 IP 位址

# 建立 AP
ap = network.WLAN(network.AP_IF)
ap.active(True)
# AP 名稱為 IP 位址
ap.config(essid='LAB015-'+str(sta.ifconfig()[0]))

while True:
    ESP8266WebServer.handleClient()
    # 如果接收到 A 且車子還沒開始動
    if(result == 'A' and move == False):
        move = True  # 開始移動
    
    if(move == True):
        motor.constantSpeed('forward', 0.02, 0.02)
    
        # 如果接受到 L
        if result == 'L':
            # 如果還沒轉 1 秒
            while(time.tick_ms() - turn_time) <= 1000:
                # 定速左轉
                motor.constantSpeed('left', 0.02, 0.02)
                
            motor.move(0, 0)
            time.sleep(0.8)
        # 如果接受到 R
        elif result == 'R':
            # 如果還沒轉 1 秒
            while(time.tick_ms() - turn_time) <= 1000:
                # 定速左轉
                motor.constantSpeed('right', 0.02, 0.02)
                
            motor.move(0, 0)
            time.sleep(0.8)
        
        # 如果接受到 B 
        if result == 'B':
            motor.move(0, 0)
            time.sleep(0.8)   # 避免前傾
            turn_time = time.tick_ms()
            # 如果還沒轉 1 秒
            while(time.tick_ms() - turn_time) <= 1000:
                # 定速左轉
                motor.constantSpeed('backward', 0.02, 0.02)
                
            motor.move(0, 0)
            time.sleep(0.8)
            
        elif result == 'S':
            motor.constantSpeed('stop', 0, 0)
            move = False
        result = ''