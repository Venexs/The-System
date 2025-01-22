import os
from PIL import Image

# Path to your folder
folder_path = "thesystem/alt_bottom_bar"

resize_factor = 0.7

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        img_path = os.path.join(folder_path, filename)
        
        # Open the image
        with Image.open(img_path) as img:
            # Calculate the new size
            new_width = int(img.width * resize_factor)
            new_height = img.height  # Keep the height unchanged
            
            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save the resized image (overwriting the original)
            resized_img.save(img_path)

print("All images have been resized and replaced.")