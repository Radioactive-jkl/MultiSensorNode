import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class NewGraph(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.axis = self.figure.add_subplot(111)
        self.line, = self.axis.plot([], [], color='blue')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack()

    def update_realtime_graph(self, input):
        x, y = self.line.get_data()
        if len(x) == 0:
            new_x = [0]
            new_y = [input]
        else:
            new_x = np.append(x, x[-1] + 1)
            new_y = np.append(y, input)
        self.line.set_data(new_x, new_y)

        self.axis = self.figure.gca()
        self.axis.relim()
        self.axis.autoscale_view()
        
        self.figure.canvas.draw()

def update_graph():
    new_window.update_realtime_graph(np.random.randint(0, 100))
    new_window.after(1000, update_graph)

if __name__ == '__main__':
    new_window = NewGraph()
    new_window.after(1000, update_graph)
    new_window.mainloop()