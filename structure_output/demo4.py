import gradio as gr
import google.generativeai as genai
import os
import json

with open('2025_01_29.csv',encoding='utf-8') as file:
    csv_content = file.read()
    
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction='''
    ## 請依據以下的csv格式的文字回答問題
    ## 這個表格是銀行的台幣和各幣值的轉換匯率
    ## 如果沒有資料,請輸出`沒有相關幣的資料`
    ## 規則:
        1.如果使用者輸入的是台幣要換取美金,換算公式為:
        `台幣/現金匯率本行賣出的美金價格=`
        2.如果使用者輸入的是美金換取台幣,換算公式為:
        `現金匯率本行買入美金*美金的金額=`
        3.如果不是換成台幣,請先將金額換成台幣後,再轉換為使用者要求的幣值   
    
    ''' + csv_content,
    generation_config={
        "response_mime_type":"application/json",
        "response_schema":list[str]
    }    
)

model1 = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction='''
    ## 請依據以下的csv格式的文字回答問題
    ## 這個表格是銀行的台幣和各幣值的轉換匯率
    ## 如果沒有資料,請輸出`沒有相關幣的資料`
    ## 規則:
        1.如果使用者輸入的是台幣要換取美金,換算公式為:
        `台幣/現金匯率本行賣出的美金價格=`
        2.如果使用者輸入的是美金換取台幣,換算公式為:
        `現金匯率本行買入美金*美金的金額=`
        3.如果不是換成台幣,請先將金額換成台幣後,再轉換為使用者要求的幣值   
    
    ''' + csv_content 
)

response = model.generate_content('''                                  
1. 以現有的資料,台幣可以換算的幣值有那一些?
2. 請排除無法計算的幣別
3. 請加入台幣                     
''')



with gr.Blocks() as demo:
    currencies = json.loads(response.text)
    currency_in = "台幣"
    currency_out = ""
    gr.Markdown('''
        ## 匯率試算 
        **資料來源:臺灣銀行牌告匯率**
    ''')

    in_radio = gr.Radio(currencies,label='持有幣別',info="您手上的幣別",value=currency_in)
    out_radio = gr.Radio(currencies,label='兑換幣別',info="您要轉換幣別")
    
    with gr.Row():        
        number = gr.Number(value=0,label=f'{currency_in}轉換為{currency_out}',visible=True)
        btn = gr.Button(value = '計算',visible=True)

    result_markdown = gr.Markdown()

    def radio_change(in_radio_value, in_output_value):
        """
        使用者一選取,radio,做一些初始動作
        """
        currencies_copy = currencies.copy() 
        currencies_copy.remove(in_radio_value)
        if in_radio_value and in_output_value:
            
            return [
                    gr.Number(visible=True,label=f'{in_radio_value}轉換為{in_output_value}',interactive=True),
                    gr.Button(visible=True),
                    gr.Radio(currencies_copy,label='兑換幣別',info="您要轉換幣別") 
                ]
        else:
            return [
                    gr.Number(visible=False),
                    gr.Button(visible=False),
                    gr.Radio(currencies_copy,label='兑換幣別',info="您要轉換幣別") 
                ]
    
    demo.load(lambda:[gr.Number(visible=False),gr.Button(visible=False)],outputs=[number, btn]) #一開始不顯示
    
    gr.on(
        triggers = [in_radio.change,out_radio.change],
        fn=radio_change,
        inputs = [in_radio,out_radio],
        outputs = [number,btn,out_radio]
    )

    @btn.click(inputs=[number,in_radio,out_radio,],outputs=result_markdown)
    def btn_click(number_value,in_radio_value,in_output_value):
        message = [f"請將{number_value}{in_radio_value}轉換為{in_output_value}","請輸出為markdown格式"]
        response = model1.generate_content(message)
        return response.text
             




demo.launch()