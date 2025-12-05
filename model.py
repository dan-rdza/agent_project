# server_llama.py
from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

llm = Llama(
    model_path="C:/Users/danie/.cache/lm-studio/models/mradermacher/Llama-3.2-8B-Instruct-GGUF",
    n_ctx=4096,
    n_threads=8,
)

class ChatRequest(BaseModel):
    model: str
    messages: list
    temperature: float = 0.2

@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest):
    # Convertimos messages -> prompt según el formato del modelo
    # Para un instruct simple podrías concatenar:
    user_content = ""
    for m in req.messages:
        if m["role"] == "user":
            user_content = m["content"]

    output = llm(
        user_content,
        temperature=req.temperature,
        max_tokens=512,
        stop=["</s>"],
    )

    text = output["choices"][0]["text"]

    return {
        "id": "chatcmpl-local-1",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
        ],
    }
