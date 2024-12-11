# jailbreak-gpt
![logo](docs/logo.jpg)
 Thesis project for studying the Jailbreak of LLMs. 
**This is a tool in development yet, so many more features have to be added.**  

**[Jailbreak-GPT](https://jailbreak-gpt.azurewebsites.net/)** 

\
# Overview

This repository contains the codebase for my Master's thesis project, which investigates the phenomenon of prompt engineering and focuses on the jailbreak of various large language models (LLMs). The models analyzed include:

- GPT-3.5 Turbo
- Gemini 1.5
- Claude 3.5 Sonnet
- Llama 3.1
- Gemma2
- Phi3
- Mistral-Nemo
- Vicuna
- Qwen2

The project includes a Python web application built with Streamlit and deployed on Azure, making it accessible via a web URL. The application offers:

A user interface to interact with individual models.

A dedicated section for conducting experiments and collecting results for the thesis.
\
# Features
\
## 1. Model Interaction Pages
\
The application provides separate web pages for interacting with each LLM. These pages allow users to:

- Submit prompts.
- View and analyze the model's responses in real-time.
\
## 2. Experimentation and Data Collection
\
A specialized section of the application is designed for experimentation, enabling users to:

- **Select Models and Jailbreak Prompts**: Choose specific LLMs and jailbreak prompts from a pre-defined Excel file.
- **Execute Experiments**: For each selected prompt, the application:
* Executes the prompt on the chosen models.
* Collects the model's response to the jailbreak prompt.
* Submits a follow-up request to bypass the model's policy.

- **Iterative Testing**: The process repeats for:
* 40 jailbreak prompts.
* 20 follow-up requests per prompt.
* All selected models.

- **Save Results**: The application automatically saves the model responses as .json files, which are stored remotely.

- **Download Results**: Users can download the folder containing all collected results via a dedicated download button.

\
## 3. Results Analysis
\
Once the results are collected in the appropriate files . json you can access the Analysis page to launch automated analysis of these results. In particular, these data are analyzed by GPT-3.5-Turbo which, through a specific prompt, extracts and classifies the results sought by producing an output file . json containing all the relevant metrics for the study. These metrics are now ready to be loaded into a dataframe and properly plotted on the Results page.

\
## 4. Results
\
In the results section all files are read. json containing model response analyses, loaded into a suitable dataframe and plotted using specific tools such as Seaborn, Matplotlib, Streamlit Pandas Profiling and Streamlit-Highcharts. 

\
# Deployment
\
The web application is deployed on Azure using App Service, ensuring scalability and accessibility. No additional setup is required beyond accessing the application URL.

# Project Structure

* main.py: Main application script.

* prompts/: Contains the list of jailbreak prompts.

* pages/: Scripts and configurations for each page.

* utils/: Utility scripts for the app.

* results/: Directory where .json files with model responses are stored.

* docs/: Folder containing the docs.

* requirements.txt: List of Python dependencies.

* run.sh : script to build the app on Azure App Service.

# Metrics 

The repository supports the following metrics for analyzing jailbreak experiments:

- **Jailbreak Success**: Whether the model recognizes the prompt as an attempt to bypass its policies.

- **Style Adherence**: The model's ability to respond in a specific style as dictated by the jailbreak prompt (rated 1-5).

- **Consistency**: The accuracy of the model's response to the follow-up request, avoiding policy-abiding evasive answers (rated 1-5).

- **Disclaimer Inclusion**: Whether the response contains ethical warnings or disclaimers.

- **Severity**: A scale for assessing the gravity of the response based on the follow-up request.

# Acknowledgments

Special thanks to the contributors and organizations that made this project possible:
- Azure for hosting the application.
- Streamlit for simplifying the creation of interactive web apps.
- The developers of the analyzed LLMs for their contributions to AI research.

# Contact

For questions or feedback, feel free to reach out:

* Name: Orlando De Bernardis

* Email: dborlando98@gmail.com

* **[Instagram](https://www.instagram.com/theorly_/)**

* **[Telegram @theorly](https://t.me/theorly/)**







