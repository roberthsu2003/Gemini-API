## 讀取文件(Document_understanding)
Gemini API 支援pdf輸入,保含長的文件,最高達3600頁。Gemini模型使用原生視覺處理pdf檔,因此能夠了解文字和圖像內容.透過原生pdf視覺支援,Gemini模型能夠:
- 分析文件中的圖解說明,圖表和表格
- 提取資訊轉換成為結構化資料
- 回答有關於視覺所見和文字內容的問題
- 摘要文件內容
- 抄錄文件內容(例如轉換為HTML),保留版面和格式,以便給其它應用程式使用(例如資料庫或向量資料庫)

本教學課程示範了一些將Gemini API與PDF文件結合的可能方式,所有輸出皆為純文字

## 對pdf進行提示(Prompting with PDFs)

這指南示範如何處理遠端pdf和本地端pdf上傳至模型。

文件必需是下列格式的其中一種資料格式

- pdf - application/pdf
- javascript - application/x-javascript,text/javascript
- python - application/x-python, text/x-python
- txt - text/plain
- html - text/html
- css - text/css
- markdown - text/md
- csv - text/csv
- xml - text/xml
- rtf - text/rtf

每個文件頁面相當258tokens
