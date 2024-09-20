from transformers import AutoModelForCausalLM, AutoTokenizer

# Load pre-trained DialoGPT model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def get_chatbot_response(user_input):
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    response_ids = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return response
