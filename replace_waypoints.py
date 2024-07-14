import json
import sys

if len(sys.argv) == 2:
    file_path = sys.argv[1]
else:
    print("Usage: python replace_waypoints.py <file_path>")
    sys.exit()


def replace_blocks(data, found_blocks):
    """
    Recursively search for blocks of a specific type in a nested JSON structure.

    :param data: The current level of the JSON structure being searched.
    :param found_blocks: A list to accumulate the found blocks.
    """
    if isinstance(data, dict):
        # If the current level is a dictionary and matches the block type, add it to the list
        if (
            data.get("type") == "subroutineInstanceBlock"
            and data["extraState"].get("subroutineName") == "pl_addWaypoint"
        ):
            if len(found_blocks) == 0:
                found_blocks.append(data)
            new_wp_block_parameters = {
                "parameters": [
                    {"types": "Number", "name": "x"},
                    {"types": "Number", "name": "y"},
                    {"types": "Number", "name": "z"},
                ]
            }
            new_wp_block_inputs = {
                "PARAM-0": {
                    "block": {
                        "type": "Number",
                        "id": data["inputs"]["PARAM-0"]["block"]["inputs"]["VALUE-0"][
                            "block"
                        ]["id"],
                        "fields": {
                            "NUM": data["inputs"]["PARAM-0"]["block"]["inputs"][
                                "VALUE-0"
                            ]["block"]["fields"]["NUM"]
                        },
                    }
                },
                "PARAM-1": {
                    "block": {
                        "type": "Number",
                        "id": data["inputs"]["PARAM-0"]["block"]["inputs"]["VALUE-1"][
                            "block"
                        ]["id"],
                        "fields": {
                            "NUM": data["inputs"]["PARAM-0"]["block"]["inputs"][
                                "VALUE-1"
                            ]["block"]["fields"]["NUM"]
                        },
                    }
                },
                "PARAM-2": {
                    "block": {
                        "type": "Number",
                        "id": data["inputs"]["PARAM-0"]["block"]["inputs"]["VALUE-2"][
                            "block"
                        ]["id"],
                        "fields": {
                            "NUM": data["inputs"]["PARAM-0"]["block"]["inputs"][
                                "VALUE-2"
                            ]["block"]["fields"]["NUM"]
                        },
                    }
                },
            }
            data["extraState"]["subroutineName"] = "pl_addWP"
            data["extraState"]["parameters"] = new_wp_block_parameters
            data["fields"]["SUBROUTINE_NAME"] = "pl_addWP"
            data["inputs"] = new_wp_block_inputs
        # Recursively search in each value of the dictionary
        for value in data.values():
            replace_blocks(value, found_blocks)
    elif isinstance(data, list):
        # If the current level is a list, recursively search in each item
        for item in data:
            replace_blocks(item, found_blocks)


# List to hold the found blocks
found_blocks = []

new_wp_block_parameters = {
    "parameters": [
        {"types": "Number", "name": "x"},
        {"types": "Number", "name": "y"},
        {"types": "Number", "name": "z"},
    ]
}
new_wp_block_inputs = {
    "PARAM-0": {"block": {"type": "Number", "id": "param0Id", "fields": {"NUM": 999}}},
    "PARAM-1": {"block": {"type": "Number", "id": "param1Id", "fields": {"NUM": 999}}},
    "PARAM-2": {"block": {"type": "Number", "id": "param2Id", "fields": {"NUM": 999}}},
}

# Open and read the JSON data from the file
with open(file_path, "r") as file:
    json_data = json.load(file)

# Replace 'pl_addWaypoint' with the specific block type you're searching for
replace_blocks(json_data, found_blocks)

# Specify the file name
output_file = "output.json"

# Writing JSON data to a file
with open(output_file, "w") as file:
    json.dump(json_data, file, indent=2)
