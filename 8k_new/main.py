from Backend.Extra import AnswerModifier, QueryModifier, LoadMessages, GuiMessagesConverter
from Backend.Automation import Automation, professional_responses
from Backend.RSE import RealTimeChatBotAI
from dotenv import load_dotenv, set_key
from Backend.Chatbot import ChatBotAI
from Backend.AutoModel import Model
from Backend.ChatGpt import ChatBotAI as ChatGptAI
from Backend.TTS import TTS
from random import choice
import mtranslate as mt
import pyautogui
import threading
import asyncio
import json
import eel
import os
import base64
from threading import Lock
from time import sleep

lock = Lock()
# say turn on 
#turn on bulb say that after i click 
load_dotenv()
state = "Available..."
messages = LoadMessages()
WEBCAM = False
js_messageslist = []
working:list[threading.Thread] = []
InputLanguage = os.environ["InputLanguage"]
Assistantname = os.environ["AssistantName"]
Username = os.environ["NickName"]

def UniversalTranslator(Text:str):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def MainExecution(Query:str):
    global state, WEBCAM
    print("Starting...")
    Query: str = UniversalTranslator(Query) if "en" not in InputLanguage.lower() else Query.capitalize()
    print("translating...")
    Query: str = QueryModifier(Query)
    if state == "Available...":
        pass
    else:
        state = "Thinking..."
    Decesion:list[str] = Model(Query)
    print(Decesion)
    if  "general" in Decesion or "realtime" in Decesion:
        if Decesion[0] == "general":
            if WEBCAM:
                python_call_to_capture()
                sleep(0.5)
                Answer = ChatGptAI(Query)
            else:
                Answer = AnswerModifier(ChatBotAI(Query))
            if state == "Available...":
                pass
            else:
                state = "Answering..."
            TTS(Answer)
        else:
            if state == "Available...":
                pass
            else:
                state = "Searching..."

            Answer = AnswerModifier(RealTimeChatBotAI(Query))

            if state == "Available...":
                pass
            else:
                state = "Answering..."
            TTS(Answer)
    elif "open webcam" in Decesion:
        python_call_to_start_video()
        print("Video Started")
        WEBCAM = True
        Decesion.remove("open webcam")
    elif "close webcam" in Decesion:
        print("Video Stopped")
        python_call_to_stop_video()
        WEBCAM = False
        Decesion.remove("close webcam")
    else:
        if state == "Available...":
            pass
        else:
            state = "Automation..."

        asyncio.run(Automation(Decesion, print))
        response = choice(professional_responses)
        state = "Answering..."
        with open("ChatLog.json","w") as f:
            json.dump(messages + [{"role": "assistant", "content": response}],f,indent=4)
        TTS(response)
    if state == "Available...":
        pass
    else:
        state = "Listening..."


@eel.expose
def js_messages():
    global js_messageslist, messages
    with lock:
        messages = LoadMessages()
    if js_messageslist != messages:
        toreturn = GuiMessagesConverter(messages[len(js_messageslist):])
        js_messageslist = messages
        return toreturn
    return []

@eel.expose
def js_state(stat=None):
    global state
    if stat:
        state = stat
    return state

@eel.expose
def js_mic(transcription):
    
    global working
    print(transcription)
    
    if not working:
        work = threading.Thread(target=MainExecution,args=(transcription, ), daemon=True)
        work.start()
        working.append(work)

    else:
        if working[0].is_alive():
            pass

        else:
            working.pop()
            work = threading.Thread(target=MainExecution,args=(transcription, ), daemon=True)
            work.start()
            working.append(work)

@eel.expose
def python_call_to_start_video():
    eel.startVideo()

@eel.expose
def python_call_to_stop_video():
    eel.stopVideo()

@eel.expose
def python_call_to_capture():
    eel.capture()

@eel.expose
def js_page(cpage = None):
    if cpage:
        if cpage=="home":
            eel.openHome()
        elif cpage=="settings":
            eel.openSettings()

@eel.expose
def js_setvalues(GeminiApi, HuggingFaceApi, GroqApi, AssistantName, Username):
    print(f"{GeminiApi = } {HuggingFaceApi = } {GroqApi = } {AssistantName = } {Username = }")
    if GeminiApi:
        set_key(".env", "CohereAPI", GeminiApi)
    if HuggingFaceApi:
        set_key(".env", "HuggingFaceAPI", HuggingFaceApi)
    if GroqApi:
        set_key(".env", "GroqAPI", GroqApi)
    if AssistantName:
        set_key(".env", "AssistantName", AssistantName)
    if Username:
        set_key(".env", "NickName", Username)

@eel.expose
def setup():
    pyautogui.hotkey("win","up")

@eel.expose
def js_language():
    return str(InputLanguage)

@eel.expose
def js_assistantname():
    return Assistantname

@eel.expose
def js_capture(image_data):
    # Convert base64 image data to bytes
    image_bytes = base64.b64decode(image_data.split(',')[1])

    # Save the image to a file
    with open('capture.png', 'wb') as f:
        f.write(image_bytes)

eel.init('web')
eel.start('spider.html', port = 4444)







