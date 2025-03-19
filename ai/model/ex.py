from threading import Thread
from transformers import LlamaTokenizer
from optimum.rbln import BatchTextIteratorStreamer, RBLNLlamaForCausalLM

# 컴파일된 모델 로드
compiled_model = RBLNLlamaForCausalLM.from_pretrained(
    model_id="rbln-Llama-2-7b-chat-hf",
    export=False,
)

# input 준비
tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", padding_side="left")
tokenizer.pad_token = tokenizer.eos_token
conversation = [{"role": "user", "content": "Hey, are you conscious? Can you talk to me?"}]
text = tokenizer.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
inputs = tokenizer(text, return_tensors="pt", padding=True)

# 배치스트리밍을 위한 스트리머 준비
batch_size = 1
streamer = BatchTextIteratorStreamer(
    tokenizer=tokenizer,
    batch_size=batch_size,
    skip_special_tokens=True,
    skip_prompt=True,
)

# 문장 생성
generation_kwargs = dict(
    **inputs,
    streamer=streamer,
    do_sample=False,
    max_length=4096,
)
thread = Thread(target=compiled_model.generate, kwargs=generation_kwargs)
thread.start()

# 단어가 생성되어 토큰화되는 즉시 가져오기
for new_text in streamer:
    for i in range(batch_size):
        print(new_text[i], end="", flush=True)