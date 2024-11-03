import os
import json
import sys

# Mapping of skills to corresponding item types
skill_to_item = {
    "strength": "sword",
    "defense": "armor",
    "mining": "tool",
    "farming": ["axe", "hoe"]  # farming has multiple items
}

abbreviation = {
    "strength": "str",
    "defense": "def",
    "mining": "min",
    "farming": "far"
}

# Function to generate the config content
def generate_material_file(skill, material, level, item_type):
    return {
        "replace": True,
        "skill": skill,
        "level": level,
        "item": f"minecraft:{item_type}",
        "material": material
    }
def generate_item_file(skill, item, level):
    return {
        "replace": True,
        "skill": skill,
        "level": level,
        "item": item
    }
def generate_custom_file(skill, item, level):
    return {
        "replace": True,
        "skill": skill,
        "level": level,
        "item": "minecraft:custom_item",
        "object": item
    }

# Load the input JSON file
with open('./input/main.json', 'r') as f:
    try:
        input_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

# Create the output folders
output_folder = os.path.join("output", "item")
os.makedirs(output_folder, exist_ok=True)

# Iterate through each skill and material, creating JSON files
for skill, materials in input_data.items():
    for type, level in materials.items():
        filename: str
        config_data: dict
        
        if ":" in type:
            if "minecraft:" in type:
                filename = f"{abbreviation[skill]}.item-{type.split(':')[1]}.json"
                config_data = generate_item_file(skill, type, level)
            else:
                filename = f"{abbreviation[skill]}.custom-{type.split(":")[1]}.json"
                config_data = generate_custom_file(skill, type, level)
            
            # Write to the JSON file
            with open(os.path.join(output_folder, filename), 'w') as f:
                json.dump(config_data, f, indent=4)
        
        elif isinstance(skill_to_item[skill], list):
            for item_type in skill_to_item[skill]:
                filename = f"{abbreviation[skill]}.{item_type}-{type}.json"
                config_data = generate_material_file(skill, type, level, item_type)
                
                # Write to the JSON file
                with open(os.path.join(output_folder, filename), 'w') as f:
                    json.dump(config_data, f, indent=4)
        
        else:
            # Single item type
            item_type = skill_to_item[skill]
            filename = f"{abbreviation[skill]}.{item_type}-{type}.json"
            config_data = generate_material_file(skill, type, level, item_type)
            
            # Write to the JSON file
            with open(os.path.join(output_folder, filename), 'w') as f:
                json.dump(config_data, f, indent=4)

print(f"Config files generated in '{output_folder}' folder.")
