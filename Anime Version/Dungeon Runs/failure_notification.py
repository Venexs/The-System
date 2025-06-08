import tkinter as tk
from tkinter import Toplevel, Frame, Label, Button, Canvas
import random
import json
import os
import sys
from pathlib import Path

class ShadowExtractionFailure:
    def __init__(self, parent_window, boss_name, transp_clr):
        self.parent_window = parent_window
        self.boss_name = boss_name
        self.transp_clr = transp_clr
        self.create_failure_window()
    
    def create_failure_window(self):
        # Create failure window
        self.failure_window = Toplevel(self.parent_window)
        self.failure_window.title("Extraction Failed")
        self.failure_window.geometry("500x300")
        self.failure_window.configure(bg="#1E1E1E")
        self.failure_window.overrideredirect(True)
        
        # Create canvas
        self.canvas = Canvas(
            self.failure_window,
            bg="#1E1E1E",
            height=300,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Top and bottom colored bars
        self.canvas.create_rectangle(0.0, 0.0, 500.0, 30.0, fill="#AA0000", outline="")
        self.canvas.create_rectangle(0.0, 270.0, 500.0, 300.0, fill="#AA0000", outline="")
        
        # Failure messages
        failure_titles = [
            "SHADOW EXTRACTION FAILED",
            "EXTRACTION PROCESS DISRUPTED",
            "SHADOW RESISTED EXTRACTION",
            "EXTRACTION ATTEMPT REJECTED",
            "SHADOW BOND UNSTABLE"
        ]
        
        failure_details = [
            f"The {self.boss_name}'s shadow refused to submit to your control.",
            f"The {self.boss_name}'s will was too strong to be dominated.",
            f"The shadow extraction process was disrupted by lingering magic.",
            f"Your connection to the shadow realm is currently weakened.",
            f"The {self.boss_name}'s essence is incompatible with your shadow army."
        ]
        
        failure_advice = [
            "Try extracting from a weaker enemy or improve your shadow mastery.",
            "Perhaps your shadow control abilities need more practice.",
            "Consider strengthening your connection to the shadow realm.",
            "Some enemies resist extraction. Seek more compatible targets.",
            "Your power may not yet be sufficient to control this type of shadow."
        ]
        
        # Randomly select messages
        title = random.choice(failure_titles)
        detail = random.choice(failure_details)
        advice = random.choice(failure_advice)
        
        # Create failure icon
        self.canvas.create_oval(
            225, 60, 275, 110,
            fill="#AA0000",
            outline="#FF0000"
        )
        
        self.canvas.create_text(
            250, 85,
            text="✖",
            fill="#FFFFFF",
            font=("Montserrat Bold", 28),
            anchor="center"
        )
        
        # Create failure title
        self.canvas.create_text(
            250, 130,
            text=title,
            fill="#FF0000",
            font=("Montserrat Bold", 16),
            anchor="center"
        )
        
        # Create failure details
        self.canvas.create_text(
            250, 170,
            text=detail,
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            width=400,
            anchor="center"
        )
        
        # Create advice
        self.canvas.create_text(
            250, 210,
            text=advice,
            fill="#AAAAAA",
            font=("Montserrat Italic", 12),
            width=400,
            anchor="center"
        )
        
        # Create close button
        close_button = Button(
            self.failure_window,
            text="Close",
            bg="#333333",
            fg="#FFFFFF",
            font=("Montserrat Regular", 12),
            command=self.failure_window.destroy,
            width=10,
            height=1
        )
        close_button.place(x=200, y=240)
        
        # Center the window
        self.failure_window.geometry("+%d+%d" % (
            self.parent_window.winfo_rootx() + 100,
            self.parent_window.winfo_rooty() + 100
        ))
        
        # Make window modal
        self.failure_window.transient(self.parent_window)
        self.failure_window.grab_set()

# For testing as standalone
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    ShadowExtractionFailure(root, "Dragon Lord", "#652AA3")
    root.mainloop()
