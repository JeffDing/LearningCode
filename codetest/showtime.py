from datetime import datetime
import pytz
#设置时区为北京时区
beijing_tz= pytz.timezone('Asia/shanghai')
#获取当前时间，并转为北京时间
current_beijing_time= datetime.now(beijing_tz)
#格式化时间输出
formatted_time = current_beijing_time.strftime('%y-%m-%d_%H:%M:%S')
print("当前北京时间:", formatted_time)
