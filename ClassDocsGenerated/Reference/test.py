import os
import re

# List of Unreal Engine default types to replace, add more as needed.
unreal_types = [
    "bool",
    "int",
    "int32",
    "uint8",
    "FName",
    "float",
    "double",
    "FString",
    "FVector",
    "FRotator",
    "FQuat",
    "FColor",
    "FTransform",
]

# Regex patterns
pattern_1 = re.compile(r"(\[[^\]]+\])(\([^\)]+\))")
pattern_2 = {re.compile(fr"\[\[{type_}\]\]"): type_ for type_ in unreal_types}

def process_file(file_path):
    """Process a single file to apply regex replacements."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Apply first regex replacement
    content = pattern_1.sub(r"[\1]", content)

    # Apply second regex replacement for Unreal types
    for regex, replacement in pattern_2.items():
        content = regex.sub(replacement, content)

    # Write changes back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

def process_directory(directory):
    """Process all .md files in a given directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                process_file(file_path)
            # break
        # break

if __name__ == "__main__":
    # Specify the directory containing .md files
    # target_directory = input("Enter the path to the directory containing .md files: ").strip()
    target_directory = 'Classes'

    if os.path.isdir(target_directory):
        process_directory(target_directory)
        print("Processing complete.")
    else:
        print(f"Invalid directory: {target_directory}")
