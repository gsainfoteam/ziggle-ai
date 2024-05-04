# %%
import emot.core
import torch
import torch.backends
import torch.backends.cudnn
import torchtext
from torchtext.functional import to_tensor
import numpy as np
import torch.nn as nn
import torch.nn.functional as F 
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from konlpy.tag import Kkma
import re
import emot

import torchtext.data
import torchtext.datasets
import torchtext.models

SEED=777
torch.manual_seed(SEED)
torch.backends.cudnn.deterministic=True
# %% df 생성
content_df=pd.read_excel("./data/Content.xlsx", engine="openpyxl")
# notice2tag_df=pd.read_excel("./data/_NoticeToTag.xlsx", engine="openpyxl")
notice_df=pd.read_excel("./data/Notice.xlsx", engine="openpyxl")
# tag_df=pd.read_excel("./data/Tag.xlsx", engine="openpyxl")

ko_content_df=content_df.loc[content_df["lang"]=="ko"].copy(deep=True)
df=pd.merge(ko_content_df, notice_df, left_on="notice_id", right_on="id", how="inner")
df=df[["title", "body", "views"]]
df

# %% step1: tag 제거
def tag_processing(df) -> list[str]:
    if type(df)==pd.core.frame.DataFrame:
        body_list=df.body.to_list()
    custom_replacement=torchtext.data.custom_replace([(r'<(?!\/?strong\s*\/?)[^>]+>', '')])
    body_list=list(custom_replacement(body_list))

    columns=df.columns.tolist()
    df_matrix=[0 for i in range(len(columns))]

    for i in range(len(columns)):
        col=columns[i]
        if col=="body":
            df_matrix[i]=body_list
            continue
        
        df_matrix[i]=df[col].to_list()
    return df_matrix
# %% check whether tag_processing works well
df_matrix=tag_processing(df)
df_matrix[1][:5]

# %% step2: emot_processing
# bulk_text=["😘 당신은 사랑받기 ♥️ 위해 태어난 사람", "행복한 하루 되세요 🍀"]
bulk_text=["동해물과🚢 백두산이⛰️ 마르고 닳도록~", "하느님이✝️ 보우하사 우리나라 만세"]
for text in bulk_text:
    print(text.split())
emot_obj=emot.core.emot()

def emot_processing(df_matrix):
    for i in range(len(df_matrix[1])):
        text=df_matrix[1][i]
        emoji=emot_obj.emoji(text)
        text=list(df_matrix[1][i])
        for j in range(len(emoji["value"])):
            try:
                text[emoji["location"][j][0]]=emoji["mean"][j]
            except IndexError:
                print("IndexError Ocurred")
                print(emoji)
                print(text)
                print(emoji["location"][j][0])
        text="".join(text)
        df_matrix[1][i]=text
    return df_matrix

df_matrix=emot_processing(df_matrix)
# %% convert df_matrix to transform it into DataFrame
def list2df(df_matrix):
    df_form_matrix=[]
    for i in range(len(df_matrix[0])):
        row=[]
        for j in range(3):
            row.append(df_matrix[j][i])
        df_form_matrix.append(row)

    df_processed=pd.DataFrame(df_form_matrix, columns=["title", "body", "views"])
    df_processed.to_excel('./data/data_processed.xlsx')
# %% 
# -------------------start from processed data-------------------
df=pd.read_excel('./data/data_processed.xlsx')
body_list=df.body.to_list()

# %% xmlr 인코딩
xlmr_base=torchtext.models.XLMR_BASE_ENCODER
model=xlmr_base.get_model()
transform=xlmr_base.transform()
# ----------------------------------------------------------
input_batch=[body_list[0]]
model_input=to_tensor(transform(input_batch), padding_value=1)
print(model_input.shape)
output=model(model_input)
print(output.shape)

# %% custom Dataset
class TextDataset(Dataset):
    def __init__(self, text, labels):
        self.data=text
        self.labels=labels

    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        label=self.labels[idx]
        text=self.data[idx]
        item={'text':text, 'views':label}
        return item
    
ViewDataset=TextDataset(body_list, df.views.to_list())
TextDataLoader=DataLoader(ViewDataset, batch_size=3, shuffle=True)

# %%

# %% RNN cell
class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleRNN, self).__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out, hidden = self.rnn(x)
        out = self.fc(out[:, -1, :])  # 마지막 시간 단계의 출력만 사용
        return out

# 모델, 손실 함수, 옵티마이저 생성
input_size = 100  # 입력 차원
hidden_size = 64  # RNN의 은닉 상태 크기
output_size = 768  # 출력 크기는 단어 집합의 크기와 동일
model = SimpleRNN(input_size, hidden_size, output_size)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 훈련
for epoch in range(10):
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# %%
from torch.utils.data import DataLoader
train_dataloader=DataLoader(body_list)
label_dataloader=DataLoader(df.views.to_list())

print(type(train_dataloader))
# %% TODO:poetry 적용