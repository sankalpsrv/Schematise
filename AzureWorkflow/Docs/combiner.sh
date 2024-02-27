#!/bin/bash

# Name of the file to store the combined content
combined_file="combined_files.txt"

# Check if the combined file already exists; if so, remove it to start fresh
if [[ -f "$combined_file" ]]; then
    rm "$combined_file"
fi

# Loop through all files in the current directory
for file in *; do
    # Check if the current item is a file
    if [[ -f "$file" ]]; then
        # Read the content of the file, delete newline and tab characters, and escape double quotes
        content=$(cat "$file" | tr -d '\n\t' | sed 's/"/\\"/g')
        # Append the formatted string to the combined file
        echo "{\"$file\": \"$content\"}," >> "$combined_file"
    fi
done

# Optionally, you can remove the last comma to make it a valid JSON array if that's the intention
# This requires sed or a similar tool to be available
sed '$ s/,$//' "$combined_file" > temp_file && mv temp_file "$combined_file"

echo "Files have been combined into $combined_file."
