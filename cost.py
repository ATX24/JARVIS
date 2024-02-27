#Lets try to make a cheaper, more cost-effective version of jarvis
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer
import transformers

model_id = 'meta-llama/Llama-2-7b-chat-hf'

hf_auth = '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'
tokenizer = LlamaTokenizer.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)

model = LlamaForCausalLM.from_pretrained(
    model_id, load_in_8bit=True, device_map='auto', torch_dtype=torch.float16,
    use_auth_token=hf_auth
)
model.eval()

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)

generate_text = transformers.pipeline(
    model=model, tokenizer=tokenizer,
    return_full_text=True,  # langchain expects the full text
    task='text-generation',
    # we pass model parameters here too
    # stopping_criteria=stopping_criteria,  # without this model rambles during chat
    temperature=0.0,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
    max_new_tokens=512,  # mex number of tokens to generate in the output
    repetition_penalty=1.1  # without this output begins repeating
)

# ----------------------------------
# Use LangChain to generate response
# ----------------------------------
from langchain.llms import HuggingFacePipeline

llm = HuggingFacePipeline(pipeline=generate_text)
res = llm(prompt="Explain to me the difference between nuclear fission and fusion.")
print(res)
# ----------------------------------------
# Experiment with LangChain Agent and Tool
# ----------------------------------------
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import load_tools

memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=5, return_messages=True, output_key="output"
)
tools = load_tools(["llm-math"], llm=llm)

from langchain.agents import AgentOutputParser
from langchain.agents.conversational_chat.prompt import FORMAT_INSTRUCTIONS
from langchain.output_parsers.json import parse_json_markdown
from langchain.schema import AgentAction, AgentFinish

class OutputParser(AgentOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> AgentAction | AgentFinish:
        try:
            # this will work IF the text is a valid JSON with action and action_input
            response = parse_json_markdown(text)
            action, action_input = response["action"], response["action_input"]
            if action == "Final Answer":
                # this means the agent is finished so we call AgentFinish
                return AgentFinish({"output": action_input}, text)
            else:
                # otherwise the agent wants to use an action, so we call AgentAction
                return AgentAction(action, action_input, text)
        except Exception:
            # sometimes the agent will return a string that is not a valid JSON
            # often this happens when the agent is finished
            # so we just return the text as the output
            return AgentFinish({"output": text}, text)

    @property
    def _type(self) -> str:
        return "conversational_chat"


# initialize output parser for agent
parser = OutputParser()

from langchain.agents import initialize_agent

# initialize agent
agent = initialize_agent(
    agent="chat-conversational-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    early_stopping_method="generate",
    memory=memory,
    agent_kwargs={"output_parser": parser}
)

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<>\n", "\n<>\n\n"
sys_msg = B_SYS + """Assistant is a expert JSON builder designed to assist with a wide range of tasks.

Assistant is able to respond to the User and use tools using JSON strings that contain "action" and "action_input" parameters.

All of Assistant's communication is performed using this JSON format.

Assistant can also use tools by responding to the user with tool use instructions in the same "action" and "action_input" JSON format. Tools available to Assistant are:

- "Calculator": Useful for when you need to answer questions about math.
  - To use the calculator tool, Assistant should write like so:
    ```json
    {{"action": "Calculator",
      "action_input": "sqrt(4)"}}
    ```

Here are some previous conversations between the Assistant and User:

User: Hey how are you today?
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "I'm good thanks, how are you?"}}
```
User: I'm great, what is the square root of 4?
Assistant: ```json
{{"action": "Calculator",
 "action_input": "sqrt(4)"}}
```
User: 2.0
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "It looks like the answer is 2!"}}
```
User: Thanks could you tell me what 4 to the power of 2 is?
Assistant: ```json
{{"action": "Calculator",
 "action_input": "4**2"}}
```
User: 16.0
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "It looks like the answer is 16!"}}
```
User: Thanks then could you tell me what is 16 multiplied by 3 is?
Assistant: ```json
{{"action": "Calculator",
 "action_input": "16*3"}}
```
User: 48.0
Assistant: ```json
{{"action": "Final Answer",
 "action_input": "It looks like the answer is 48!"}}
```
Here is the latest conversation between Assistant and User.""" + E_SYS

new_prompt = agent.agent.create_prompt(
    system_message=sys_msg,
    tools=tools
)
agent.agent.llm_chain.prompt = new_prompt

instruction = B_INST + " Respond to the following in JSON with 'action' and 'action_input' values " + E_INST
human_msg = instruction + "\nUser: {input}"

agent.agent.llm_chain.prompt.messages[2].prompt.template = human_msg


print(agent("hey how are you today?"))

print(agent("what is 4 to the power of 2.1?"))

print(agent("can you multiply that by 3?"))
