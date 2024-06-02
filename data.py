# %%
# TODO: align the notice template
# export interface Notice {
#   id: number; #content_df - "content_id"
#   title: string; #content_df - "title"
#   deadline: dayjs.Dayjs | string | null; #content_df - "deadline"
#   currentDeadline: dayjs.Dayjs | string | null; #content_df - "deadline"
#   langs: string[]; #content_df - "lang" [ko] 또는 [ko, en]
#   content: string[]; #content_df - "body" 여러 개인 경우, lang=ko인 body로
#   author: {
#     name: string; # 어떻게 찾지 (백엔드에 문의 - 불가능하면 ""로 처리)
#     uuid: string; #notice_df - "author_id"
#   };
#   createdAt: dayjs.Dayjs | string; #notice_df - "created_at"
#   views: number; #notice_df - "views"
# }
import pandas as pd
content_df=pd.read_excel('./data/content.xlsx')
data_df=pd.read_excel('./data/data.xlsx', index_col=0)
notice_df=pd.read_excel('./data/notice.xlsx')
tag_df=pd.read_excel('./data/tag.xlsx')
notice_to_tag_df=pd.read_excel('./data/notice_to_tag.xlsx')
user_df=pd.read_excel('./data/user.xlsx')
formatted_notice_df=pd.read_excel('./data/formatted_notice.xlsx')
# %%
merged_df=pd.merge(content_df, notice_df, left_on="notice_id", right_on="id", suffixes=('_content', '_notice'))
# %%
langs_df=merged_df.groupby("notice_id")["lang"].apply(lambda x: list(set(x))).reset_index()
merged_df=pd.merge(merged_df[merged_df["lang"]=="ko"], langs_df, on="notice_id", suffixes=('_drop', ''))
# %%
# merged_df["lang"].apply(lambda x: len(x)).value_counts()
# %%
merged_df.drop(columns=["id_notice", "id_content", "created_at_content", "lang_drop", "updated_at", "deleted_at"], inplace=True)
merged_df.rename(columns={"notice_id": "id", "created_at_notice": "createdAt", "author_id": "author_uuid", "lang": "langs", "current_deadline": "currentDeadline"}, inplace=True)
# %%
user_df.drop(columns=["created_at", "consent"], inplace=True)
# %%
formatted_notice_df=pd.merge(formatted_notice_df, user_df, left_on="author_uuid", right_on="uuid")
# %%
formatted_notice_df.rename({"name": "author_name"}, axis=1, inplace=True)
# %%
#formatted_notice_df.to_excel('./data/formatted_notice.xlsx', index=False)
# %%
