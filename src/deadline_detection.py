# %%
from openai import OpenAI
client = OpenAI()

import json
import requests
import time
# %%
def extract_deadline(body: str, createdAt: str) -> str:
    url="https://api.openai.com/v1/chat/completions"
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.api_key}"
    }
    data={
        "model": "gpt-3.5-turbo-0125",
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "## 당신의 목적\n당신은 공지글로부터 신청 마감 기한, 행사 시작 시간과 같은 deadline 정보를 알아내는 AI 봇입니다.\n\n## 입력 정보\n**공지의 생성 일자**와 **공지 본문**이 제공됩니다.\n\n## 출력 값\n만약, deadline을 알아내기에 정보가 충분하지 않다면 빈 문자열을 반환하고, 정보가 있다면 '%Y-%m-%d %H:%M:%S'의 datetime.datetime 형식의 string으로 deadline을 알려주세요.\n\n## 출력 형식\n다음과 같은 json 형태로 출력하세요 {'deadline': ''}"},
            {"role": "user", "content": f"## 공지의 생성 일자\n{createdAt}\n\n## 공지 본문\n{body}. 이제 json 형식으로 deadline 정보를 추출해주세요."}
        ]

    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=5)
    except requests.Timeout:
        raise TimeoutError("The response time is longer than 5 seconds.")
    except requests.RequestException as e:
        data["model"]="gpt-4o"
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=5)

    return json.loads(response.json()["choices"][0]["message"]["content"])["deadline"]
    
# %%
if __name__ == "__main__":
    createdAt = "2022-01-01 00:00:00"
    body = "안녕하세요, 하우스연합회입니다. 6월 7일 20시에 진행하였던 하우스연합회 '봄학기 격려행사'에 많은 관심을 가져주셔서 감사합니다. 많은 학생들이 참여하는 행사인만큼 다음 행사 때는 부족한 점을 보완하고자 행사 만족도조사를 진행합니다. 여러분의 설문조사가 행사에 반영될 수 있으니 소중한 의견 부탁드립니다. 만족도조사 바로가기 : https://forms.gle/z3fp2GzGWp8F6HNK9 ( * 만족도 조사 기간 : ~ 2024년 6월 13일 목요일)"