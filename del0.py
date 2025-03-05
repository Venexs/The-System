import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Custom Dropdown")
root.geometry("300x200")  # Set window size

# Custom font
custom_font = ("Arial", 14)

# Create a Combobox
combo = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"], font=custom_font)
combo.set("Select an option")  # Default text

# Adjust width of combobox
combo["width"] = 15  # Width in characters

# Start the GUI event loop
root.mainloop()
