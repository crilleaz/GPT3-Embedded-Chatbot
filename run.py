import json
import openai
import csv
import time

def calculate_similarity(vec1, vec2):
    dot_product = sum(vec1[i] * vec2[i] for i in range(len(vec1)))
    magnitude1 = sum(vec1[i] ** 2 for i in range(len(vec1))) ** 0.5
    magnitude2 = sum(vec2[i] ** 2 for i in range(len(vec2))) ** 0.5
    return dot_product / (magnitude1 * magnitude2)

def startAI():
    openai.api_key = "OPENAI_KEY"
    compiledData = "processedData.csv"
    company_name = "COMPANY_NAME HERE"
    start_chat = True

    while True:
        if start_chat:
            print(f"Welcome to the knowledge database for {company_name}. How can I assist you?")
            start_chat = False
            print("Write 'bye' to quit.")
        else:
            print("Anything else?")
        question = input("> ")
        if question == "bye" or not question:
            break
        response = openai.Embedding.create(model="text-embedding-ada-002", input=[question])
        try:
            question_embedding = response['data'][0]["embedding"]
        except:
            continue
        csv.field_size_limit(100000000) # yeah, it's a big number
        similarity_array = []
        with open(compiledData, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                text_embedding = json.loads(row['embedding'])
                similarity_array.append(calculate_similarity(question_embedding, text_embedding))
        index_of_max = similarity_array.index(max(similarity_array))
        original_text = ""
        with open(compiledData, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for rowno, row in enumerate(reader):
                if rowno == index_of_max:
                    original_text = row['text']
        system_prompt = f"""You can obtain information about swords from the list. You are an AI assistant working for {company_name}. Only answer the customer's question [Question] without adding additional information. Do not answer [Article] questions that have not been asked. Do not respond with a question."""
        question_prompt = f"[Article]\n{original_text}\n\n[Question]\n{question}"

        # Split messages into smaller chunks
        message_chunks = []
        while len(question_prompt) > 4096:
            last_period = question_prompt[:4096].rfind('.')
            message_chunks.append({"role": "user", "content": question_prompt[:last_period + 1]})
            question_prompt = question_prompt[last_period + 1:]
        message_chunks.append({"role": "user", "content": question_prompt})

        # Send each chunk to the API and concatenate the results
        response_chunks = []
        for i, message_chunk in enumerate(message_chunks):
            response_chunk = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_prompt}, message_chunk],
                temperature=0.5,
                max_tokens=2000,
            )
            response_chunks.append(response_chunk['choices'][0]['message']['content'])

            # Add delay if there are more than one chunks to avoid rate limit bullshit
            if i < len(message_chunks) - 1:
                print('Sendin data. Please wait')
                time.sleep(21)

        answer = ''.join(response_chunks)

        print("\n\033[32mSupport:\033[0m")
        print("\033[32m{}\033[0m".format(answer.lstrip()))
    print("Bye!")
startAI()
