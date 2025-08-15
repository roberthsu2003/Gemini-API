from google import genai
from google.genai import types
import os
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])




with gr.Blocks(title="Example") as demo:
    gr.Markdown("# Text To Summarization(總結)")
    style_radio = gr.Radio(['學術','商業','專業','口語化','條列式'],label='風格',info="請選擇總結風格",value='口語化') 
    input_text = gr.Textbox(
        label="請輸入文章",
        lines=10,
        submit_btn=True
        )
    output_md = gr.Markdown()

    @input_text.submit(inputs=[style_radio,input_text], outputs=[output_md])
    def generate_text(style:str,input_str:str):
        if style=="口語化":
            style = "請使用口語化的風格\n"
        elif style == "學術":
            style = "請使用專業學術的風格\n"
        elif style == "商業":
            style = "請使用商業文章的風格\n"
        elif style == "條列式":
            style = "請條列式重點\n"
        response = client.models.generate_content(
                                            model="gemini-2.5-flash",    
                                            contents=[input_str],
                                            config=types.GenerateContentConfig(
                                                   system_instruction=f"""
                                                   你是一位文章的總結專家,也是一位繁體中文的高手。你的任務是: 
                                                    1. 請將內容`總結`
                                                    2. {style}
                                                    """
                                                   )
                                            )
        

        return  f"{style}\n\n### 總結內容如下:\n" + response.text

demo.launch(share=True)