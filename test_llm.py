from llama_cpp import Llama

# Load the model
llm = Llama(model_path="/home/vmuser/Downloads/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf")

# Query the model
prompt = "Translate the following Korean sentence into fluent English:\n묘도콤-#하헤7"
response = llm(prompt, max_tokens=100)

# Print the result
print("🧠 Response:", response['choices'][0]['text'].strip())
