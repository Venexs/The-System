import pygame
import sys
import cv2
import numpy as np

# Initialize Pygame and OpenCV
pygame.init()

# Constants
WIDTH, HEIGHT = 1152, 648
WHITE = (255, 255, 255)
FONT_COLOR = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HUD Display")

# Fonts
font_large = pygame.font.SysFont("Montserrat Bold", 40)
font_small = pygame.font.SysFont("Montserrat Thin", 30)
font_bold = pygame.font.SysFont("Montserrat Bold", 40)
font_slant = pygame.font.SysFont("Montserrat", 30, italic=True)

# OpenCV Camera Capture


# Control variable
control = 0  # Set to 0 for black screen, 1 for video feed

# Functions to draw elements
def draw_text(surface, text, font, color, x, y, angle=0):
    text_surface = font.render(text, True, color)
    text_surface = pygame.transform.rotate(text_surface, angle)
    surface.blit(text_surface, (x, y))

def draw_ellipse(surface, color, x, y, width, height):
    pygame.draw.ellipse(surface, color, pygame.Rect(x - width // 2, y - height // 2, width, height), 2)  # 2-pixel thick ellipse

def draw_hud():
    # Display slanting HUD Text
    draw_text(screen, "Sung Jin-woo", font_large, FONT_COLOR, 50, 40, angle=-10)
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


# Main loop
clock = pygame.time.Clock()
running = True

if control==1:
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read frame from camera

    if control == 1:
        ret, frame = camera.read()
        # Convert frame to Pygame surface
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame_surface = pygame.surfarray.make_surface(frame)

        # Blit frame to screen
        screen.blit(pygame.transform.scale(frame_surface, (WIDTH, HEIGHT)), (0, 0))
    else:
        # Display black screen if control is 0
        screen.fill((0, 0, 0))

    # Draw HUD
    draw_hud()

    # Update screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

if control == 1:
    camera.release()
pygame.quit()
sys.exit()
