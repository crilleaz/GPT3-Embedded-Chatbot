import openai
import os
import csv
import glob
import json
import numpy as np
import time

text_array = []
api_key = "OPENAI_KEY"
openai.api_key = api_key
dir_path = os.path.join(os.getcwd(), 'train')
dir_full_path = os.path.join(dir_path, '*.txt')
embeddingFile = "processedData.csv"

# Loop through all .txt files in the /train folder
for file in glob.glob(dir_full_path):
    # Read the data from each file and push to the array
    # The dump method is used to convert spacings into newline characters \n
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        try:
            text = f.read().replace('\n', '')
        except UnicodeDecodeError:
            print(f"Error reading file: {file}. Skipping...")
        else:
            text_array.append(text)


# This array is used to store the embeddings
embedding_array = []

if api_key is None or api_key == "OPENAI_KEY":
    print("Invalid API key")
    exit()

# Loop through each element of the array
max_tokens_per_chunk = 8191
embedding_array = []

for text in text_array:
    text_chunks = []
    chunk_start = 0
    chunk_end = 0
    while chunk_end < len(text):
        chunk_end = min(len(text), chunk_start + max_tokens_per_chunk)
        text_chunk = text[chunk_start:chunk_end]
        text_chunks.append(text_chunk)
        chunk_start = chunk_end

    embeddings = []
    for text_chunk in text_chunks:
        try:
            response = openai.Embedding.create(
                input=text_chunk,
                model="text-embedding-ada-002"
            )
            embeddings.append(response)
            print(response)
        except Exception as e:
            print(f"Error processing chunk: {e}")
        time.sleep(5)

    embedding_list = []
    for response in embeddings:
        try:
            embedding_list.append(response['data'][0]['embedding'])
        except KeyError as e:
            print(f"Error extracting embedding: {e}")
    if len(embedding_list) > 0:
        embedding = np.concatenate(embedding_list)
        # Create a Python dictionary containing the vector and the original text
        embedding_dict = {'embedding': embedding.tolist(), 'text': text}

        # Store the dictionary in a list.
        embedding_array.append(embedding_dict)

with open(embeddingFile, 'w', newline='', encoding='utf-8') as f:
    # This sets the headers
    writer = csv.writer(f)
    writer.writerow(['embedding', 'text'])

    for obj in embedding_array:
        # Serialize the embedding vector as a JSON object
        embedding_json = json.dumps(obj['embedding'])
        writer.writerow([embedding_json, obj['text']])

print("Embeddings saved to:", embeddingFile)
