import os
import openai

import json

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

# define a function
functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]

messages = [
    {
        "role": "user",
        "content": "What's the weather like in Boston?"
    }
]

from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=functions
)
print("Function call response:")
print(response)
print()

print("Function call:")
print(response.choices[0].message)
print()

print("Function call name:")
print(response.choices[0].message.function_call)
print()

print("Function call arguments:")
args = json.loads(response.choices[0].message.function_call.arguments)
print(args)
print()

print("Function call name:")
response_message = response.choices[0].message
print(response_message.function_call.name)
print()

print("Function call with arguments:")
print(get_current_weather(args))
print()

messages = [
    {
        "role": "user",
        "content": "hi!",
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=functions
)

print("Function call response with OpenAI to question irrelevant to weather:")
print(response)
print()

messages = [
    {
        "role": "user",
        "content": "What's the weather in Boston?",
    }
]
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=functions,
    function_call="none",
)

print("Function call response with OpenAI to question about the weather, but without function calling:")
print(response)
print()

messages = [
    {
        "role": "user",
        "content": "hi!",
    }
]
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=functions,
    function_call={"name": "get_current_weather"},
)
print("Function call response with OpenAI to question irrelevant to weather with function calling:")
print(response)
print()

messages = [
    {
        "role": "user",
        "content": "What's the weather like in Boston!",
    }
]
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=functions,
    function_call={"name": "get_current_weather"},
)
print("Function call response with OpenAI to question about the weather with function calling:")
print(response)
print()

#current state of messages
print("Current state of messages:")
print(messages)
print()

args = json.loads(response.choices[0].message.function_call.arguments)
observation = get_current_weather(args)

messages.append(
        {
            "role": "function",
            "name": "get_current_weather",
            "content": observation,
        }
)

print("Current state of messages after appending function call:")
print(messages)
print()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)
print("Final response after appending function call:")
print(response)
print()

# The complete function calling process
import json

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)
# define a function
functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]
messages = [
    {
        "role": "user",
        "content": "What's the weather like in Boston?"
    }
]
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=functions
)

args = json.loads(response.choices[0].message.function_call.arguments)
observation = get_current_weather(args)

messages.append(
        {
            "role": "function",
            "name": "get_current_weather",
            "content": observation,
        }
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)
print("Final result of a complete function calling process:")
print(response)
print()