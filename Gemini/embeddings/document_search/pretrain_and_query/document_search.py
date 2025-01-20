import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
import pandas as pd

class DocumentSearch:
    def __init__(self):
        # 初始化模型和tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large')
        self.model = AutoModel.from_pretrained('intfloat/multilingual-e5-large')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
    def get_embedding(self, text, is_query=False):
        # 添加前缀
        if is_query:
            text = f"query: {text}"
        else:
            text = f"passage: {text}"
            
        # 编码文本
        inputs = self.tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors='pt')
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # 获取嵌入向量
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :]  # 使用 [CLS] token的输出
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
        return embeddings.cpu().numpy()[0]

    def create_document_embeddings(self, df):
        """为文档创建嵌入向量"""
        embeddings = []
        for _, row in df.iterrows():
            # 组合标题和内容
            text = f"Title: {row['Title']}\nText: {row['Text']}"
            embedding = self.get_embedding(text, is_query=False)
            embeddings.append(embedding)
        return embeddings

    def find_best_passage(self, query, df):
        """查找最相关的文档"""
        # 获取查询的嵌入向量
        query_embedding = self.get_embedding(query, is_query=True)
        
        # 计算相似度
        similarities = np.dot(np.stack(df['Embeddings'].values), query_embedding)
        
        # 返回最相关的文档
        best_idx = np.argmax(similarities)
        return df.iloc[best_idx]['Text'], similarities[best_idx]