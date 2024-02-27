import os
from audio import get_audio
from custom_tools import getDuckDuckGoTool, getGmailTool, getLightsTool

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
    from langchain.agents import load_tools
    tools = load_tools(["terminal", "arxiv"]) 
    search_tool = getDuckDuckGoTool()
    gmail_tools = getGmailTool()
    lights_tools = getLightsTool()
    for tool in lights_tools:
        tools.append(tool)

    tools.append(search_tool)
    for tool in gmail_tools:
        tools.append(tool)
    
    return tools





#Build Agent
def jarvisCom():
    
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
    jarvis = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True, agent_kwargs=agent_kwargs,
        memory=memory,)


    return jarvis



def runJarvis():
    setKeys()
    jarvis = jarvisCom()
    response = jarvis.run("From now on you are to take the role of a helper assistant named Friday. My name is Tony Stark.")
    print(response)


