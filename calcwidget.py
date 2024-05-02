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

class CalculatorWidget(Widget):
    def __init__(self, master, widget_manager, widget_name):
        super().__init__(master, widget_manager, widget_name)

        self.calculator_frame = tk.Frame(self.frame)
        self.calculator_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        self.entry = tk.Entry(self.calculator_frame, width=20, font=('Arial', 13)) 
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew") 

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('C', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('%', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('^', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('sqrt', 4, 4) 
        ]

        for (text, row, column) in buttons:
            button = tk.Button(self.calculator_frame, text=text, width=5, height=2, font=('Arial', 14), command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=column, padx=5, pady=5)

    def on_button_click(self, char):
        if char == '=':
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        elif char == 'C':
            self.entry.delete(0, tk.END)
        elif char == '^':
            self.entry.insert(tk.END, "**")
        elif char == 'sqrt':
            self.entry.insert(tk.END, "**0.5")
        else:
            self.entry.insert(tk.END, char)

def main():
    root = tk.Tk()
    widget_manager = WidgetManager(root)

    calculator_widget = CalculatorWidget(root, widget_manager, "Calculator") 
    calculator_widget.display()

    root.mainloop()

if __name__ == "__main__":
    main()