# Devrev---AI-Agent-007
## Team 15

Devrev---AI-Agent-007 is a streamlined tool for deploying AI applications. Follow these steps to get started:

### Installation and Setup

1. **Install Dependencies:**
   Install the required libraries using:
```python
pip install -r requirements.txt`
```


2. **Download Seed Dataset:**
Use this command to download the Seed Dataset to your local directory:
```python
gdown 19aAuy_SHqclSuHqtC8rR6Thgne6QgM7R`
```


3. **Configure File Paths:**
- **app.py:**
  Modify `retrieval_loader` with your CSV file path:
  ```python
  retrieval_loader = CSVLoader(file_path=r"Your Path here", source_column='QUERY')
  ```
  ![image](https://github.com/himanshu-skid19/Devrev-AI-Agent-007/assets/94075433/ba14afd2-7b15-49de-adff-86cb385527f7)
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
![image](https://github.com/himanshu-skid19/Devrev-AI-Agent-007/assets/95518516/279be45c-d5a2-4a9e-912e-14aca18c3988)

- **Update Tool Details:** To update a tool's name or description, select it and make changes as needed.
<img width="890" alt="image" src="https://github.com/himanshu-skid19/Devrev-AI-Agent-007/assets/95518516/65a59138-dc65-4456-9237-ca7e5187e88a">
- **Delete Tool:** Select a tool and click "Delete tool" to remove it.
<img width="906" alt="image" src="https://github.com/himanshu-skid19/Devrev-AI-Agent-007/assets/95518516/8b842fe4-82af-4913-839d-54dfa6897726">

4. **Argument Management:**
- **Add New Arguments:** Fill in the details for new arguments in the provided form.
- **Update/Delete Arguments:** Select an argument to update or delete it.
- **Bulk Delete:** Choose multiple arguments to delete them at once.

5. **Finalize:**
Complete the necessary actions to fully utilize the interface.

---

This README provides a comprehensive guide to set up and use the Devrev---AI-Agent-007 application.
