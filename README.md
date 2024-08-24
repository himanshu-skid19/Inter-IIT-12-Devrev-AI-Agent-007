# Inter-IIT-12-Devrev-AI-Agent-007 (Team 15)

This is a solution for DevRev's Problem Statement at the 12th Inter IIT TechMeet aiming adepty address domain-specific user queries.

We developed a Large Language Model (LLM) powered chatbot, augmented by a set of tools (APIs), each accompanied by its detailed description. The chatbot intelligently recommends subset of tools that best match the unique context of the query, specifying precise tool arguments, and sequencing tool execution intelligently. Additionally, our solution incorporates features facilitating the seamless addition and modification of tools within our toolset. 

We optimize the pipeline for performance, latency, and resource usage. The dynamically changing toolset and vastly different user queries make this task challenging. We analyse the performance of different LLMs and prompting strategies, and propose novel methods for handling LLM hallucinations. We also propose a new synthetic data generation methodology which we used to generate novel queries, enabling us to better understand the user's needs.

## Problem Statement
A Language model L has a set of tools T, and a user query Q is given. To answer query Q, we need to use existing tools. You need to output the subset of tools to be used to answer the query, the arguments that these tools should be called with, and how to compose the tools to answer the query. The user queries are conversational.

The set of tools T is dynamic, and new tools can be added, and existing ones could be modified or removed and the agent needs to be able to handle it gracefully.


## Our Approach
![Screenshot 2024-06-08 225742](https://github.com/himanshu-skid19/Inter-IIT-12-Devrev-AI-Agent-007/assets/118837763/637b0c8b-041d-4500-8842-dae5314983ec)

## Pipeline Overview
Our final pipeline includes the following parts:

**Retrieval-ICL** - Retrieval of semantically similar query-answer pairs to serve as few-shot examples for the LLM.

**Chain-of-Thought Prompting** - COT prompting was used to enhance the reasoning capabilities of the LLM.

**Hallucination Check** - We detect all forseeable hallucinations that may occur.

**Corrective Reprompting** - If hallucinations are detected, we ensure they are removed reprompting the LLM.

**Memory** - To effectively manage the conversational aspects of the query.

### Installation and Setup

1. **Install Dependencies:**
   Install the required libraries using:
```python
pip install -r requirements.txt
```


2. **Download Seed Dataset:**
Download from this link: [here](https://drive.google.com/file/d/19aAuy_SHqclSuHqtC8rR6Thgne6QgM7R/view?usp=sharing)


3. **Configure File Paths:**
- **app.py:**
  Modify `retrieval_loader` with your CSV file path:
  ```python
  retrieval_loader = CSVLoader(file_path=r"Your Path here", source_column='QUERY')
  ```
![image](https://github.com/himanshu-skid19/Inter-IIT-12-Devrev-AI-Agent-007/assets/114365148/db799b02-8853-4084-b1df-765700713198)

- **retrieval.py:**
  Modify `loader` with your CSV file path:
  ```python
  loader = CSVLoader(file_path=r"Your Path here")
  ```

4. **API Keys Setup:**
Add your API keys:
- Hugging Face API Key:
  ```python
  os.environ['HUGGINGFACEHUB_API_TOKEN'] = "Your Hugging Face API Key here"
  ```
- OpenAI API Key:
  ```python
  os.environ['OPENAI_API_KEY'] = "Your OpenAI Key here"
  ```
Get the Hugging Face API Keys from [here](https://huggingface.co/settings/tokens).

5. **Run the Application:**
Execute the following command to run the app:
```python
streamlit run app.py
```

### Using the Application

1. **Initial Setup:**
Upon launching, you'll land on the Chatbot page.

2. **Navigate to Tools Management Page:**
Click the radio button in the sidebar to access the Tools Management Page.

3. **Tool Management:**
- **Reset API Toolset:** Click on "Reset API toolset" on the Tools Management Page.
- **Add New Tools:** Use the "Add New Tool" form to add tools to the API list. Multiple tools can be added.
- **Update Tool Details:** To update a tool's name or description, select it and make changes as needed.
- **Delete Tool:** Select a tool and click "Delete tool" to remove it.

4. **Argument Management:**
- **Add New Arguments:** Fill in the details for new arguments in the provided form.
- **Update/Delete Arguments:** Select an argument to update or delete it.
- **Bulk Delete:** Choose multiple arguments to delete them at once.

5. **Finalize:**
Complete the necessary actions to fully utilize the interface.

## Contributors
- [Parth-Agarwal216](https://github.com/Parth-Agarwal216)
- [himanshu-skid19](https://github.com/himanshu-skid19)
- [SpyzzVVarun](https://github.com/SpyzzVVarun)
- [prabhanjan-jadhav](https://github.com/prabhanjan-jadhav)
- [grgkaran03](https://github.com/grgkaran03)
- [arush414](https://github.com/arush414)
- [aryansingh0909](https://github.com/aryansingh0909)
- [Jahnavikkk](https://github.com/Jahnavikkk)
- [JAYESH1304](https://github.com/JAYESH1304)
---
