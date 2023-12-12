# Devrev---AI-Agent-007
## Team 15

Follow the steps to run the deployment
1. Install the requirements.txt file using the following command.
`pip install -r requirements.txt`
2. Copy the path of Seed_Dataset.csv and paste it into:
   a. File name:app.py; retrieval_loader = CSVLoader(file_path = r"Your Path here", source_column = 'QUERY') and comment out the file path in line 61.
   b. retrieval.py; loader = CSVLoader(file_path = r"Your Path here")
3. Add your API Keys:
   a. os.environ['HUGGINGFACEHUB_API_TOKEN'] = "Your Hugging Face API Key here".
   b. os.environ['OPENAI_API_KEY'] = "Your OpenAI Key here".
   Get the Hugging Face API Keys from this page: https://huggingface.co/settings/tokens
5. Now To run the app execute the following command.
`streamlit run app.py`


Step 1: You'll initially land on the Chatbot page.

Navigate to Tools Management Page:

Click on the radio button in the sidebar to access the Tools Management Page.
Reset API Toolset:

On the Tools Management Page, locate and click on the "Reset API toolset" button.
Add New Tools:

Utilize the "Add New Tool" form to add new tools to the API list.
You can add multiple tools at once.
Update Tool Name & Description:

If you wish to update any tool name or description:
Choose the tool from the drop-down list "Select a tool."
Fill up the required fields for the tool.
Click on the "Update tool" button.
Delete Tool:

To delete a tool:
Choose the tool from the drop-down list "Select a tool."
Click on the "Delete tool" button.
Add New Arguments to a Tool:

Scroll to the corresponding form for adding new arguments to a tool.
Fill in the argument name, description, allowed values (if present), and the argument type.
Make sure to input allowed values as a list of strings (e.g., ['p0', 'p1', 'p2']).
Update or Delete Arguments:

To update or delete arguments:
Move to the following form, where the selected tool is mentioned below the heading.
Select the argument from the "Select an argument" box.
Add the new argument name, description, allowed values, and type.
Click "Update argument" to update or "Delete argument" to delete.
Delete Multiple Arguments:

If you want to delete multiple arguments from a tool:
Select all the required arguments from the "Select arguments to delete from the tool" drop-down list.
Click the "Delete selected arguments" button to delete the selected arguments from the tool.
Finalize:

Once you've completed the necessary actions, you have successfully used the interface.
