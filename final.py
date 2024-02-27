#Combining thinky jarvis with communication jarvis
from jarvy import jarvisCom
from jarvy2 import jarvisThink
from langchain.agents import Tool
import speech_recognition as sr
import threading
import pygame
import time
from gtts import gTTS

import os
from audio import get_audio
from custom_tools import getDuckDuckGoTool, getGmailTool, getLightsTool, getPythonTool

#Set API keys
os.environ["OPENAI_API_KEY"] = "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" #Key is disabled haha I'm not that stupid


jarv1 = jarvisCom()
jarv2 = jarvisThink()

jarvisCom = Tool.from_function(
        name="emailTool",
        func=jarv1.run,
        description="Use when tasked with drafting/sending an email",
    )

jarvisThink = Tool.from_function(
        name="anyTool",
        func=jarv2.run,
        description="Use when tasked with anything other than sending an email",
    )


from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-3.5-turbo")

tools = []
tools.append(jarvisCom)
tools.append(jarvisThink)

 
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}

memory = ConversationBufferMemory(memory_key="memory", return_messages=True)


#Create agent
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

jarvis = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_kwargs=agent_kwargs,
    memory=memory,handle_parsing_errors=True)


#Two listening functions
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


#Back to the main code
stop_event = threading.Event()
while True:
    #Non audio
    print("WELCOME DHILAN SHAH. AUDIO SYSTEM DISENGAGED. SWITCHING TO MANUAL MODE.")
    q1 = input("Question: ")
    response = jarvis.run(q1)
    print(response)


    # #Audio
    # print("Stark...")
    # q1 = get_audio()
    # if 'stop listening' in q1:
    #     print('ok')
    #     break

    # if 'friday' in q1.lower():
    #     myobj = gTTS(text="on it", tld='co.uk', slow=False)
    #     myobj.save('response.mp3')
    #     os.system("mpg123 response.mp3")
    #     os.system("rm response.mp3")
    #     response = jarvis.run(q1)
    #     stop_event.clear()
    #     listen_thread = threading.Thread(target=listen_for_wake_word, args=(stop_event,))
    #     listen_thread.start()
    #     play_response(response, stop_event)
    #     listen_thread.join()




