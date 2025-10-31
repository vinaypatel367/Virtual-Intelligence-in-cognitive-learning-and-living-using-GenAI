import requests
import os
from rich import print
from dotenv import load_dotenv
import base64

load_dotenv()

class LLM:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    def __init__(
            self,
            messages: list[dict[str, str]] = [],
            model: str = "rohan/tune-gpt-4o",
            temperature: float = 0.0,
            system_prompt: str = "",
            max_tokens: int = 2048,
            verbose: bool = False,
            api_key: str | None = None
    ) -> None:
        """
        Initializes the LLM with the given parameters.

        Args
        ----
        messages: list[dict[str, str]]
            A list of messages to initialize the LLM with.
        model: str
            The model to use for the LLM.
        temperature: float
            The temperature to use for the LLM.
        system_prompt: str
            The system prompt to use for the LLM.
        max_tokens: int
            The maximum number of tokens to use for the LLM.
        verbose: bool
            Whether to print the response from the LLM.
        api_key: str | None
            The API key to use for the LLM.
        
        example:
        >>> llm = LLM()
        >>> llm.add_message("user", "Hello, how are you?")
        >>> llm.add_message("assistant", "I'm doing well, thank you!")
        >>> llm.run("Hello, how are you?")
        >>> "I'm doing well, thank you!"
        """
        self.api_key = "sk-tune-eTDj0lYiJ9fIWLEvqdgxBq0LqxMk28tfYjt"
        self.session =  requests.session()
        self.messages = messages
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.verbose = verbose

    def run(self, prompt: str|None = None) -> str:
        """
        Runs the LLM with the given prompt.

        Args
        ----
        prompt: str
            The prompt to use for the LLM.

        Returns
        -------
        str
            The response from the LLM.

        example:
        >>> llm = LLM()
        >>> llm.add_message("user", "Hello, how are you?")
        >>> llm.add_message("assistant", "I'm doing well, thank you!")
        >>> llm.run("Hello, how are you?")
        """

        "" if not prompt else self.add_message("user", prompt)

        url = "https://proxy.tune.app/chat/completions"
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        data = {
        "temperature": self.temperature,
        
            "messages":  self.messages,
            "model": self.model,
            "stream": False,
            "frequency_penalty":  0.0,
            "max_tokens": self.max_tokens
        }
        response = self.session.post(url, headers=headers, json=data)
        print(response.json())
        return response.json()["choices"][0]["message"]["content"]

    def add_message(self, role: str, content: str, base64_image: str = "") -> None:
        """
        Adds a message to the LLM with the given role and content.

        Args
        ----
        role: str
            The role of the message.
        content: str
            The content of the message.
        base64_image: str
            The base64 image of the message.

        example
        -------
        >>> llm = LLM()
        >>> llm.add_message("user", "Hello, how are you?")
        >>> llm.add_message("assistant", "I'm doing well, thank you!")
        >>> llm.run("Hello, how are you?")
        >>> "I'm doing well, thank you!"
        """
        if content and base64_image:
            self.messages.append({
                "role": role,
                "content": [
                {
                    "type": "text",
                    "text": content
                },
                {
                    "type": "image_url", 
                    "image_url": 
                {
                    "url": f"data:image/png;base64,{base64_image}"
                }
                }
                ]
                })
        elif base64_image:
            self.messages.append(
                {
                "role": role, 
                "content": [
                    {
                    "type": "image_url", 
                    "image_url": 
                        {
                        "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]       
                }
                )
        elif content:
            self.messages.append(
                {
                "role": role, 
                "content": [
                    {
                    "type": "text",
                    "text": content
                }
                ]       
                }
                )
        else:
            raise ValueError("Both content and base64_image are None")

    
    def __getitem__(self, index) -> dict[str, str] | list[dict[str, str]]:
        """
        Returns the message at the given index.

        Args
        ----
        index: int
            The index of the message to return.

        Returns
        -------
        dict[str, str] | list[dict[str, str]]
            The message at the given index.

        example
        -------
        >>> llm = LLM()
        >>> llm.add_message("user", "Hello, how are you?")
        >>> llm.add_message("assistant", "I'm doing well, thank you!")
        >>> llm.run("Hello, how are you?")
        >>> "I'm doing well, thank you!"
        >>> llm[1]
        >>> llm[1:]
        """
        if isinstance(index, slice):
            return self.messages[index]
        elif isinstance(index, int):
            return self.messages[index]
        else:
            raise TypeError("Invalid argument type")

    def __setitem__(self, index, value) -> None:
        """
        Sets the message at the given index to the given value.

        Args
        ----
        index: int
            The index of the message to set.
        value: dict[str, str] | list[dict[str, str]]
            The value to set the message to.

        example
        -------
        >>> llm = LLM()
        >>> llm.add_message("user", "Hello, how are you?")
        >>> llm.add_message("assistant", "I'm doing well, thank you!")
        >>> llm.run("Hello, how are you?")
        >>> "I'm doing well, thank you!"
        >>> llm[1] = "I'm doing well, thank you!"
        """

        if isinstance(index, slice):
            self.messages[index] = value
        elif isinstance(index, int):
            self.messages[index] = value
        else:
            raise TypeError("Invalid argument type")


from groq import Groq
from json import load,dump
import datetime
from dotenv import load_dotenv
from os import environ

load_dotenv()
client = Groq(api_key=environ["GroqAPI"])
messages = []
System = f"""Hello, I am {environ['NickName']}, You are a very accurate and advance AI chatbot named {environ['AssistantName']} which also have realtime up-to-date information of internet.
*** Do not tell time until i ask, do not talk too much, just answer to the question.***
*** Provide Answers In a Professional Way, make sure to add fullstops, comma, question mark and use proper grammar.***
*** Reply in the same language, if the question is in hindi, then reply in hindi. if the question is in english, then reply in english.***
*** Do not provide note in the output, just answer the question and never mention your training data. ***"""

SystemChatBot = [
    {"role": "system",
    "content": System},
    {"role": "user",
    "content": "Hi"},
    {"role": "assistant",
    "content": "Hello, how can I help you?"}
    ]

DefaultMessage = [
    {
    "role": "user",
    "content": f"Hello {environ['AssistantName']}, How are you?"
    },
    {
    "role": "assistant",
    "content": f"Welcome Back {environ['NickName']}, I am doing well. How may i assist you?"
    }
]

try:
    with open("ChatLog.json","r") as f:
        messages = load(f)

except:
    with open("ChatLog.json","w") as f:
        dump(DefaultMessage,f)

def Information():
    data=""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data+=f"Use This Realtime Information. if needed\n"
    data+=f"Day: {day}\n"
    data+=f"Date: {date}\n"
    data+=f"Month: {month}\n"
    data+=f"Year: {year}\n"
    data+=f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer


def FileToBase64(file_path:str):
    """
    Convert image file to base64 string.

    Args
    ----
    file_path : str

    Returns
    -------
    base64_image : str
    """
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image

def ChatBotAI(prompt):
    try:
        with open("ChatLog.json","r") as f:
            messages:dict = load(f)

        llm = LLM()
        llm.messages = SystemChatBot + [{"role": "system", "content": Information()}] + messages
        llm.add_message("user",content=prompt, base64_image=FileToBase64("capture.png"))
        Answer = llm.run()

        messages.append({"role": "assistant", "content": Answer})

        with open("ChatLog.json","w") as f:
            dump(messages,f,indent=4)
        return  AnswerModifier(Answer)
    
    except Exception as e:
        print(e)
        with open("ChatLog.json","w") as f:
            dump([],f,indent=4)
        return ChatBotAI(prompt)

if __name__ == "__main__":
    print(ChatBotAI("what can you see in image"))

