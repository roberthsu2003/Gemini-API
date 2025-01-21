
**連結函式呼叫(呼叫完成後再呼叫下一個)**

```python
import os
import google.generativeai as genai

def find_movies(description:str, location:str = "") -> list[str]:
    """find movie titles currently playing in theaters based on any description, genre, title words, etc.

    Args:
        description: Any kind of description including category or genre, title words, attributes, etc.
        location: The city and state, e.g. San Francisco, CA or a zip code e.g. 95616
    """

    return ["Barbie", "Oppenheimer"]

def find_theaters(location: str, movie: str = ""):
    """Find theaters based on location and optionally movie title which are is currently playing in theaters.

    Args:
        location: The city and state, e.g. San Francisco, CA or a zip code e.g. 95616
        movie: Any movie title
    """
    return ["Googleplex 16", "Android Theatre"]

def get_showtimes(location: str, movie: str, theater: str, date: str):
    """
    Find the start times for movies playing in a specific theater.

    Args:
      location: The city and state, e.g. San Francisco, CA or a zip code e.g. 95616
      movie: Any movie title
      thearer: Name of the theater
      date: Date for requested showtime
    """
    return ["10:00", "11:00"]

functions = {
    "find_movies": find_movies,
    "find_theaters": find_theaters,
    "get_showtimes": get_showtimes,
}

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

model = genai.GenerativeModel(
    model_name = 'gemini-2.0-flash-exp',
    tools = functions.values()
)

chat = model.start_chat(enable_automatic_function_calling=True)
response = chat.send_message(
    "Which comedy movies are shown at tonight in Mountain view and at what time?"
)

for content in chat.history:
    print(content.role, "->", [type(part).to_dict(part) for part in content.parts])
    print("-" * 80)


```



### 平行呼叫




















