Train and use the embedded data combined with GPT3 to chat directly with said data.<br>
Embeddings via text-embedding-ada-002<br>
Processing via gpt-3.5-turbo<br>


### Installation

1. Clone the repository
```
git clone https://github.com/crilleaz/GPT3-Embedded-Chatbot
```

2. Install the dependencies
```
pip install -r requirements.txt
```

3. In train.py and run.py change 
```
api_key = "OPENAI_KEY"
```

4. Add your own .txt-files in folder /train to generate embeddings
```
python train.py
```

5. Run the bot
```
python run.py
```

### How to add data to train

Place your .txt-files into /train folder, i've seen better results with OpenAI API's by splitting the files into smaller chunks. Change and use split.py if you run into limits.


### Discord
Crilleaz
