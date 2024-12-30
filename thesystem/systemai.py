import os
import ast
import sys
import json
import google.generativeai as genai
import re
from concurrent.futures import ThreadPoolExecutor

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.insert(0, project_root)

# List of files to read but not edit
FILES_TO_READ_ONLY = [
    "thesystem/system.py",
    "thesystem/systemai.py",
    "thesystem/dungeon.py",
    "thesystem/dailyquest.py"
]


# Function to load directories from JSON
def load_directories(json_path):
    """Load the directories from the JSON file."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    # Extract all directory paths from the JSON
    directories = []
    for category in data.values():
        directories.extend(category.values())
    return directories

# Function to analyze code structure
def analyze_code(file_path):
    """Analyze the structure of the Python code in a file."""
    with open(file_path, 'r') as f:
        code = f.read()
    parsed_code = ast.parse(code)
    functions = [node.name for node in ast.walk(parsed_code) if isinstance(node, ast.FunctionDef)]
    classes = [node.name for node in ast.walk(parsed_code) if isinstance(node, ast.ClassDef)]
    return {"functions": functions, "classes": classes, "code": code}

# Function to interact with Gemini AI
def interact_with_ai(existing_code, prompt):
    """Send the prompt to Gemini AI and get the response, generating entire new code."""
    # Configure the Gemini API with your API key
    genai.configure(api_key="AIzaSyCSoGWi5wdBs3nXUBrNDMp5gkvyTNTCmqA")

    # Create a GenerativeModel instance
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Generate content based on the prompt alone (no existing code included)
    response = model.generate_content(f"{prompt}")
    
    # Clean the response to remove unwanted parts like comments and markdown artifacts
    cleaned_response = clean_ai_response(response.text)
    
    return cleaned_response


# Function to clean AI-generated response by removing unwanted comments and markdown artifacts
def clean_ai_response(ai_response):
    """Clean up the AI-generated response to remove comments and markdown artifacts."""
    # Remove code block markers like ```python or ```
    ai_response = re.sub(r'```python|```', '', ai_response)
    
    # Remove any leading comments (assuming comments start with #)
    ai_response = re.sub(r'^\s*#.*\n', '', ai_response)  # Removes single-line comments at the top

    # Optionally, remove any other unwanted patterns, like specific comment headers.
    return ai_response.strip()

# Function to decide if the file should be changed based on AI's analysis
def should_change_file(player_level, required_level, ai_decision_prompt):
    """Decide if the file should be changed based on player level and AI's decision."""
    if player_level >= required_level:
        # Ask AI whether the current file is the most relevant to change
        decision_prompt = f"Based on the player's level of {player_level}, should the game code be updated? {ai_decision_prompt}"
        ai_response = interact_with_ai("", decision_prompt)  # Pass empty code for just the decision prompt
        
        # Use AI's response to decide whether to proceed
        if "yes" in ai_response.lower():
            return True
        else:
            return False
    else:
        print("Player level is not high enough to change the file.")
        return False

# Function to integrate new code
def integrate_code(existing_file, new_code):
    """Backup the original file and write the new code to it."""
    backup_file = existing_file + ".backup"
    os.rename(existing_file, backup_file)  # Backup original file
    with open(existing_file, 'w') as f:
        f.write(new_code)

# Function to process a single file
def process_file(file_path, player_level, required_level, prompt):
    """Process a single file, analyzing it, deciding if it should be updated, and integrating the new code if necessary."""
    file_name = os.path.basename(file_path)
    
    # Check if the file is in the read-only list by using the full path
    if file_path in FILES_TO_READ_ONLY:
        print(f"Reading {file_path}, but not editing it...")
    elif file_name == "gui.py" or should_process_other_file(file_name):
        print(f"Processing {file_path}...")

        # Step 1: Analyze existing code
        code_info = analyze_code(file_path)

        # Step 2: Get AI decision about whether to change the file
        ai_decision_prompt = f"Based on the current game state, should the {file_name} file be updated or should another file be changed?"
        if should_change_file(player_level, required_level, ai_decision_prompt):
            # Step 3: Get AI-generated code
            new_code = interact_with_ai(code_info["code"], prompt)

            # Step 4: Integrate new code into the project
            integrate_code(file_path, new_code)

            print(f"New code integrated into {file_path}. Backup saved as {file_path}.backup")
        else:
            print(f"No changes made to {file_path} based on AI decision.")
    else:
        print(f"Skipping {file_path}, not a valid file to process.")


# Function to decide whether a non-gui.py file should be processed
def should_process_other_file(file_name):
    """Decide whether a non-gui.py file should be processed based on its name."""
    # Add custom conditions here for files you want to process
    # Example: Check if the file name matches a specific pattern or ends with a specific suffix
    if file_name.endswith(".py"):
        return True
    return False

# Main process
def main():
    json_file = "thesystem/Directories.json"  # Path to your JSON file
    prompt = "Analyze the following Tkinter code and regenerate it (use it as a template, keep the rest the same) with a new feature of your choice, it needs to be relevant to the code. DONT MAKE ANY COMMENTS, PURE CODE."

    # Load directories from JSON
    directories = load_directories(json_file)
    print(directories)
    
    with open("Files/status.json", 'r') as fson:
        data = json.load(fson)
        lvl = data["status"][0]['level']
        player_level = lvl
        required_level = 1  # Example required level for change
        
        # Step 1: Prepare a list of all Python file paths to process
        file_paths = []
        for directory in directories:
            directorypath = os.path.join(project_root, directory)
            for root, dirs, files in os.walk(directorypath):
                for file in files:
                    if file.endswith(".py"):  # Collecting all Python files
                        file_paths.append(os.path.join(root, file))
        
        # Step 2: Use ThreadPoolExecutor to process all files concurrently
        with ThreadPoolExecutor() as executor:
            executor.map(lambda file_path: process_file(file_path, player_level, required_level, prompt), file_paths)

if __name__ == "__main__":
    main()
