# JARVIS 🤖 🦜
Modern AI assistant powered by LangChain

Implements the LangChain OpenAIFunctions Agent

## Abilities  🚀
- Can draft emails, turn on lights, write and compile code, search the web, and work with local files

**Conversation**
- Python speech recognition library to get input
- GTTS for response output
- Activates when the user says the wake-word: "Friday" (To customize the wake word, change the condition in the runJarvis function)
  

## LLM Tools 🔨
- Gmail tool for writing custom email drafts
- Terminal tool for local-env interaction (dangerous)
- IFTTT smarthome tool to control lights
- Python_REPL to write and compile code
- Duck Duck Go search tool
- Arxiv tool for referencing scholarly articles




## To Do: 
- [ ] Improved memory solution using a vector database to store embeddings
- [ ] Use the new Llama-2 model to eliminate the need for the OpenAI API (in progress)
