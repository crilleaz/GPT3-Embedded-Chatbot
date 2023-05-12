import os
import glob

# Set the path to the folder containing the .txt files
folder_path = "PATH_TO_FOLDER"

# Find all .txt files in the folder
txt_files = glob.glob(os.path.join(folder_path, "*.txt"))

# Loop through each .txt file
for txt_file in txt_files:
    # Open the file and read its contents
    with open(txt_file, "r") as f:
        contents = f.readlines()

    # Split the contents into chunks of 10 lines
    chunks = [contents[i:i+10] for i in range(0, len(contents), 10)]

    # Loop through each chunk and save it as a separate file
    for i, chunk in enumerate(chunks):
        # Get the original file name and add an increment number at the end
        new_file_name = os.path.splitext(txt_file)[0] + f"_{i+1}.txt"

        # Save the chunk as a new file with the incremented file name
        with open(new_file_name, "w") as f:
            f.writelines(chunk)
