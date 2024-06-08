# %%
from openai import OpenAI
import emoji
import re
import pandas as pd
import json
from dotenv import load_dotenv
import os

load_dotenv(override=True)
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY_DEADLINE_DETECTION")

# %%
client=OpenAI(api_key=OPENAI_API_KEY)

# %%
df=pd.read_excel("./data/formatted_notice.xlsx", engine="openpyxl")
# %% step1: delete tags except <strong>
def tag_processing(body: str) -> str:
    return re.sub(r'<(?!\/?strong\s*\/?)[^>]+>', '', body)

# %% step2: demojize
def demojize(body: str) -> str:
    return emoji.demojize(body)

# %% step3: revert demojized emoji
def revert_demojize(body: str) -> str:
    return emoji.emojize(body)

# %% TODO: Hugging Face Data Preparation - extract deadline information with GPT API
def extract_deadline(body: str, createdAt: str) -> str:
    try:
        response=client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "## 당신의 목적\n당신은 공지글로부터 신청 마감 기한, 행사 시작 시간과 같은 deadline 정보를 알아내는 AI 봇입니다.\n\n## 입력 정보\n**공지의 생성 일자**와 **공지 본문**이 제공됩니다.\n\n## 출력 값\n만약, deadline을 알아내기에 정보가 충분하지 않다면 빈 문자열을 반환하고, 정보가 있다면 '%Y-%m-%d %H:%M:%S'의 datetime.datetime 형식의 string으로 deadline을 알려주세요.\n\n## 출력 형식\n다음과 같은 json 형태로 출력하세요 {'deadline': ''}"},
                {"role": "user", "content": f'## 공지의 생성 일자\n{createdAt}\n\n## 공지 본문\n{body} 이제 json 형식으로 deadline 정보를 추출해주세요.'}
            ]
        )
    except Exception as e: #If the context window is exceeded, use GPT-4
        response=client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "## 당신의 목적\n당신은 공지글로부터 신청 마감 기한, 행사 시작 시간과 같은 deadline 정보를 알아내는 AI 봇입니다.\n\n## 입력 정보\n**공지의 생성 일자**와 **공지 본문**이 제공됩니다.\n\n## 출력 값\n만약, deadline을 알아내기에 정보가 충분하지 않다면 빈 문자열을 반환하고, 정보가 있다면 '%Y-%m-%d %H:%M:%S'의 datetime.datetime 형식의 string으로 deadline을 알려주세요.\n\n## 출력 형식\n다음과 같은 json 형태로 출력하세요 {'deadline': ''}"},
                {"role": "user", "content": f'## 공지의 생성 일자\n{createdAt}\n\n## 공지 본문\n{body} 이제 json 형식으로 deadline 정보를 추출해주세요.'}
            ]
        )
        
    return json.loads(response.choices[0].message.content)["deadline"]

# %%
if __name__=="__main__":
    df["body"]=df["body"].apply(tag_processing)
    df["body"]=df["body"].apply(demojize)
    df.to_excel("./data/formatted_notice.xlsx", index=False)
# %%
