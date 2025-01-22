import pygame
import sys
import cv2
import numpy as np
import speech_recognition as sr
import threading
import subprocess
import ujson
import time
from word2number import w2n

# Initialize Pygame and OpenCV
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720  # Reduced resolution for performance
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (255, 255, 255)
FPS = 24  # Lower frame rate for optimization
show_daily = False

# Face detection setup
face_cascade = cv2.CascadeClassifier('Files/Data/haarcascade_frontalface_default.xml')

# Global variables
user_name = None
face_detected = False

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption("System AR")

# Fonts
font_large = pygame.font.SysFont("Montserrat Bold", 40)
font_small = pygame.font.SysFont("Montserrat Thin", 30)
font_bold = pygame.font.SysFont("Montserrat Bold", 40)
font_slant = pygame.font.SysFont("Montserrat", 30, italic=True)

# Control variable
control = 0  # Set to 0 for black screen, 1 for video feed

def word_to_int(word):
    if isinstance(word, (int)):
        return word
    if isinstance(word, (float)):
        return int(word)
    else:
        try:
            # Try to convert the word to an integer using word2number library
            return w2n.word_to_num(word)
        except ValueError:
            print("Invalid number word")
            return None

# Functions to draw elements
def draw_text(surface, text, font, color, x, y, angle=0):
    text_surface = font.render(text, True, color)
    text_surface = pygame.transform.rotate(text_surface, angle)
    surface.blit(text_surface, (x, y))

def draw_ellipse(surface, color, x, y, width, height):
    pygame.draw.ellipse(surface, color, pygame.Rect(x - width // 2, y - height // 2, width, height), 2)  # 2-pixel thick ellipse

def draw_hud():
    global face_detected
    # Display slanting HUD Text
    draw_text(screen, "Sung Jinwoo", font_large, FONT_COLOR, 50, 40, angle=-10)
    draw_text(screen, "Title:", font_bold, FONT_COLOR, 50, 75, angle=-10)
    draw_text(screen, "Demon Slayer", font_small, FONT_COLOR, 120, 81, angle=-10)
    draw_text(screen, "Job:", font_bold, FONT_COLOR, 50, 110, angle=-10)
    draw_text(screen, "Shadow Monarch", font_small, FONT_COLOR, 115, 115, angle=-10)

    draw_text(screen, "Lv. 67", font_large, FONT_COLOR, 50, 150, angle=-10)

    # Display slanting date and time
    draw_text(screen, "06th January 2025", font_slant, FONT_COLOR, WIDTH - 250, 40, angle=15)
    draw_text(screen, "Monday", font_slant, FONT_COLOR, WIDTH - 250, 90, angle=15)

    # Display slanting HP and Fatigue
    draw_text(screen, "HP: XXXX", font_bold, FONT_COLOR, 50, HEIGHT - 80, angle=8)
    draw_text(screen, "Fatigue: XXX%", font_bold, FONT_COLOR, 200, HEIGHT - 100, angle=6)

    # Draw Curves around the HUD
    ellipse_width, ellipse_height = 1800, 600
    top_ellipse_y = int((HEIGHT / 2) - (550 * (HEIGHT / 648)))
    bottom_ellipse_y = int((HEIGHT / 2) + (550 * (HEIGHT / 648)))
    scaled_ellipse_width = int(ellipse_width * (WIDTH / 1152))
    scaled_ellipse_height = int(ellipse_height * (HEIGHT / 648))

    draw_ellipse(screen, WHITE, WIDTH // 2, top_ellipse_y, scaled_ellipse_width, scaled_ellipse_height)
    draw_ellipse(screen, WHITE, WIDTH // 2, bottom_ellipse_y, scaled_ellipse_width, scaled_ellipse_height)

# Voice Control Part
HOTKEY = "system"
COMMANDS = {
    "status": 1,
    "inventory": 2,
    "quests": 3,
    "skills": 5,
    "exit": 7,
}

# A flag to control the listening state
listening = True

# Add these global variables to store exercise values
push_val = 0
sit_val = 0
squats_val = 0
run_val = 0
daily_mode = False  # Flag for daily tracking mode

def recognize_speech():
    global show_daily, daily_mode
    global listening, running
    global push_val, sit_val, squats_val, run_val
    global user_name
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Thread started, listening for commands...")
    while listening and running:
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)

                # Recognize the speech
                command = recognizer.recognize_google(audio).lower().strip()
                print(f"Command received: {command}")  # Debug print

                # Check for HOTKEY and other commands
                if HOTKEY in command:
                    print("HOTKEY detected")

                    # Check for status and toggle daily mode
                    if "daily" in command:
                        show_daily = True
                        print("Status mode enabled")
                        daily_mode = not daily_mode
                        print(f"Daily mode {'enabled' if daily_mode else 'disabled'}", flush=True)
                    
                    if "system new identity" in command.lower() or "set name" in command.lower():
                        print("Please say your name:")
                        # Display prompt on screen (optional)
                        try:
                            with microphone as source:
                                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                                audio = recognizer.listen(source, timeout=5)
                                name = recognizer.recognize_google(audio).lower().strip()
                                user_name = name
                                print(f"New identity set: {user_name}")
                        except (sr.UnknownValueError, sr.WaitTimeoutError):
                            print("Name not recognized.")
                        except sr.RequestError as e:
                            print(f"Error with speech recognition service: {e}")

                # Process exercises if daily_mode is enabled
                if daily_mode:
                    print("Daily mode is active")
                    # Process exercise commands (without needing the 'add' keyword)

                    #! PUSHUPS
                    if "push up" in command:
                        try:
                            number = int(word_to_int(command.split("push up")[0].strip()))
                            push_val += number
                        except (ValueError, IndexError):
                            pass
                    elif "push-up" in command:
                        try:
                            number = int(word_to_int(command.split("push-up")[0].strip()))
                            push_val += number
                        except (ValueError, IndexError):
                            pass
                    elif "pushup" in command:
                        try:
                            number = int(word_to_int(command.split("pushup")[0].strip()))
                            push_val += number
                        except (ValueError, IndexError):
                            pass

                    #! SQUATS
                    if "squat" in command:
                        try:
                            number = int(word_to_int(command.split("push up")[0].strip()))
                            push_val += number
                        except (ValueError, IndexError):
                            pass
                    elif "squats" in command:
                        try:
                            number = int(word_to_int(command.split("push-up")[0].strip()))
                            push_val += number
                        except (ValueError, IndexError):
                            pass

                    #! SITUPS
                    elif "sit up" in command:
                        try:
                            number = int(word_to_int(command.split("sit up")[0].strip()))
                            sit_val += number
                        except (ValueError, IndexError):
                            pass
                    elif "situp" in command:
                        try:
                            number = int(word_to_int(command.split("situp")[0].strip()))
                            sit_val += number
                        except (ValueError, IndexError):
                            pass
                    elif "sit-up" in command:
                        try:
                            number = int(word_to_int(command.split("sit-up")[0].strip()))
                            sit_val += number
                        except (ValueError, IndexError):
                            pass

                    #! RUN
                    elif "run" in command:
                        try:
                            number = int(word_to_int(command.split("run")[0].strip()))
                            run_val += number
                        except (ValueError, IndexError):
                            pass

        except (sr.UnknownValueError, sr.WaitTimeoutError):
            print("No command detected or timeout")
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
        time.sleep(0.1)  # Reduce CPU usage

# Main loop
clock = pygame.time.Clock()
running = True

# Camera Initializing
if control == 1:
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, 15)

# Start the speech recognition thread
speech_thread = threading.Thread(target=recognize_speech, daemon=True)
speech_thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.RESIZABLE)

    # Read frame from camera
    if control == 1:
        ret, frame = camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (WIDTH, HEIGHT))  # Resize frame to match window dimensions
            frame = np.rot90(frame)
            unflipped_frame = cv2.flip(frame, 0)
            frame_surface = pygame.surfarray.make_surface(unflipped_frame)
            screen.blit(frame_surface, (0, 0))
    else:
        screen.fill((0, 0, 0))

    # Draw HUD
    draw_hud()
    if show_daily == True:
        rectangle_height = 500
        rectangle_width = 300  # Maintain the desired width
        rectangle_x = WIDTH - rectangle_width  # Calculate x to position right edge at WIDTH
        rectangle_y = HEIGHT // 2 - rectangle_height // 2
        pygame.draw.rect(screen, WHITE, (rectangle_x, rectangle_y, rectangle_width, rectangle_height))
        
        #Pushups
        pushups_text_x = rectangle_x + (rectangle_width // 2) - 130
        pushups_text_y = rectangle_y + (rectangle_height // 2) - 170

        pushups_val_text_x = rectangle_x + (rectangle_width // 2) - 0
        pushups_val_text_y = rectangle_y + (rectangle_height // 2) - 170

        draw_text(screen, "Pushups", font_bold, BLACK, pushups_text_x, pushups_text_y)
        draw_text(screen, f"[{push_val}/100]", font_bold, BLACK, pushups_val_text_x, pushups_val_text_y)

        #Situps
        situps_text_x = rectangle_x + (rectangle_width // 2) - 130
        situps_text_y = rectangle_y + (rectangle_height // 2) - 120

        situps_val_text_x = rectangle_x + (rectangle_width // 2) - 0
        situps_val_text_y = rectangle_y + (rectangle_height // 2) - 120

        draw_text(screen, "Situps", font_bold, BLACK, situps_text_x, situps_text_y)
        draw_text(screen, f"[{sit_val}/100]", font_bold, BLACK, situps_val_text_x, situps_val_text_y)

        #Squats
        squats_text_x = rectangle_x + (rectangle_width // 2) - 130
        squats_text_y = rectangle_y + (rectangle_height // 2) - 70

        squats_val_text_x = rectangle_x + (rectangle_width // 2) - 0
        squats_val_text_y = rectangle_y + (rectangle_height // 2) - 70

        draw_text(screen, "Squats", font_bold, BLACK, squats_text_x, squats_text_y)
        draw_text(screen, f"[{squats_val}/100]", font_bold, BLACK, squats_val_text_x, squats_val_text_y)

        #Run
        run_text_x = rectangle_x + (rectangle_width // 2) - 130
        run_text_y = rectangle_y + (rectangle_height // 2) - 20

        run_val_text_x = rectangle_x + (rectangle_width // 2) - 0
        run_val_text_y = rectangle_y + (rectangle_height // 2) - 20

        draw_text(screen, "Run", font_bold, BLACK, run_text_x, run_text_y)
        draw_text(screen, f"[{run_val}/10]", font_bold, BLACK, run_val_text_x, run_val_text_y)

    # Update screen
    pygame.display.flip()
    clock.tick(FPS)


if control == 1:
    camera.release()
listening = False  # Stop the speech recognition thread
speech_thread.join()
pygame.quit()
sys.exit()
