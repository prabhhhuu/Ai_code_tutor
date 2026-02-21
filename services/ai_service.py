from huggingface_hub import InferenceClient
from flask import current_app
import time

MODEL_MAP = {
    "qwen": "Qwen/Qwen2.5-Coder-3B-Instruct",
    "llama": "meta-llama/Llama-2-7b-chat-hf",
    "mistral": "mistralai/Mistral-7B-Instruct-v0.1",
    "falcon": "tiiuae/falcon-7b-instruct"
}

def ask_ai(prompt, model="qwen"):
    hf_token = current_app.config.get("HF_TOKEN")
    
    if not hf_token or hf_token == "":
        raise ValueError(
            "HF_TOKEN not configured. Please set HF_TOKEN in .env file. "
            "Get your token from https://huggingface.co/settings/tokens"
        )
    
    model_id = MODEL_MAP.get(model, MODEL_MAP["qwen"])
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            client = InferenceClient(token=hf_token, timeout=30)
            
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,
                temperature=0.3
            )
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's authentication error
            if "401" in error_msg or "Unauthorized" in error_msg:
                raise ValueError(
                    "Invalid HF token. Please check your token at "
                    "https://huggingface.co/settings/tokens. Make sure it has "
                    "'Read' access and is not revoked."
                )
            
            # Check if it's connection error
            if "getaddrinfo failed" in error_msg or "ConnectError" in error_msg or "Connection" in error_msg:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    raise ValueError(
                        "⚠️ Network Error: Cannot connect to Hugging Face servers. "
                        "Please check your internet connection and try again."
                    )
            
            # Fallback to Qwen if other model fails
            if model != "qwen":
                try:
                    client = InferenceClient(token=hf_token, timeout=30)
                    response = client.chat.completions.create(
                        model=MODEL_MAP["qwen"],
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=700,
                        temperature=0.3
                    )
                    return response.choices[0].message.content
                except Exception:
                    pass
            
            raise e
    
    raise ValueError("Failed to get response from AI models after multiple attempts.")
