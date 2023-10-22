# Imports

## std
import json
import queue
import smtplib
from email.mime.text import MIMEText
import winsound
## 3p
import paho.mqtt.client as mqtt
## project
from app import MultiNodeApp

# Setting Information

## E-mail Settings
from_addr = 'youremail'
password = 'xxxxxxxxx'
to_addr = 'receiver'
smtp_server = 'smtp.qq.com'
port = 465

### E-mail Content
html_msg = """
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>系统通知邮件</title>
</head>

<body>
    <div style="font-size: 14px;">
        <br><br><br><br>
        <div style="width: 600px; margin: 0 auto; background-color: #00838a; border-radius: 3px;">
            <div style="padding: 0 15px; padding-bottom: 20px;">
                <div style="height: 72px;">
                    <div>
                        <a href="https://mall.bydauto.com.cn/" target="_blank" rel="noopener"
                            style="text-decoration: none;">
                            <img src="https://mall.bydauto.com.cn/pc/_nuxt/img/logo.97a8e60.svg" style="height: 72px;"
                                alt="BYD" title="BYD">
                        </a>
                    </div>
                </div>
                <div style="background: #fff; padding: 20px 15px; border-radius: 3px;">
                    <div><span style="font-size: 20px; font-weight: bold;">风险预警：</span>
                        <div style="line-height: 24px; margin-top: 10px;">
                            <div>
                                您的半导体无尘车间出现
                                <span style="font-weight: bold;">有机气体浓度超标</span>
                                待办，编号为“
                                <span style="font-weight: bold;">XJ230708005</span>
                                ”，收到信息后请尽快
                                <a style="color: #006eff;font-weight: bold;" href="https://mall.bydauto.com.cn/"
                                    target="_blank" rel="noopener">登录监测系统</a>查看并安排处理！
                            </div>
                        </div>
                    </div>
                    <div style="margin-top: 30px;">
                        <div><span
                                style="font-size: 20px; font-weight: bold; position: relative; top: -4px;">详细信息:</span>
                        </div>
                        <table
                            style="width: 400px; border-spacing: 0px; border-collapse: collapse; border: none; margin-top: 20px;">
                            <tbody>
                                <tr style="height: 45px;">
                                    <td
                                        style="width: 150px; height: 40px; background: #F6F6F6;border: 1px solid #DBDBDB; font-size: 14px; font-weight: normal; text-align: left; padding-left: 14px;">
                                        异常节点</td>
                                    <td
                                        style="width: 250px;height: 40px; border: 1px solid #DBDBDB; font-size: 14px; font-weight: normal; text-align: left; padding-left: 14px;">
                                        NODE1</td>
                                </tr>
                                <tr style="height: 45px;">
                                    <td
                                        style="width: 150px;height: 40px; background: #F6F6F6;border: 1px solid #DBDBDB; font-size: 14px; font-weight: normal; text-align: left; padding-left: 14px;">
                                        异常参数</td>
                                    <td
                                        style="width: 250px;height: 40px; border: 1px solid #DBDBDB; font-size: 14px; font-weight: normal; text-align: left; padding-left: 14px;">
                                        有机分子浓度</td>
                                </tr>
                                <tr style="height: 45px;">
                                    <td
                                        style="width: 150px; height: 40px; background: #F6F6F6;border: 1px solid #DBDBDB; font-size: 14px; font-weight: normal; text-align: left; padding-left: 14px;">
                                        异常数值</td>
                                    <td
                                        style="width: 250px;height: 40px; border: 1px solid #DBDBDB; font-size: 14px; font-weight: normal; text-align: left; padding-left: 14px;">
                                        <a style="color: #006eff;" href="https://mall.bydauto.com.cn/" target="_blank"
                                            rel="noopener">42.51</a>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div style="margin-top: 60px;margin-bottom: 10px;"><span
                            style="font-size: 16px; font-weight: bold; color: #666;">温馨提醒</span>
                        <div style="line-height: 24px; margin-top: 10px;">
                            <div style="font-size: 13px; color: #666;">使用过程中如有任何问题，请联系系统管理员Radioactive。</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div
            style="width: 600px; margin: 0 auto;  margin-top: 50px; font-size: 12px; -webkit-font-smoothing: subpixel-antialiased; text-size-adjust: 100%;">
            <p
                style="text-align: center; line-height: 20.4px; text-size-adjust: 100%; font-family: 'Microsoft YaHei'!important; padding: 0px !important; margin: 0px !important; color: #7e8890 !important;">
                <span class="appleLinks">
                    Copyright © 2023-2024 武汉Radioactive科技股份有限公司. 保留所有权利。</span>
            </p>
            <p
                style="text-align: center;line-height: 20.4px; text-size-adjust: 100%; font-family: 'Microsoft YaHei'!important; padding: 0px !important; margin: 0px; color: #7e8890 !important; margin-top: 10px;">
                <span class="appleLinks">
                    邮件由系统自动发送，请勿直接回复本邮件！</span>
            </p>
        </div>
    </div>
</body>

</html>
"""
msg = MIMEText(html_msg, 'html', 'utf-8')
### Message Header
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = 'MULTINODE WARNING'

## MQTT Settings
PORT=1883
HOST=r"iot-xxxxxxxxxxxx.mqtt.iothub.aliyuncs.com"
DEV_ID = r"xxxxxxxxxx.Desktop|securemode=2,signmethod=hmacsha256,timestamp=xxxxxxxxxxx|" 
PRO_ID = r"xxxxxxxxxx" 
AUTH_INFO = r"xxxxxxxxxxxxxxxxxxxxx"
TOPIC = r"/sys/xxxxxxxxxx/xxxxxxxxx/thing/service/property/set"


# MQTT Functions

## The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

## The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic)
    str = json.loads(msg.payload)
    #print(str)
    q_ali.put(str)


# APP Functions

## Refresh APP data at 10Hz
def update_data():
    #print(q_ali.qsize())

    if q_ali.qsize() != 0: 
        message = q_ali.get()
        app.update_message(str_message=message)

    else:
        app.message_count1 += 1
        app.message_count2 += 1


    if app.message_count1 >= 100:
        app.message_count1 = 0
        app.running[1] = 0
        app.button1.configure(text="NODE1\nClosed", bg=app.color[5], anchor="center")

    if app.message_count2 >= 100:
        app.message_count2 = 0
        app.running[2] = 0
        app.button2.configure(text="NODE2\nClosed", bg=app.color[5], anchor="center")
    
    app.after(100, update_data)

## Refresh graphs at 1Hz
def update_graph_data():
    if app.graph_opened ==True:
        if app.numb == 0:
            y = app.Temperature1
        if app.numb == 1:
            y = app.Humidity1
        if app.numb == 2:
            y = app.Smoke1
        if app.numb == 3:
            y = app.LightLux1
        if app.numb == 4:
            y = app.Temperature2
        if app.numb == 5:
            y = app.Humidity2
        if app.numb == 6:
            y = app.Smoke2
        if app.numb == 7:
            y = app.LightLux2
            
        app.new_graph.update_realtime_graph(y)
    app.after(1000, update_graph_data)

## Check thresholds at 0.2Hz
def gasWarning():
    if app.Smoke1 > 40.0:
        return True
    
    if app.Smoke2 > 40.0:
        return True

def update_warning():
    if gasWarning() == True:
        try:
            smtpobj = smtplib.SMTP_SSL(smtp_server, port)
            # connect
            smtpobj.connect(smtp_server, port)    
            # login
            smtpobj.login(from_addr, password)   
            # send
            smtpobj.sendmail(from_addr, to_addr, msg.as_string()) 
            print("Succeeded To Send")
        except smtplib.SMTPException:
            print("Failed To Send")
        finally:
            # Shut Down
            smtpobj.quit()
        
        winsound.PlaySound('iphone.wav', winsound.SND_NODEFAULT)
    
    app.after(5000, update_warning)


# Main Function

if __name__ == '__main__':

    ## message
    q_ali = queue.Queue()

    ## Client Initialization
    client = mqtt.Client(DEV_ID)
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.username_pw_set(PRO_ID,AUTH_INFO)
    client.connect(HOST, PORT, 90)
    client.loop_start()

    ## App Initialization
    app = MultiNodeApp()
    app.after(100, update_data)
    app.after(1000, update_graph_data)
    app.after(1000, update_warning)
    app.mainloop()

    ## Loop
    while True:
        pass
