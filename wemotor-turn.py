# 匯入馬達模組
import wemotor
import time

# 建立馬達物件
motor = wemotor.Motor()

motor.move(20, 80)   # 右轉
time.sleep(1)        # 暫停1秒
motor.move(80, 20)   # 左轉
time.sleep(1)        # 暫停1秒  
motor.move(0, 0)     # 停止