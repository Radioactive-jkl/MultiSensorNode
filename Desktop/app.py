# std
import tkinter as tk
# project
from graph import NewGraph

class MultiNodeApp(tk.Tk):
    def __init__(self, master = None):
        super().__init__()
        # bsae
        self.master = master
        self.title("MultiNodeApp")
        self.geometry("585x385")
        self.configure(background="white")

        self.color = ["#037EF3", "#f85a40", "#00c16e", "#52565E", "#52565E", "#52565E"]
        self.running = [0,0,0,0,0,0]
        self.message_count1 = 0
        self.message_count2 = 0

        # node1
        self.Temperature1 = 0
        self.Humidity1 = 0
        self.BatteryPercentage1 = 0
        self.LightLux1 = 0
        self.LightLuxstd1 = 0.0
        self.LightLuxle1 = False
        self.LightLuxpe1 = False
        self.Smoke1 = 0
        self.Smokele1 = False
        self.Smokepe1 = False

        # node2
        self.Temperature2 = 0
        self.Humidity2 = 0
        self.BatteryPercentage2 = 0
        self.LightLux2 = 0
        self.LightLuxstd2 = 0.0
        self.LightLuxle2 = False
        self.LightLuxpe2 = False
        self.Smoke2 = 0
        self.Smokele2 = False
        self.Smokepe2 = False

        # graph
        self.numb = 0

        # buttons
        self.window_opened = False
        self.graph_opened = False

        self.button0 = tk.Button(
                    self,
                    text="Settings\nView",
                    width=25, height=10,
                    background=self.color[0],
                    relief="flat", overrelief="sunken",
                    command=lambda: self.create_window(0)
                    )
        self.button0.grid(row=0, column=0, padx=5, pady=5)

        self.button1 = tk.Button(
                    self,
                    text="NODE1\nClosed",
                    width=25, height=10, 
                    background=self.color[1],
                    relief="flat", overrelief="sunken",
                    command=lambda: self.create_window(1)
                    )
        self.button1.grid(row=0, column=1, padx=5, pady=5)

        self.button2 = tk.Button(
                    self,
                    text="NODE2\nClosed",
                    width=25, height=10, 
                    background=self.color[2], 
                    relief="flat", overrelief="sunken",
                    command=lambda: self.create_window(2)
                    )
        self.button2.grid(row=0, column=2, padx=5, pady=5)

        self.button3 = tk.Button(
                    self,
                    text="NODE3\nClosed",
                    width=25, height=10, 
                    background=self.color[3], 
                    relief="flat", overrelief="sunken",
                    command=lambda: self.create_window(3)
                    )
        self.button3.grid(row=1, column=0, padx=5, pady=5)

        self.button4 = tk.Button(
                    self,
                    text="NODE4\nClosed",
                    width=25, height=10, 
                    background=self.color[4], 
                    relief="flat", overrelief="sunken",
                    command=lambda: self.create_window(4)
                    )
        self.button4.grid(row=1, column=1, padx=5, pady=5)

        self.button5 = tk.Button(
                    self,
                    text="Unused",
                    width=25, height=10, 
                    background=self.color[5], 
                    relief="flat", overrelief="sunken",
                    command=lambda: self.create_window(5)
                    )
        self.button5.grid(row=1, column=2, padx=5, pady=5)


    def update_message(self, str_message):
        device, message = str_message['deviceName'], str_message['items']
        if (device == "Node1"):
            try:
                self.Temperature1 = message['temperature1']['value']
                self.Humidity1 = message['humidity1']['value']
                self.Smoke1 = message['smokescope1']['value']
                self.Smokele1 = message['smokescopele1']['value']
                self.Smokepe1 = message['smokescopepe1']['value']
                self.LightLux1 = message['illumination1']['value']
                self.LightLuxstd1 = message['illuminationstd1']['value']
                self.LightLuxle1 = message['illuminationle1']['value']
                self.LightLuxpe1 = message['illuminationpe1']['value']
                self.BatteryPercentage1 = message['battery1']['value']
                
                self.message_count1 = 0
                self.running[1] = 1
                text1 = "NODE1: Running\n"
                text1 = text1 + "Temperature: "     + str(self.Temperature1) + "\n"
                text1 = text1 + "Humidity: "     + str(self.Humidity1) + "\n"
                text1 = text1 + "LightLux: "     + str(self.LightLux1) + "±" + str(self.LightLuxstd1) + " LE:" + str(self.LightLuxle1) + " PE:" + str(self.LightLuxpe1) + "\n"
                text1 = text1 + "Smokescope: "     + str(self.Smoke1) + " LE:" + str(self.Smokele1) + " PE:" + str(self.Smokepe1) + "\n"
                text1 = text1 + "BatteryPer: "     + str(self.BatteryPercentage1) + "\n"
                
                self.button1.configure(text=text1, bg=self.color[1], anchor='w')

            except:
                self.message_count1 += 1
                
        elif (device == "Node2"):
            try:
                self.Temperature2 = message['temperature2']['value']
                self.Humidity2 = message['humidity2']['value']
                self.Smoke2 = message['smokescope2']['value']
                self.Smokele2 = message['smokescopele2']['value']
                self.Smokepe2 = message['smokescopepe2']['value']
                self.LightLux2 = message['illumination2']['value']
                self.LightLuxstd2 = message['illuminationstd2']['value']
                self.LightLuxle2 = message['illuminationle2']['value']
                self.LightLuxpe2 = message['illuminationpe2']['value']
                self.BatteryPercentage2 = message['battery2']['value']
                
                self.message_count2 = 0
                self.running[2] = 1
                text2 = "NODE2: Running\n"
                text2 = text2 + "Temperature: "     + str(self.Temperature2) + "\n"
                text2 = text2 + "Humidity   : "     + str(self.Humidity2) + "\n"
                text2 = text2 + "LightLux: "     + str(self.LightLux2) + "±" + str(self.LightLuxstd2) + " LE:" + str(self.LightLuxle2) + " PE:" + str(self.LightLuxpe2) + "\n"
                text2 = text2 + "Smokescope: "     + str(self.Smoke2) + " LE:" + str(self.Smokele2) + " PE:" + str(self.Smokepe2) + "\n"
                text2 = text2 + "BatteryPer : "     + str(self.BatteryPercentage2) + "\n"
            
                self.button2.configure(text=text2, bg=self.color[2], anchor='w')

            except:
                self.message_count2 += 1


    def create_window(self, num):
        if not self.window_opened:
            self.window_opened = True
            self.new_window = tk.Toplevel(self.master)
            #self.new_window.configure(background="white")
            self.new_window.protocol('WM_DELETE_WINDOW', self.on_window_close)
            if   num == 0:
                self.new_window.title("Settings")
                self.new_window.geometry("385x385")
                self.label = tk.Label(
                    self.new_window, 
                    text="HOST:\n" + "iot-06z00itmv0vajzw.\nmqtt.iothub.aliyuncs.com" + "\n" 
                    + "\nPORT: 1883" + "\n" 
                    + "DEV_ID:\njk3pz9zX1pF.longxinpi|securemode=2,\nsignmethod=hmacsha256,\ntimestamp=1688816652077|\n" 
                    + "PRO_ID:\nlongxinpi&jk3pz9zX1pF\n",
                    anchor='w'
                    )
                self.label.grid()
                
            else:
                if not((num == 1 and self.running[num] == 1) or (num == 2 and self.running[num] == 1)):
                    self.new_window.title("WARNING")
                    self.label = tk.Label(self.new_window, text="Unable to use!", anchor='center')
                    self.label.grid()

                else:    
                    if num == 1 and self.running[num] == 1:
                        self.new_window.title("NODE1")

                    elif num == 2 and self.running[num] == 1:
                        self.new_window.title("NODE2")
                    
                    self.new_window.geometry("385x385")
                    self.new_window.button0 = tk.Button(
                                self.new_window,
                                text="temp",
                                width=25, height=10,
                                background=self.color[0],
                                relief="flat", overrelief="sunken",
                                command=lambda: self.create_graph((num-1)*4+0)
                                )
                    self.new_window.button0.grid(row=0, column=0, padx=5, pady=5)

                    self.new_window.button1 = tk.Button(
                                self.new_window,
                                text="humi",
                                width=25, height=10, 
                                background=self.color[1],
                                relief="flat", overrelief="sunken",
                                command=lambda: self.create_graph((num-1)*4+1)
                                )
                    self.new_window.button1.grid(row=0, column=1, padx=5, pady=5)

                    self.new_window.button2 = tk.Button(
                                self.new_window,
                                text="smoke",
                                width=25, height=10, 
                                background=self.color[2], 
                                relief="flat", overrelief="sunken",
                                command=lambda: self.create_graph((num-1)*4+2)
                                )
                    self.new_window.button2.grid(row=1, column=0, padx=5, pady=5)

                    self.new_window.button3 = tk.Button(
                                self.new_window,
                                text="light",
                                width=25, height=10, 
                                background=self.color[3], 
                                relief="flat", overrelief="sunken",
                                command=lambda: self.create_graph((num-1)*4+3)
                                )
                    self.new_window.button3.grid(row=1, column=1, padx=5, pady=5)


    def on_window_close(self):
        self.window_opened = False
        self.new_window.destroy()

    def create_graph(self, num):
        if not self.graph_opened:
            self.graph_opened = True
            self.new_graph = NewGraph()
            self.new_graph.protocol('WM_DELETE_WINDOW', self.on_graph_close)
            if num%4 == 0:
                self.new_graph.title("temp")
            if num%4 == 1:
                self.new_graph.title("humi")
            if num%4 == 2:
                self.new_graph.title("smoke")
            if num%4 == 3:
                self.new_graph.title("light")

            self.numb = num

    def on_graph_close(self):
        self.graph_opened = False
        self.new_graph.destroy()
