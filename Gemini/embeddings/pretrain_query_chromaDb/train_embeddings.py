import pandas as pd
from document_search import DocumentSearch
import chromadb

def train_and_save_embeddings():
    # Initialize document search
    doc_search = DocumentSearch()

    # 初始化ChromaDb,建立永久儲存
    client = chromadb.PersistentClient()
    
    collection = client.get_or_create_collection(
        name="charging_station",
        metadata={"description": "充電站位置資訊"}
    )
    print("Created new collection")

    df = pd.read_csv('001.csv')
    df['說明'] = '地址:' + df['地址']+',' + \
    '經度:' + df['經度'].astype(str)+',' + \
    '緯度:' + df['緯度'].astype(str)+',' + \
    '充電樁數量' + df['充電樁數量']

    result_df = df[['充電樁位置','說明']]
    result_df.columns = ['Title','Text']
    
    
    # 创建DataFrame
    df = result_df.copy()       

    #準備要加入ChromaDb的資料
    # Generate embeddings
    embeddings = doc_search.create_document_embeddings(df)
    print(embeddings)
    documents= df['Text'].tolist()
    metadatas =[{'title': title} for title in df['Title'].tolist()]
    ids = [str(i) for i in range(len(documents))]

    #將資料加入ChromaDb
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    #檢查是否成功加入   
    print(collection.peek())
    print("資料已成功儲存至ChromaDb")




if __name__ == "__main__":
    train_and_save_embeddings()