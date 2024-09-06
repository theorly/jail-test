# jailbreak-gpt
 Thesis project for studying the Jailbreak of LLMs. 
**This is a tool in development yet, so many more features have to be added.**  
For the moment the tool has been created from command line and to run it you need to have all the necessary requirements as well as the API_KEY of Google Gemini and Claude that, For reasons of privacy and lack of resources, they have been hidden in the code.

# LLM now supported: 
- Gemini 
- LLama3
- Claude
- Gemma2 

# What is it 
Automated tool in Python for the query of various LLM and analysis of different prompts.  
When the queries to the various LLMs are finished, a .json file is created containing the "chat_history".

# How to use 

Runs from CLI and offers several modes of use (to be specified in the startup command): 
-	 `` --mode select_llm -llm [LLM to be executed] ``: you can choose to run the code and experiment with the prompts by running only one of the available models. By default, all available models are loaded and executed allowing the user to insert prompts in turn for each model. 
-  ``--prompt_file [PATH] --prompt_id [ID]``: you can specify a path to a specific ". xlsx" or ". csv" , appropriately made, from which to load the prompts. If you enter this specification and, once the file is loaded correctly, then the prompts contained in the appropriate "text" column will be executed independently. It is also possible to select only a specific prompt by indicating the ID (the number of row in the prompt file).

*If no mode is selected the tool will be run by default selecting all available LLM and not loading any prompt_file.*

Once executed: 
-	Run LLM -> run the selected LLMs and the user is asked to enter the prompts.
-	Get token counts -> utility function for counting tokens. 
-	Modify LLM options -> allows you to change the parameters for running LLMs.
-	Exit

# EXAMPLE OF USE 

![Simple example](docs/img.jpg)

# VIDEO DEMO
<a align="center" href="https://www.youtube.com/watch?v=hSxCJx23zDo">
  <img src="https://markdown-videos-api.jorgenkh.no/url?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DhSxCJx23zDo" alt="Demo" title="Demo"/>
</a>
