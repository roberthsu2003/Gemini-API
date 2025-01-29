import os
import google.generativeai as genai
import json

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

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    tools=[set_light_value]
)



# Add error handling and more detailed response inspection

response = model.generate_content('Dim the lights so the room feels cozy and warm.')
print(response)

if hasattr(response, 'candidates'):
    print("有candidates")
    function_name = response.candidates[0].content.parts[0].function_call.name
    args = response.candidates[0].content.parts[0].function_call.args
    print(type(function_name)) #<class 'str'>
    print(type(args)) #<class 'proto.marshal.collections.maps.MapComposite'>
    #question:How to run `function_name`
    # Create a dictionary of available functions
    available_functions = {
        'set_light_value': set_light_value
    }
    
    # Get the function from the dictionary and call it with the arguments
    if function_name in available_functions:
        # Convert MapComposite to regular dictionary if needed
        args_dict = dict(args)
        result = available_functions[function_name](**args_dict)
        print("Function result:", result)
    else:
        print(f"Function {function_name} not found")
    

