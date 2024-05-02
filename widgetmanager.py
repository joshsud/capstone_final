import tkinter as tk
from tkinter import simpledialog as sd, messagebox as mb, filedialog
import importlib.util, os, inspect

class WidgetManager:
    def __init__(self, master):
        self.master = master
        self.widget_frames = {}

    def add_widget_frame(self, widget_name, widget_frame):
        if widget_name in self.widget_frames:
            return False 
        self.widget_frames[widget_name] = widget_frame
        return True

    def remove_widget_frame(self, widget_name):
        if widget_name in self.widget_frames:
            widget_frame = self.widget_frames.pop(widget_name)
            widget_frame.destroy()

    def update_widget_listbox(self):
        widget_listbox.delete(0, tk.END)
        for widget_name in self.widget_frames:
            widget_listbox.insert(tk.END, widget_name)

    def display_widget(self, widget_name):
        widget_frame = self.widget_frames.get(widget_name)
        if widget_frame:
            widget_frame.pack(fill=tk.BOTH, expand=True)
        else:
            mb.showerror("Error", "Widget not found")

    def hide_widget(self, widget_name):
        widget_frame = self.widget_frames.get(widget_name)
        if widget_frame:
            widget_frame.pack_forget()

def import_widget():
    widget_path = filedialog.askopenfilename(title="Select Widget File", filetypes=[("Python Files", "*.py")])
    if widget_path:
        widget_module_name = os.path.basename(widget_path).split(".")[0]
        spec = importlib.util.spec_from_file_location(widget_module_name, widget_path)
        widget_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(widget_module)

        widget_classes = [cls for name, cls in inspect.getmembers(widget_module, inspect.isclass)]
        user_input = sd.askstring("Widget Name", "Enter a name for your widget:")
        if user_input:
            widget_name = user_input
            if widget_name in widget_manager.widget_frames:
                mb.showerror("Error", "That widget is already added.")
                return
        else:
            mb.showerror("Error", "Please input a name for the widget.")
            return

        for widget_class in widget_classes:
            # Class needs to have widget framework
            if issubclass(widget_class, globals().get('Widget', object)):
                widget_instance = widget_class(right_frame, widget_manager, widget_name)
                widget_manager.add_widget_frame(widget_name, widget_instance.frame)
                widget_manager.update_widget_listbox()

        if not widget_manager.widget_frames:
            mb.showerror("Error", "No valid widget class found in the module.")

def display_selected_widget():
    selected_widget = widget_listbox.curselection()
    if selected_widget:
        widget_name = widget_listbox.get(selected_widget)
        widget_manager.display_widget(widget_name)

def hide_selected_widget():
    selected_widget = widget_listbox.curselection()
    if selected_widget:
        widget_name = widget_listbox.get(selected_widget)
        widget_manager.hide_widget(widget_name)

def display_help():
    help_text = """
    Welcome to my Widget Manager Application!

    To use the application, you can:
    - Import a widget by clicking 'Import Widget' and selecting a Python file,
        -Note: it has to have the widget subclass. Instructions on what to include is found under
            "How To!"
    - Display a widget by selecting it and clicking 'Display Widget'.
    - Hide a displayed widget by selecting it and clicking 'Hide Widget'.
    """
    mb.showinfo("Help", help_text)

def display_how_to():
    help_text = """
    In order to create a widget, you can copy the framework and make a couple edits, and add to the subclass within.
    The edits that have to be made:
        In the main, change the name of the widgets to the name of your new widget subclass
        Change the name of your widget subclass to match the new widget name
    Thats it!
    You can create your widget in the subclass, the framework already allows the widget to display in the application.
    """
    mb.showinfo("How To", help_text)

def display_framework():
    framework_text = """
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

# Change Calculator to Widget subclass name of choosing
class CalculatorWidget(Widget):

def main():
    root = tk.Tk()
    widget_manager = WidgetManager(root)

    # Change Calculator to Widget name of choosing
    calculator_widget = CalculatorWidget(root, widget_manager, "Calculator") 
    calculator_widget.display()

    root.mainloop()

if __name__ == "__main__":
    main()
"""
    framework_window = tk.Toplevel()
    framework_window.title("Framework")
    framework_window.geometry("600x400")
    framework_textbox = tk.Text(framework_window, wrap="word", font=("Arial", 12))
    framework_textbox.pack(fill="both", expand=True)
    framework_textbox.insert("1.0", framework_text)
    framework_textbox.config(state="disabled")

root = tk.Tk()
root.title("Widget Manager")
root.geometry("600x750")  

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Display Help", command=display_help)
help_menu.add_command(label="How to", command=display_how_to)
help_menu.add_command(label="Framework", command=display_framework)

widget_manager = WidgetManager(root)

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

import_button = tk.Button(left_frame, text="Import Widget", command=import_widget, font=('Arial', 12))
import_button.pack(side=tk.TOP, padx=10, pady=10)
display_button = tk.Button(left_frame, text="Display Widget", command=display_selected_widget, font=('Arial', 12))
display_button.pack(side=tk.TOP, padx=10, pady=10)
hide_button = tk.Button(left_frame, text="Hide Widget", command=hide_selected_widget, font=('Arial', 12))
hide_button.pack(side=tk.TOP, padx=10, pady=10)

# Widget Listbox to select widget
widget_listbox = tk.Listbox(left_frame, font=('Arial', 12))
widget_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Right Frame (Display Frame for Widgets)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.mainloop()