from Backend.Cohere import LLM
from Backend.TTS import TTS
from json import dumps
import requests as rq
import re
from rich import print

uri = "https://divy118-homeautomationr.hf.space"
# https://divy118-homeautomationr.hf.space/home
system_prompt = """\
```python
Home = {}
```
this is the dictionary of home appliances and their values with all possible values. on your commands you can update the values. and you can control users home appliances. on every query you will get The latest updated values.
you can update values by using python syntax.

```python
Home["appliance"]["value"] = 1
Home["appliance"]["value"] = 0
```
this was just an example you can update many values at once using python.
DO NOT Ask For clarification just do the closest what you understand.
"""

llm = LLM(max_tokens=2048, messages=[], system_prompt=system_prompt)


llm.add_message("User", "Hello, how are you?")

llm.add_message("Chatbot", "I'm doing well, thank you!")

llm.add_message("User", "the bed room light turn on")

llm.add_message("Chatbot", "turning on the light .\n```python\nHome['bulb'].update({'value': 1})\n```")

llm.add_message("User", "turn off the bulb of bed room light")

llm.add_message("Chatbot", "turning off the light .\n```python\nHome['bulb'].update({'value': 0})\n```")



Home = {}

def GetHomeSystem():
    global Home
    response = rq.get(uri+"/home").json()
    Home = response
    return system_prompt.format(dumps(response, indent=4))

def SetHome(data):
    global Home
    response = rq.post(uri+"/home", json=data).json()
    Home = response
    return system_prompt.format(dumps(response, indent=4))

def Call(prompt: str):
    global Home
    llm.messages = llm.messages[1:]
    llm.messages.insert(0, {"role": "System", "message": GetHomeSystem()})
    llm.add_message("User", prompt)
    response = llm.run(prompt=prompt)
    
    if ExtractPythonCode(response) is not None:
        try:
            print(f"{response = }")
            exec(ExtractPythonCode(response))
        except Exception as e:
            print(e)
            print("[red]Retrying[/red]")
            try:
                response = llm.run(prompt=prompt)
                print(f"{response = }")
                exec(ExtractPythonCode(response))
            except Exception as e:
                print(e)
        
        SetHome(Home)
    llm.add_message("Chatbot", response)
    return response


def ExtractPythonCode(response: str):
    regex = r"```python\n(.*)\n```"
    matches = re.findall(regex, response, re.DOTALL)

    if len(matches) > 0:
        return matches[0]
    else:
        return None


def HomeAutomation(command):
    print("[green]Home Automation[/green]")
    print(command)
    x = Call(command)
    print(x)


if __name__ == "__main__":
    while True:
        HomeAutomation(input(">>> "))

# connect esp8266
# okay