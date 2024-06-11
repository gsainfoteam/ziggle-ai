from unsloth import FastLanguageModel
import torch
from dotenv import load_dotenv
import os

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "inthree3/ziggle-ai-deadline-detection",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    token = HUGGINGFACE_API_KEY, # use one if using gated models like meta-llama/Llama-2-7b-hf
)

alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

def detect_deadline(createdAt: str, notice: str) -> str:
    FastLanguageModel.for_inference(model) # Enable native 2x faster inference
    inputs = tokenizer(
    [
        alpaca_prompt.format(
            "## 당신의 목적\n당신은 공지글로부터 신청 마감 기한, 행사 시작 시간과 같은 deadline 정보를 알아내는 AI 봇입니다.\n\n## 입력 정보\n**공지의 생성 일자**와 **공지 본문**이 제공됩니다.\n\n## 출력 값\n만약, deadline을 알아내기에 정보가 충분하지 않다면 빈 문자열을 반환하고, 정보가 있다면 '%Y-%m-%d %H:%M:%S'의 datetime.datetime 형식의 string으로 deadline을 알려주세요.\n\n## 출력 형식\n다음과 같은 json 형태로 출력하세요 {'deadline': ''}", # instruction
            f"## 공지의 생성 일자\n{createdAt}\n\n## 공지 본문\n{notice}\n\n이제 json 형식으로 마감 기한 정보를 추출해주세요.", # input
            "", # output - leave this blank for generation!
        )
    ], return_tensors = "pt").to("cuda")

    outputs = model.generate(**inputs, max_new_tokens = 64, use_cache = True)
    return tokenizer.batch_decode(outputs)