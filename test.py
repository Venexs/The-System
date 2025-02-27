from mistralai import Mistral
from mistralai.models import UserMessage
import os
from PIL import Image



# Initialize Mistral client
MISTRAL_API_KEY = "KSfbpbCqw1EOX5AVMoMUYfPBGRiSoylj"
mistral_client = Mistral(api_key=MISTRAL_API_KEY)



# Define a prompt that avoids existing elements and focuses on a new workout module
prompt = """
Generate new Python script for a Solo Leveling system feature inside my solo leveling system app using tkinter.
This script should:
- Use the assets/frame1 path for images, the images include:

button_9.png: close window button
button_1.png: + button, for add buttons and stuff
button_2.png: a checkbox
button_3.png: a warning/danger alert

DONT ADD ANY IMAGES THAT ARENT in that list!

- Introduce a new feature, create something unique.
- Make something gamified rpg solo leveling style like a complex rpg workout dungeon. IT NEEDS TO BE UNIQUE THOUGH.
- Make sure the images have a transparent background.
- It needs to follow the solo leveling color scheme, all rectangles need to be black, and text needs to be white.
- MAKE SURE NOTHING OVERLAPS.
"""

# Load an image file (Change the path to your actual image)
image_path = "assets/assets_list.png"

def generate_text():
    response = mistral_client.agents.complete(
        agent_id="ag:debe4322:20250219:ashborn-v1:892933ab",
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            },
        ],
    )

    return response.choices[0].message.content
    
try:
    # Open the image using PIL
    image = Image.open(image_path)


    response = generate_text()
    

    # Extract and clean generated codee
    generated_code = response.replace("```python", "").replace("```", "").strip()

    # Save the new module
    file_path = "generated_workout_module.py"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(generated_code)

    print(f"New workout module saved: {file_path}")

except FileNotFoundError:
    print(f"Error: Image file '{image_path}' not found.")