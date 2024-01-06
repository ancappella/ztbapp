# import os
# from docx import Document
from transformers import BertTokenizer, BertModel
# from transformers import AutoTokenizer, AutoModel, AutoConfig
import torch
from scipy.spatial.distance import cosine
# import numpy as np
# import sys
# print(sys.executable)
# from summarizer import Summarizer
# import textwrap



# 这里手动下载模型与分词器，根据目录加载使用
vocab_file = 'shibing624/vocab.txt'
tokenizer = BertTokenizer(vocab_file)
model = BertModel.from_pretrained("shibing624/text2vec-base-chinese-sentence/")
# 加载配置
#config = AutoConfig.from_pretrained('shibing624/text2vec-base-chinese-sentence/')

# 修改配置
#config.output_hidden_states = True
#summary_model = BertModel.from_pretrained('shibing624/text2vec-base-chinese-sentence/', config=config)
# 初始化抽取式摘要模型
#summarizer = Summarizer(custom_model=summary_model, custom_tokenizer=tokenizer)
# Mean Pooling - Take attention mask into account for correct averaging


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# # 提问
# question = '离婚了彩礼怎么办'
# encoded_input = tokenizer([question], padding=True, truncation=True, return_tensors='pt')
# with torch.no_grad():
#     model_output = model(**encoded_input)
# question_embedding = mean_pooling(model_output, encoded_input['attention_mask']).numpy().squeeze()

# # 读取Word文档
# file_path = 'D:\\律所资料\\律师助手要的资料库\\离婚案例.docx'
# focus_embeddings = []
# doc = Document(file_path)
# for para in doc.paragraphs:
#     if '案情焦点：' in para.text:
#         focus = para.text.split('案情焦点：')[1].split('\n')[0]
#         encoded_input = tokenizer([focus], padding=True, truncation=True, max_length=512, return_tensors='pt')
#         with torch.no_grad():
#             model_output = model(**encoded_input)
#         focus_embedding = mean_pooling(model_output, encoded_input['attention_mask']).numpy().squeeze()
#         focus_embeddings.append((file_path, focus, focus_embedding))

# similarities = [(file, focus, 1 - cosine(question_embedding, focus_embedding)) for file, focus, focus_embedding in focus_embeddings]
# top_three = sorted(similarities, key=lambda x: x[2], reverse=True)[:3]

# print('最相似的三个案情焦点来自以下文档：')
# for file, focus_text, similarity in top_three:
#     print(f'案情焦点：{focus_text}，相似度：{similarity}')


def get_project(project_info, projects):
    # 提问
    question = project_info
    encoded_input = tokenizer([question], padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    question_embedding = mean_pooling(model_output, encoded_input['attention_mask']).numpy().squeeze()

    # 读取Word文档
    # file_path = 'D:\\律所资料\\律师助手要的资料库\\离婚案例.docx'
    focus_embeddings = []
    # doc = Document(file_path)
    for para in projects:
        # if '案情焦点：' in para.text:
        # focus = para.text.split('案情焦点：')[1].split('\n')[0]
        # focus = f"{para.案件概要}"

        # 将每一行的 project_name,project_detail,budget,start_time, buyer_info 进行拼接(str_bid_info)
        focus = f"{para.project_name} {para.project_detail} {para.budget} {para.start_time} {para.buyer_info}"
        encoded_input = tokenizer([focus], padding=True, truncation=True, max_length=512, return_tensors='pt')
        with torch.no_grad():
            model_output = model(**encoded_input)
        focus_embedding = mean_pooling(model_output, encoded_input['attention_mask']).numpy().squeeze()
        focus_embeddings.append((para, focus, focus_embedding))

    similarities = [(file, focus, 1 - cosine(question_embedding, focus_embedding)) for file, focus, focus_embedding in focus_embeddings]
    top_three = sorted(similarities, key=lambda x: x[2], reverse=True)[:5]

    projects = []
    print('最相似的三个案情焦点来自以下文档：')
    for para, focus_text, similarity in top_three:
        print(f'id：{para.id}，相似度：{similarity}')
        projects.append(para)

    return projects
