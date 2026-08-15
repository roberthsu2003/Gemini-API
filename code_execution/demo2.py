import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


def set_light_value(brightness: int, color_temp: str) -> dict:
    """Set the brightness and color temperature of a room light. (mock API).

    Args:
        brightness: Light level from 0 to 100. Zero is off and 100 is full brightness
        color_temp: Color temperature of the light fixture, which can be `daylight`, `cool` or `warm`.

    Returns:
        A dictionary containing the set brightness and color temperature.
    """
    print("Function called with:")
    print(f"  brightness: {brightness}")
    print(f"  color_temp: {color_temp}")

    result = {
        "brightness": brightness,
        "colorTemperature": color_temp
    }
    print("Returning:", result)
    return result


client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

# 關閉自動函式呼叫,示範如何手動取出 function_call 並自行執行
response = client.models.generate_content(
    model='gemini-flash-latest',
    contents='Dim the lights so the room feels cozy and warm.',
    config=types.GenerateContentConfig(
        tools=[set_light_value],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
)
print(response)

# Create a dictionary of available functions
available_functions = {
    'set_light_value': set_light_value
}

if response.function_calls:
    print("有 function_calls")
    for call in response.function_calls:
        function_name = call.name
        args = call.args
        print(f"Function name: {function_name} ({type(function_name)})")
        print(f"Function args: {args} ({type(args)})")

        if function_name in available_functions:
            args_dict = dict(args)
            result = available_functions[function_name](**args_dict)
            print("Function result:", result)
        else:
            print(f"Function {function_name} not found")
else:
    print("模型沒有觸發 function_call,回覆文字為:", response.text)
