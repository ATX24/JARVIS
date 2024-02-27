from langchain.agents import Tool

def getDuckDuckGoTool():
    from langchain.tools import DuckDuckGoSearchRun, Tool
    #DuckDuckGo Tool
    search = DuckDuckGoSearchRun()

    search_tool = Tool(
        name="SearchTool",
        func=search.run,
        description="Useful when needed to search the web or get the weather",
    )
    return search_tool



#GMAIL Tool
def getGmailTool():
    from langchain.agents.agent_toolkits import GmailToolkit
    toolkit = GmailToolkit()

    # tools = toolkit.get_tools()
    # print(tools)

    from langchain_community.tools.gmail.utils import build_resource_service, get_gmail_credentials

    # Can review scopes here https://developers.google.com/gmail/api/auth/scopes
    # For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
    credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=["https://mail.google.com/"],
        client_secrets_file="credentials.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)
    gmail_tools = toolkit.get_tools()
    return gmail_tools


#Create IFTTT tool
def getLightsTool():
    from langchain.tools.ifttt import IFTTTWebhook

    key = "cuI8iZ5WcLxo8956Iy19sQ"


    onurl = f"https://maker.ifttt.com/trigger/lightson/with/key/{key}"
    offurl = f"https://maker.ifttt.com/trigger/lightsoff/with/key/{key}"

    light_tool_on = IFTTTWebhook(
        name="lightson", description="Use for turning on lights", url=onurl
    )

    light_tool_off = IFTTTWebhook(
        name="lightsoff", description="Use for turning off lights", url=offurl
    )

    return [light_tool_on, light_tool_off]


#Microsoft outlook tool: Use for non-email work activities ig (Calendar, tasks, etc)
def getMicrosoftTool():
    return 'bruh'

def getAcademicSearchTool():
    from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
    tools = [SemanticScholarQueryRun()]
    return tools

def getPythonTool():
    from langchain_experimental.utilities import PythonREPL
    python_repl = PythonREPL()

    # You can create the tool to pass to an agent
    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    )
    return repl_tool