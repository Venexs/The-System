import cv2
from tkinter import Tk, Canvas, PhotoImage
from PIL import Image, ImageTk
import threading
import time

def play_video():
    def video_loop():
        # Set the playback speed (lower FPS for slower playback)
        playback_speed = 15  # Frames per second (e.g., 15 FPS)
        frame_delay = 1 / playback_speed  # Delay in seconds between frames

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Resize the frame to 860x52
                frame = cv2.resize(frame, (860, 52))

                # Convert the frame to RGB format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert the frame to a format Tkinter can use
                frame_image = ImageTk.PhotoImage(Image.fromarray(frame))

                # Update the canvas image
                canvas.itemconfig(video_item, image=frame_image)
                canvas.image = frame_image  # Keep a reference to avoid garbage collection

                # Wait to control playback speed
                time.sleep(frame_delay)
            else:
                # Restart the video once it ends
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Run the video loop in a thread
    threading.Thread(target=video_loop, daemon=True).start()

# Initialize the Tkinter window
root = Tk()
root.geometry("800x600")
root.wm_attributes('-transparentcolor', "#0c709c")

# Create a Canvas to place the video
canvas = Canvas(root, width=800, height=600)
canvas.pack()

# Create an empty image element in the Canvas
video_item = canvas.create_image(400, 300, anchor="center", image=None)

# Load the video
video_path = "path_to_your_video.mp4"  # Replace with your video path
cap = cv2.VideoCapture(video_path)

# Start the video loop in a separate thread
play_video()

# Run the Tkinter main loop
root.mainloop()

# Release the video resources when the window is closed
cap.release()
cv2.destroyAllWindows()
