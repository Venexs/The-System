import ujson

def decrement_stats():
    ujson_file="Files/Player Data/Status.json"
    # Load the ujson file
    with open(ujson_file, 'r') as file:
        data = ujson.load(file)

    # Extract the "status" part of the ujson data
    status = data["status"][0]

    # List of attributes to decrement
    attributes_to_decrement = ["level", "str", "int", "agi", "vit", "per", "man"]

    # Decrement each attribute, ensuring no value goes below 0
    for attr in attributes_to_decrement:
        if status[attr] > 0:
            status[attr] -= 1
        else:
            print(f"{attr} is already at 0, not decrementing.")

    # Save the updated ujson data back to the file
    with open(ujson_file, 'w') as file:
        ujson.dump(data, file, indent=4)





