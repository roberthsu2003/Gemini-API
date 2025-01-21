import pandas as pd
from document_search import DocumentSearch
from pathlib import Path

def train_and_save_embeddings():
    # Initialize document search
    doc_search = DocumentSearch() 

    df = pd.read_csv('001.csv')
    df['說明'] = '地址:' + df['地址']+',' + \
    '經度:' + df['經度'].astype(str)+',' + \
    '緯度:' + df['緯度'].astype(str)+',' + \
    '充電樁數量' + df['充電樁數量']

    result_df = df[['充電樁位置','說明']]
    result_df.columns = ['Title','Text']
    
    
    # 创建DataFrame
    df = result_df.copy()       

    # Generate embeddings
    df['Embeddings'] = doc_search.create_document_embeddings(df)
    
    # Save DataFrame
    df.to_pickle("embeddings.pkl")
    print("Embeddings saved successfully")

if __name__ == "__main__":
    train_and_save_embeddings()