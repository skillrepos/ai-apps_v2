# AI 3-in-1: Agents, RAG and Local Models
## Building out an AI agent that uses RAG and runs locally
## Session labs 
## Revision 4.5 - 02/23/26

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**NOTES**
- To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.
- If your codespace has to be restarted, run these commands again!
  ```
  ollama serve &
  python warmup_models.py
  ```

<br><br><br>
**Lab 1 - Using Ollama to run models locally**

**Purpose: In this lab, we’ll start getting familiar with Ollama, a way to run models locally.**

---

**What the Ollama example does**
- Starts a local Ollama server inside the Codespace so you can run models locally.
- Pulls a small model (`llama3.2:1b`) and creates an alias (`llama3.2:latest`) used by the rest of the workshop.
- Runs the model interactively (`ollama run`) and via HTTP (`/api/generate`) to show the two common access patterns.
- Runs a simple Python script (`simple_ollama.py`) that calls Ollama programmatically using LangChain’s Ollama integration.

**What it demonstrates**
- The difference between:
  - **Interactive CLI usage** (quick testing),
  - **Direct HTTP API calls** (service-style integration),
  - **Python integration** (application development).
- Why “local model execution” matters for workshops and prototyping:
  - consistent environment, no cloud account required, predictable tooling.
- The importance of using a consistent model tag/alias (`llama3.2:latest`) so later labs behave consistently.

---

### Steps


1. The Ollama app is already installed as part of the codespace setup via [**scripts/startOllama.sh**](./scripts/startOllama.sh). Start it running with the first command below. (If you need to restart it at some point, you can use the same command. To see the different options Ollama makes available for working with models, you can run the second command below in the *TERMINAL*. 

```
ollama serve &
<Hit Enter>
ollama --help
```

<br><br>

2. Now let's find a model to use. Go to https://ollama.com and in the *Search models* box at the top, enter *llama*. In the list that pops up, choose the entry for "llama3.2".

![searching for llama](./images/31ai7.png?raw=true "searching for llama")

<br><br>

3. This will put you on the specific page about that model. Scroll down and scan the various information available about this model.
![reading about llama3.2](./images/31ai37.png?raw=true "reading about llama3.2")

<br><br>

4. Switch back to a terminal in your codespace. Run the first command to see what models are loaded (none currently). Then pull the latest (3b parameters) model down with the second command. (This will take a few minutes.)

```
ollama list
ollama pull llama3.2
```

![pulling the model](./images/31ai9.png?raw=true "pulling the model")

<br><br>

5. Once the model is downloaded, you can see it with the first command below. Then run the model with the second command below. This will load it and make it available to query/prompt. 

```
ollama list
ollama run llama3.2:latest
```

<br><br>

6. Now you can query the model by inputting text at the *>>>Send a message (/? for help)* prompt.  Let's ask it about what the weather is in Paris. What you'll see is it telling you that it doesn't have access to current weather data and suggesting some ways to gather it yourself.

```
What's the current weather in Paris?
```

![answer to weather prompt and response](./images/31ai10.png?raw=true "answer to weather prompt and response")

<br><br>

7. Now, let's try a call with the API. You can stop the current run with a Ctrl-D or switch to another terminal. Then put in the command below (or whatever simple prompt you want). 

```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "What causes weather changes?",
  "stream": false
}' | jq -r '.response'
```

<br><br>

8. This will take a minute or so to run. You should see a long text response . You can try out some other prompts/queries if you want.

![query response](./images/aiapps37.png?raw=true "Query response")

<br><br>

9. Now let's try a simple Python script that uses Ollama programmatically. We have a basic example script called `simple_ollama.py`. Take a look at it either via [**simple_ollama.py**](./simple_ollama.py) or via the command below.

```
code simple_ollama.py
```

You should see a simple script that:
- Imports the ChatOllama class from langchain_ollama
- Initializes the Ollama client with the llama3.2 model
- Takes user input
- Sends it to Ollama
- Displays the response

![simple ollama](./images/31ai36.png?raw=true "simple ollama")


<br><br>

10. Now you can run the script with the command below. 

```
python simple_ollama.py
```

<br><br>

11. When prompted, enter a question like "What is the capital of France?" and press Enter. You should see the model's response printed to the terminal. This demonstrates how easy it is to integrate Ollama into a Python application. Feel free to try other prompts. 

![query](./images/31ai35.png?raw=true "query")


<br><br>

12. In preparation for the remaining labs, let's get the model access approaches "warmed up". Start the command below and just leave it running while we continue (if it doesn't finish quickly).

```
python warmup_models.py
```

<p align="center">
**[END OF LAB]**
</p>
</br></br>


**Lab 2 - Creating a simple agent**

**Purpose: In this lab, we’ll learn the basics of agents and create a simple one. We’ll observe the agent loop (plan → tool call → result) via the program’s logged steps and tool inputs/outputs.**

---

**What the agent example does**
- Uses a local Ollama-served LLM (llama3.2) to interpret a weather request and decide when to call a tool.
- Extracts a location (or coordinates) from the input and calls Open-Meteo to fetch current/forecast weather data.
- Produces a short, user-friendly summary by iterating through an agent loop.

**What it demonstrates**
- How to integrate **LangChain + Ollama** to drive an agent workflow.
- An observable agent trace: **plan → tool call → tool result → response** (including tool arguments and outputs).
- Basic tool/function calling patterns and how tools ground the final answer in external data.

---

### Steps

1. For this lab, we have the outline of an agent in a file called *agent.py* in the project's directory. You can take a look at the code either by clicking on [**agent.py**](./agent.py) or by entering the command below in the codespace's terminal.
   
```
code agent.py
```

![starting agent code](./images/31ai38.png?raw=true "Starting agent code")

<br><br>

2. As you can see, this outlines the steps the agent will go through without all the code. When you are done looking at it, close the file by clicking on the "X" in the tab at the top of the file.

<br><br>

3. Now, let's fill in the code. To keep things simple and avoid formatting/typing frustration, we already have the code in another file that we can merge into this one. Run the command below in the terminal.

```
code -d labs/common/lab2_agent_solution.txt agent.py
```

<br><br>

4. Once you have run the command, you'll have a side-by-side in your editor of the completed code and the **agent.py** file.
  You can merge each section of code into **agent.py** by hovering over the middle bar and clicking on the arrows pointing right. Go through each section, look at the code, and then click to merge the changes in, one at a time.

![Side-by-side merge](./images/31ai39.png?raw=true "Side-by-side merge") 

<br><br>

5. When you have finished merging all the sections in, the files should show no differences. Save the changes simply by clicking on the "X" in the tab name.

![Merge complete](./images/31ai40.png?raw=true "Merge complete") 

<br><br>

6. Now you can run your agent with the following command:

```
python agent.py
```

![Running the agent](./images/31ai41.png?raw=true "Running the agent")

<br><br>

7. The agent will start running and will prompt for a location (or "exit" to finish). At the prompt, you can type in a location like "Paris, France" or "London" or "Raleigh" and hit *Enter*. You may see activity while the model is loaded. After that you'll be able to see the Thought -> Action -> Observation loop in practice as each one is listed out. You'll also see the arguments being passed to the tools as they are called. Finally you should see a human-friendly message summarizing the weather forecast.

![Agent run](./images/31ai42.png?raw=true "Agent run") 

<br><br>

8. You can then input another location and run the agent again or exit. Note that if you get a timeout error, the API may be limiting the number of accesses in a short period of time - it should retry on its own and return a result.

<br><br>

9. Try putting in *Sydney, Australia* and then check the output against the weather forecast on the web. Why do you think it doesn't match? How would you fix it?

Here's a clue: "If latitude/longitude is in the Southern or Western hemisphere, use negative values as appropriate"


<p align="center">
**[END OF LAB]**
</p>
</br></br>


**Lab 3 - Exploring MCP**

**Purpose: In this lab, we'll see how MCP can be used to standardize an agent's interaction with tools.**

---

**What the MCP example does**
- Implements an **MCP server** using `FastMCP` that exposes weather-related tools.
- Connects an **MCP client agent** that uses an LLM to decide which MCP tools to invoke.
- Handles retries/timeouts and demonstrates robustness when tool calls fail.

**What it demonstrates**
- How **FastMCP** standardizes tool interfaces via JSON-RPC with minimal boilerplate.
- Clean separation between **tool hosting (server)** and **agent orchestration (client + LLM)**.
- Protocol-first design: capability listing, structured tool schemas, and transport configuration (stdio vs streamable HTTP).

---

### Steps

1. We have partial implementations of an MCP server and an agent that uses an MCP client to connect to tools on the server. So that you can get acquainted with the main parts of each, we'll build them out as we did the agent in the second lab - by viewing differences and merging. Let's start with the server. Run the command below to see the differences.

```
code -d labs/common/lab3_server_solution.txt mcp_server.py
```

As you look at the differences, note that we are using FastMCP to more easily set up a server, with its *@mcp.tool* decorators to designate our functions as MCP tools. Also, we run this using the *streamable-http* transport protocol. Review each difference to see what is being done, then use the arrows to merge. When finished, click the "X" in the tab at the top to close and save the files.

![MCP server code](./images/31ai44.png?raw=true "MCP server code") 

<br><br>

2. Now that we've built out the server code, run it using the command below. You should see some startup messages similar to the ones in the screenshot.

```
python mcp_server.py
```

![MCP server start](./images/31ai18.png?raw=true "MCP server start") 

<br><br>

3. Since this terminal is now tied up with the running server, we need to have a second terminal to use to work with the client. So that we can see the server responses, let's just open another terminal side-by-side with this one. To do that, over in the upper right section of the *TERMINAL* panel, find the plus sign and click on the downward arrow next to it. (See screenshot below.) Then select "Split Terminal" from the popup menu. Then click into that terminal to do the steps for the rest of the lab. (FYI: If you want to open another full terminal at some point, you can just click on the "+" itself and not the down arrow.)

![Opening a second terminal](./images/aiapps38.png?raw=true "Opening a second terminal") 

<br><br>

4. We also have a small helper script that connects to the MCP server and **lists the available tools** (for demo purposes).
  Take a look at the code in `tools/discover_tools.py`, then run it to print the server’s tool list: (Make sure to click back in the terminal before typing the second command.)

```
code tools/discover_tools.py
python tools/discover_tools.py
```

![Discovering tools](./images/31ai33.png?raw=true "Discovering tools") 

<br><br>

5. Now, let's turn our attention to the agent that will use the MCP server through an MCP client interface. First, in the second terminal, run a diff command so we can build out the new agent.

```
code -d labs/common/lab3_agent_solution_dynamic.txt mcp_agent.py
```

<br><br>

6. Review and merge the changes as before. What we're highlighting in this step are the overall flow, the *System Prompt* that drives the LLM used by the agent, how the agent decides which tool to call via MCP via the LLM output, etc. When finished, close the tab to save the changes as before.

![Agent using MCP client code](./images/31ai43.png?raw=true "Agent using MCP client code") 

<br><br>
   
7. After you've made and saved the changes, you can run the client in the terminal with the command below. **Note that there may be a long pause initially while the model is loaded and processed before you get the final answer. This could be on the order of minutes.**

```
python mcp_agent.py
```

<br><br>

8. The agent should start up, and wait for you to prompt it about weather in a location. You'll be able to see similar TAO output. And you'll also be able to see the server INFO messages in the other terminal as the MCP connections and events happen. A suggested prompt is below.

```
What is the weather in New York?
```

![Agent using MCP client running](./images/aiapps40.png?raw=true "Agent using MCP client running") 

<br><br>


9. Because we're using a tool to do the geolocation (get latitude and longitude), you can also put in locations like Sydney, Australia and get accurate results.

![Agent using MCP client running](./images/31ai45.png?raw=true "Agent using MCP client running") 

<br><br>

10.  When you're done, you can use 'exit' to stop the client and CTRL-C to stop the server. 

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 4 - Working with Vector Databases**

**Purpose: In this lab, we’ll learn about how to use vector databases for storing supporting data and doing similarity searches.**

---

**What the vector database example does**
- Builds a local vector index using ChromaDB for:
  - the repository’s Python files (code indexing), and
  - a PDF document (`data/offices.pdf`) containing office information.
- Uses an embedding model to convert chunks of text into vectors.
- Runs a search tool that retrieves the top matching chunks using similarity scoring.

**What it demonstrates**
- **Retrieval-only semantic search**:
  - embeddings + vector similarity return relevant chunks,
  - but do **not** generate a natural-language answer by themselves.
- Why chunking + embeddings enable “meaning-based” search beyond keywords.
- How the same retrieval approach applies to different sources (code vs PDF).
- How similarity scores help you compare results and judge confidence before you generate an answer (Lab 5).

---

### Steps

1. For this lab and the next one, we have a data file that we'll be usihg that contains a list of office information and details for a ficticious company. The file is in [**data/offices.pdf**](./data/offices.pdf). You can use the link to open it and take a look at it.

![PDF data file](./images/31ai23.png?raw=true "PDF data file") 

<br><br>

2. In our repository, we have some simple tools built around a popular vector database called Chroma. There are two files which will create a vector db (index) for the *.py files in our repo and another to do the same for the office pdf. You can look at the files either via the usual "code <filename>" method or clicking on [**tools/index_code.py**](./tools/index_code.py) or [**tools/index_pdf.py**](./tools/index_pdf.py). 

```
code tools/index_code.py
code tools/index_pdf.py
```

<br><br>

3. Let's create a vector database of our local python files. Run the program to index those as below. You'll see the program loading Chroma's built-in embedding model that will turn the code chunks into numeric represenations in the vector database and then it will read and index our *.py files. **When you run the command below, there may be a pause while things get loaded.**

```
python tools/index_code.py
```

![Running code indexer](./images/31ai53.png?raw=true "Running code indexer")

<br><br>

4. To help us do easy/simple searches against our vector databases, we have another tool at [**tools/search.py**](./tools/search.py). This tool connects to the ChromaDB vector database we create, and, using cosine similarity metrics, finds the top "hits" (matching chunks) and prints them out. You can open it and look at the code in the usual way if you want. No changes are needed to the code.

```
code tools/search.py
```

<br><br>

5. Now, let's run the search tool against the vector database we built in step 3. You can prompt it with phrases related to our coding like any of the ones shown below. When done, just type "exit".  Notice the top hits and their respective cosine similarity values. Are they close? Farther apart?

```
python tools/search.py

convert celsius to farenheit
fastmcp tools
embed model sentence-transformers
async with Client mcp
```

![Running search](./images/31ai54.png?raw=true "Running search")

<br><br>

6.  Now, let's recreate our vector database based off of the PDF file. Type "exit" to end the current search. Then run the indexer for the pdf file.

```
python tools/index_pdf.py
```

![Indexing PDF](./images/31ai55.png?raw=true "Indexing PDF")

<br><br>

7. Now, we can run the same search tool to find the top hits for information about offices. Below are some prompts you can try here. Note that in some of them, we're using keywords only found in the PDF document. Notice the cosine similarity values on each - are they close? Farther apart?  When done, just type "exit".

```
python tools/search.py

Queries:
Corporate Operations office
Seaside cities
Tech Development sites
High revenue branch
```

![PDF search](./images/31ai56.png?raw=true "PDF search")

<br><br>

8. Keep in mind this is **retrieval only**: it uses an **embedding model** to find similar chunks, but it does **not** use a generative model to compose a natural-language answer. In Lab 5, we’ll add a generative step to produce a more user-friendly response grounded in retrieved content.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

    
**Lab 5 - Using RAG with Agents**

**Purpose: In this lab, we’ll explore how agents can leverage external data stores via RAG and tie in our previous tool use.**

---

**What the RAG + agent example does**
- Adds a **RAG search tool** (`search_offices`) that the agent can call to find office information from the Lab 4 vector database.
- Uses the same **TAO (Thought-Action-Observation) loop** from Labs 2 and 3, where the **LLM decides** which tools to call and in what order.
- Combines **local tools** (vector search) with **remote tools** (MCP server) in a single agent workflow.
- Produces office information grounded in retrieved content + live weather from MCP tools.

**What it demonstrates**
- A complete “AI 3-in-1” agentic workflow:
  - **Local model** (LLM via Ollama drives all decisions),
  - **RAG retrieval** (ChromaDB vector search as an agent tool),
  - **MCP tool use** (weather/geocoding via the Lab 3 server).
- **True agentic behavior**: the LLM controls the workflow — it decides to search offices first, extract the city, geocode it, get weather, and convert the temperature. The code doesn't hardcode this sequence.
- How “version 2” enhances the agent's final answer by having the LLM compose a natural language summary with an interesting fact about the city.

---

### Steps

1. For this lab, we're going to build an agent that uses RAG (from Lab 4's vector database) combined with MCP tools (from Lab 3's server) to answer questions about company offices and their local weather — all driven by the LLM through a TAO loop (like Labs 2 and 3).

<br><br>

2. We have a starter file for the new agent in [**rag_agent.py**](./rag_agent.py). As before, we'll use the "view differences and merge" technique to learn about the code we'll be working with. The command to run this time is below. Note how this agent has a system prompt describing all four tools (`search_offices` + three MCP tools) and a TAO loop that can dispatch to either local or remote tools. Take some time to look at each section as you merge them in.

```
code -d labs/common/lab5_agent_solution.txt rag_agent.py
```

![Code for rag agent](./images/31ai49.png?raw=true "Code for rag agent") 

<br><br>

3. When you're done merging, close the tab as usual to save your changes. Now, if the MCP server is not still running from lab3, in a terminal, start it running again:

```
python mcp_server.py
```

<br><br>

4. In a separate terminal, start the new agent running.

```
python rag_agent.py
```

<br><br>

5. You'll see a *User:* prompt when it is ready for input from you. The agent is geared around you entering a prompt about an office. Try a prompt like one of the ones below about office "names" that are only in the PDF. **NOTE: After the first run, subsequent queries may take longer due to retries required for the open-meteo API that the MCP server is running.** 

```
Tell me about HQ
Tell me about the Southern office
```

![Agent query about HQ](./images/31ai50.png?raw=true "Agent query about HQ") 

<br><br>

6. What you should see is the agent's TAO loop in action — just like in Labs 2 and 3! The LLM will think about what to do, call `search_offices` to find relevant office data from the vector database, then geocode the city, get the weather, and convert the temperature. Each step shows the Thought, Action, and Observation. At the end, it displays the collected office and weather information.
 
![Running the RAG agent](./images/31ai47.png?raw=true "Running the RAG agent") 

<br><br>

7. After the initial run, you can try prompts about other offices or cities mentioned in the PDF. Type *exit* when done.

<br><br>

8. While the agent works well and demonstrates true agentic behavior, the final output just displays the raw collected data. Let's enhance the agent so that when it finishes, the LLM composes a friendly, natural language summary that includes office details, weather, and an interesting fact about the city. To see and make the changes you can do the usual diff and merge using the command below.

```
code -d labs/common/lab5_agent_solution_v2.txt rag_agent.py
```

![Updating the RAG agent](./images/31ai51.png?raw=true "Updating the RAG agent") 

<br><br>

9. Once you've finished the merge, you can run the new agent code the same way again.

```
python rag_agent.py
```

<br><br>

10. Now, you can try the same queries as before and you should get more user-friendly answers with the LLM generating a natural language summary.

```
Tell me about HQ
Tell me about the Southern office
```

![Running the updated RAG agent](./images/31ai52.png?raw=true "Running the updated RAG agent")

<br><br>

11. When done, you can stop the MCP server via Ctrl-C and "exit" out of the agent.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 6 - Preparing the App for Deployment**

**Purpose: In this lab, we'll make the agent self-contained and deployable by adding an LLM provider abstraction and switching the MCP server from HTTP to stdio transport.**

---

**What the deployable agent does**
- Introduces an **LLM provider** layer (`llm_provider.py`) that automatically selects the right backend:
  - **Ollama** when running locally (Codespaces / laptop)
  - **HuggingFace Inference API** when deployed to HF Spaces (uses `HF_TOKEN`)
- Rebuilds the agent as a **self-contained** file (`hf_agent.py`) that starts the MCP server as a **subprocess** via stdio transport — no need to launch it separately.
- Keeps the same TAO loop and RAG search from Lab 5 — the agent logic is unchanged.

**What it demonstrates**
- **Provider pattern**: A single `get_llm()` function hides the complexity of choosing between local and cloud LLMs — the rest of the code never needs to know which one is running.
- **Stdio MCP transport**: Instead of running the MCP server separately over HTTP, the agent spawns it as a child process and talks MCP protocol over stdin/stdout. This is the standard production pattern for embedding an MCP server in a deployment.
- **Async wrapper**: Since the MCP client is async, we wrap the agent loop with `asyncio.run()` to give Gradio a simple synchronous `run_agent()` entry point.

---

### Steps

1. First, we need to install the additional packages for Hugging Face and Gradio support. Run the following command:

```
pip install huggingface_hub gradio
```

<br><br>

2. Let's start with the LLM provider — the key piece that lets our app run with either Ollama (local) or HuggingFace (cloud). We have a starter file at [**llm_provider.py**](./llm_provider.py). Open the diff and merge view:

```
code -d labs/common/lab6_llm_provider_solution.txt llm_provider.py
```

<br><br>

3. Review each section as you merge. Key things to note:
   - **HFResponse** class wraps HF API responses to look like LangChain responses
   - **HFLLMWrapper** class creates a HuggingFace `InferenceClient` and provides the same `.invoke(messages)` interface as ChatOllama
   - **get_llm()** checks for `HF_TOKEN` in the environment — if found, returns the HF wrapper; otherwise returns ChatOllama

   When finished merging, close the tab to save.

<br><br>

4. Let's test the provider. Since we're running locally with Ollama, it should automatically select the local backend:

```
python llm_provider.py
```

You should see "LLM Provider: Ollama (local)" followed by a response from the model.

<br><br>

5. Now let's build the self-contained agent. This is based on Lab 5's `rag_agent.py` but with two key changes: it uses `llm_provider` instead of ChatOllama directly, and it starts the MCP server as a **subprocess via stdio** instead of connecting over HTTP. Open the diff view:

```
code -d labs/common/lab6_agent_solution.txt hf_agent.py
```

<br><br>

6. Review and merge each section. The main things to notice:
   - The **imports** bring in `Client` from FastMCP and `StdioServerParameters` from the `mcp` library — no direct import of mcp_server.py
   - **Section 1** has the `MCP_SERVER` config using `StdioServerParameters` — this tells FastMCP to spawn `mcp_stdio_wrapper.py` as a subprocess and communicate via stdin/stdout
   - **Section 3** has the `unwrap()` function (same as Lab 5) to extract plain values from MCP result wrappers
   - **Section 4** has the same system prompt from Lab 5
   - **Section 5** has the async TAO loop — `async with Client(MCP_SERVER) as mcp:` spawns the MCP server subprocess and dispatches weather tools via `await mcp.call_tool(action, args)`
   - **Section 6** has the sync wrapper `run_agent()` that uses `asyncio.run()` so Gradio can call it easily

   When finished merging, close the tab to save.

<br><br>

7. Now let's run the deployable agent. Note: **no separate MCP server needed** — the agent starts it automatically via stdio!

```
python hf_agent.py
```

<br><br>

8. Try the same queries you used in Lab 5:

```
Tell me about HQ
Tell me about the Southern office
```

You should see the same TAO loop output and natural language summaries as before — the behavior is identical, just self-contained.

<br><br>

9.  When done, type "exit" to stop the agent.

<p align="center">
**[END OF LAB]**
</p>
</br></br>


**Lab 7 - Adding a Gradio Interface**

**Purpose: In this lab, we'll add a professional web interface using Gradio on top of our deployable agent.**

---

**What the Gradio interface does**
- Wraps the self-contained agent from Lab 6 in a **professional chat interface** using Gradio's `gr.Blocks` layout system.
- Provides a sidebar with office data and workflow explanation.
- Includes example query buttons for quick testing.
- Uses a pre-built theme (`gr.themes.Soft()`) and custom CSS for a polished look.

**What it demonstrates**
- **Gradio Blocks**: Flexible layout with rows, columns, and nested components.
- **Chat component**: `gr.Chatbot` manages conversation history automatically.
- **Event handlers**: `.click()` and `.submit()` wire UI actions to Python functions.
- **Graceful fallback**: If the agent isn't available, the UI runs in demo mode.

---

### Steps

1. We have a starter Gradio interface at [**gradio_app.py**](./gradio_app.py). Let's build it out with the diff and merge approach:

```
code -d labs/common/lab7_gradio_solution.txt gradio_app.py
```

<br><br>

2. Review and merge each section. Key things to note:
   - **Section 2** has the `chat_handler()` function — it takes a user message, calls `run_agent()` from `hf_agent.py`, and returns the updated conversation history
   - **Section 3** has the Gradio layout — a `gr.Chatbot` for the conversation, a `gr.Textbox` for input, Send/Clear buttons, and example query buttons
   - **Section 4** has the event handlers — `.click()` and `.submit()` connect the UI components to `chat_handler()`

   When finished merging, close the tab to save.

<br><br>

3. Now, let's run the Gradio app:

```
python gradio_app.py
```

<br><br>

4. When this starts, you should see a pop-up in the lower right that has a button to click to open the app. Click that to open it in a new browser tab. If it opens a new codespace instance instead, close that tab, go back, and try again.

Alternatively, switch to the *PORTS* tab (next to *TERMINAL*) in the codespace, find the row for port *7860*, hover over the second column, and click on the globe icon.

<br><br>

5. Once the app opens, you'll see the professional interface with a chat area on the left and office information on the right. Try entering a query like:

```
Tell me about HQ
```

<br><br>

6. You should see the agent process your query and return a natural language summary with office details and live weather. Try the example buttons at the bottom of the chat area for quick queries.

<br><br>

7. Try a few more queries to see the agent in action. Each conversation is maintained in the chat history.

<br><br>

8. When done, stop the Gradio app with Ctrl-C in the terminal.

<p align="center">
**[END OF LAB]**
</p>
</br></br>


**Lab 8 - Deploying to Hugging Face**

**Purpose: Deploying the full app into a Hugging Face Space.**

1. You will need the Hugging Face userid and token value that you created in the README at the beginning of the labs. Make sure you have those handy.

<br><br>

2. Make sure you are logged into huggingface.co. Go to [https://huggingface.co/spaces](https://huggingface.co/spaces) and click on the *New Space* button on the right.

<br><br>

3. On the form for the new Space, provide a name (e.g. "ai-office-assistant"), optionally a description and license. Make sure **Gradio** is selected as the *Space SDK*. You can accept the rest of the defaults on that page. Scroll to the bottom and click *Create Space*.

<br><br>

4. On the next page, we need to setup a secret with our HF token. Click on the *Settings* link on the top right.

<br><br>

5. On the Settings page, scroll down until you find the *Variables and secrets* section. Then click on *New secret*.

<br><br>

6. In the dialog, set the Name to **HF_TOKEN**, add a description if you'd like, and paste your actual Hugging Face token value, then click *Save*.

<br><br>

7. Now, in the root of the project in a terminal, run the following commands to clone the space. Replace *HF_USERID* with your actual Hugging Face userid. (If you named your space something other than "ai-office-assistant", replace that in the commands below.)

```
git clone https://huggingface.co/spaces/HF_USERID/ai-office-assistant
cd ai-office-assistant
```

<br><br>

8. We have a script to get files set up for the Hugging Face deployment. Run the script from this directory as follows:

```
../scripts/prepare_hf_spaces.sh .
```

This will copy the necessary Python files (including `mcp_server.py` and `mcp_stdio_wrapper.py` for the stdio MCP connection) and the pre-built vector database, and create a `requirements.txt` and `README.md` configured for Hugging Face Spaces.

<br><br>

9. Now, do the usual Git commands to push your files to the new space:

```
git add .
git commit -m "initial commit"
git push
```

<br><br>

10. When you run `git push`, VS Code/the codespace will prompt you at the *top* of the screen for your Hugging Face username. Enter your username and hit *Enter*. You will then be prompted for your password — **this is your Hugging Face token value**. Copy and paste the token value into the box.

<br><br>

11. Switch back to your Space on Hugging Face and click on the *App* link at the top. You should see that your app is in the process of building. After a few minutes, the app will be live and you can interact with it just like you did locally — but now it's running on the HuggingFace Inference API instead of Ollama!

<br><br>

12. Congratulations! You've taken an AI agent from a local prototype through to a deployed web application. The same agent code, the same RAG pipeline, the same tools — just with a professional interface and a cloud LLM backend.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

<p align="center">
**For educational use only by the attendees of our workshops.**
</p>

<p align="center">
**(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.**
</p>

