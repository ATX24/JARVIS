import speech_recognition as sr
import threading
import pygame
import time
from gtts import gTTS

import os
from audio import get_audio
from custom_tools import getDuckDuckGoTool, getGmailTool, getLightsTool, getPythonTool

#Set API keys
def setKeys():
    os.environ["OPENAI_API_KEY"] = "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"



#Select LLM
def getllm():
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    return llm

#Get all tools
#Python_repl: Can execute code
#Terminal: Ability to work with files
#Arxiv: Gets scientific papers
def getTools():
    llm = getllm()
    from langchain.agents import load_tools
    tools = load_tools(["terminal", "arxiv", "pubmed"]) 
    python_tool = getPythonTool()
    search_tool = getDuckDuckGoTool()
    # gmail_tools = getGmailTool()
    lights_tools = getLightsTool()
    for tool in lights_tools:
        tools.append(tool)
    # for tool in gmail_tools:
    #     tools.append(tool)

    tools.append(search_tool)
    tools.append(python_tool)

    

    
    
    return tools





#Build Agent
def jarvisThink():
    tools = getTools()
    # llm - getllm()
    llm = getllm()
    #Memory
    from langchain.prompts import MessagesPlaceholder
    from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory

    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
   
    #Create agent
    from langchain.agents import initialize_agent, Tool
    from langchain.agents import AgentType

    #Use structured zero shot reaction in the future
    jarvis = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_kwargs=agent_kwargs,
        memory=memory,handle_parsing_errors=True)
    return jarvis

def listen_for_wake_word(stop_event, wake_word="friday"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while not stop_event.is_set():
            audio = r.listen(source, phrase_time_limit=5)
            try:
                text = r.recognize_google(audio).lower()
                if wake_word in text:
                    stop_event.set()
            except sr.UnknownValueError:
                pass

def play_response(text, stop_event):
    language = 'en'
    tts = gTTS(text=text, lang=language, tld='co.uk', slow=False)
    tts.save('response.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('response.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        if stop_event.is_set():
            pygame.mixer.music.stop()
            break
    os.remove('response.mp3')

def runJarvis():
    setKeys()
    jarvis = jarvisThink()
    # response = jarvis.run("From now on you are to take the role of a helper assistant named Friday. My name is Tony Stark.")
    # print(response)

    stop_event = threading.Event()

    while True:
        print("Stark...")
        q1 = get_audio()
        if 'stop listening' in q1:
            print('ok')
            break

        if 'friday' in q1.lower():
            myobj = gTTS(text="on it", tld='co.uk', slow=False)
            myobj.save('response.mp3')
            os.system("mpg123 response.mp3")
            os.system("rm response.mp3")
            response = jarvis.run(q1)
            stop_event.clear()
            listen_thread = threading.Thread(target=listen_for_wake_word, args=(stop_event,))
            listen_thread.start()
            play_response(response, stop_event)
            listen_thread.join()

