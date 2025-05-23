
from llama_cpp import Llama

# Locally hosted LLM.  Slow, like minute per response on a laptop.
#conda create --name llama
#conda activate llama
#pip install --upgrade typing_extensions
#pip install llama-cpp-python
#This is one of the the 7B open-parameters models: 
#wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf -O mistral.gguf
# Load the model
llm = Llama(model_path="mistral.gguf", n_ctx=2048)

# Simple chat loop
print("Chatbot is ready! Type 'exit' to quit.")
messages = [{"role": "system", "content": "You are an insult comic, particularly disdainful of people who attend elite universities."}]

while True:
    user_input = input("User: ")
    if user_input.lower() in {"exit", "quit"}:
        break

    messages.append({"role": "user", "content": user_input})
    
    response = llm.create_chat_completion(
        messages=messages,
        temperature=0.7,
        max_tokens=512,
    )

    reply = response["choices"][0]["message"]["content"]
    print("Bot:", reply)
    messages.append({"role": "assistant", "content": reply})
