import os
import sys
sys.path.append(os.getcwd())
from Backend.TTS import TTS
from json import dumps
import requests
import re
from rich import print
from langchain_core.tools import tool
from langchain_cohere import ChatCohere
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage



uri = "https://home-automation-v7rj.onrender.com"
microcontroller_ids = ["67927ec86496adeb5fd8ebd1"]
# https://divy118-homeautomationr.hf.space/home
system_prompt = """\
{}

This is the home automation system.
Above is the true device value.
they will automatically update in every iteration.
so they are the true value.

use tool to update the device value
"""
def get_microcontroller_and_devices():
    return requests.post(
        f"{uri}/api/get_microcontroller_and_devices",
        json={"microcontroller_ids": microcontroller_ids},
    ).json()

def get_system_prompt():
    return system_prompt.format(dumps(get_microcontroller_and_devices(), indent=4))

@tool
def update_device_value(microcontroller_id: str, device_name: str, value: str) -> dict[str, str]:
    """
    this will update the device value
    
    Parameters
    ----------
    microcontroller_id : str
        the microcontroller id
    device_name : str
        the device name
    value : str
        the value
    
    Returns
    -------
    dict
        the response from the api
    """
    return requests.post(
        f"{uri}/api/update_device_value",
        json={
            "microcontroller_id": microcontroller_id,
            "device_name": device_name,
            "value": value,
        },
    ).json()


def real_update_device_value(microcontroller_id: str, device_name: str, value: str) -> dict[str, str]:
    """
    this will update the device value
    
    Parameters
    ----------
    microcontroller_id : str
        the microcontroller id
    device_name : str
        the device name
    value : str
        the value
    
    Returns
    -------
    dict
        the response from the api
    """
    microcontroller_id = "67927ec86496adeb5fd8ebd1"
    return requests.post(
        f"{uri}/api/update_device_value",
        json={
            "microcontroller_id": microcontroller_id,
            "device_name": device_name,
            "value": value,
        },
    ).json()
# Define the Cohere LLM
llm = ChatCohere(
    cohere_api_key="CYYEC8gkzjKVuF2hTRIBiXpz7rNFDvlmxfpdJqLt",
    model="command-r-plus-08-2024",
    temperature=0,
)

llm_with_tools = llm.bind_tools([update_device_value])
messages = ['wf']


def HomeAutomation(query: str):
    s = get_system_prompt()
    messages[0] = SystemMessage(content=s)
    # print(s)
    messages.append(HumanMessage(content=query))
    r = llm_with_tools.invoke(messages)
    try:
        print(r.content)
        print(r.tool_calls)
        for tool_call in r.tool_calls:
            if tool_call["name"] == "update_device_value":
                real_update_device_value(**tool_call["args"])
    except Exception as e:
        print(f"tool {e}")
    



if __name__ == "__main__":
    while True:
        HomeAutomation(input(">>> "))