import json

def generate_xp_dict(max_level=120):
    xp_check = {}
    
    # Stage 1: Levels 1-20 (Linear)
    # XP(n) = 20*n + 10
    # At level 20: XP = 20*20 + 10 = 410
    
    # Stage 2: Levels 21-100 (Cubic with coefficient chosen to meet desired level 97)
    cubic_coef_stage2 = 0.3444
    
    # Precompute XP at level 20 for stage 2:
    xp_level20 = 410
    
    # We'll compute XP(n) = 410 + 0.3444 * (n - 20)^3 for 21 <= n <= 100.
    # This gives XP(97) ~ 157632 as desired.
    
    # Stage 3: Levels 101+ (Eased cubic progression)
    # Let xp_level100 be the XP at level 100 using the stage 2 formula.
    xp_level100 = xp_level20 + cubic_coef_stage2 * ((100 - 20) ** 3)
    # For levels above 100, we use a lower coefficient:
    cubic_coef_stage3 = 0.3

    for level in range(1, max_level + 1):
        if level <= 20:
            xp = 20 * level + 10
        elif level <= 100:
            xp = xp_level20 + cubic_coef_stage2 * ((level - 20) ** 3)
        else:
            xp = xp_level100 + cubic_coef_stage3 * ((level - 80) ** 3)
            
        xp_check[str(level)] = round(xp, 1)
    
    return {"XP Check": xp_check}

if __name__ == "__main__":
    # Adjust max_level as desired (here set to 120 for demonstration)
    xp_data = generate_xp_dict(250)
    
    # Save the dictionary to a JSON file
    with open("Files/Data/Level_Up_Values.json", "w") as f:
        json.dump(xp_data, f, indent=4)

    print(json.dumps(xp_data, indent=4))
