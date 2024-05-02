from math import cos, sin, pi
from datetime import datetime
import tkinter as tk

class Widget:
    def __init__(self, master, widget_manager, widget_name):
        self.master = master
        self.widget_manager = widget_manager
        self.widget_name = widget_name

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.widget_manager.add_widget_frame(self.widget_name, self.frame)
        self.widget_manager.update_widget_listbox()

        self.window_tag = f"widget_{self.widget_name}"
        self.frame.window_tag = self.window_tag

    def display(self):
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

class ClockWidget(Widget):
    def __init__(self, master, widget_manager, widget_name):
        super().__init__(master, widget_manager, widget_name)

        self.canvas = tk.Canvas(self.frame, width=200, height=200, bg="white")
        self.canvas.pack(expand=True)

        self.update_clock()

    def update_clock(self):
        self.canvas.delete("clock_hand")

        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second

        hour_angle = pi / 2 - (hour * 30 + minute * 0.5) * (pi / 180)
        minute_angle = pi / 2 - minute * 6 * (pi / 180)
        second_angle = pi / 2 - second * 6 * (pi / 180)
        self.canvas.create_oval(50, 50, 150, 150, outline="black")

        hour_hand_length = 30
        hour_hand_x = 100 + hour_hand_length * cos(hour_angle)
        hour_hand_y = 100 - hour_hand_length * sin(hour_angle)
        self.canvas.create_line(100, 100, hour_hand_x, hour_hand_y, tags="clock_hand", fill="black", width=3)

        minute_hand_length = 40
        minute_hand_x = 100 + minute_hand_length * cos(minute_angle)
        minute_hand_y = 100 - minute_hand_length * sin(minute_angle)
        self.canvas.create_line(100, 100, minute_hand_x, minute_hand_y, tags="clock_hand", fill="black", width=2)

        second_hand_length = 45
        second_hand_x = 100 + second_hand_length * cos(second_angle)
        second_hand_y = 100 - second_hand_length * sin(second_angle)
        self.canvas.create_line(100, 100, second_hand_x, second_hand_y, tags="clock_hand", fill="red", width=1)


        self.canvas.after(1000, self.update_clock)

def main():
    root = tk.Tk()
    widget_manager = WidgetManager(root)

    clock_widget = ClockWidget(root, widget_manager, "Clock")
    clock_widget.display()

    root.mainloop()

if __name__ == "__main__":
    main()