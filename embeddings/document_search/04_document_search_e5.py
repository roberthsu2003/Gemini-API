"""
04_document_search_e5.py
向量檢索延伸教學：開源 Multilingual-E5 繁體中文向量模型
展示本地端開源 Embedding 模型的離線向量檢索應用
"""

import os
from dotenv import load_dotenv
import numpy as np

print("📚 開源 Multilingual-E5 向量檢索範例")
print("支援本地離線執行繁體中文語意相似度與非對稱檢索任務。")
