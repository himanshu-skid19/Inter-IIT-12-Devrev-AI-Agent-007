# Devrev---AI-Agent-007
## Team 15
install the requirements.txt file
`pip install -r requirements.txt`
To run the app execute the following command.
`streamlit run app.py`


Step 1: You'll initially land on the Chatbot page.
![image](https://github.com/himanshu-skid19/Devrev-AI-Agent-007/assets/106437020/b74542d4-12cf-4517-a54b-51438fdc2e4f)

You'll be displayed will the chatbot interface. Insert your OpenAI API key in the textbox present in the sidebar.
Now visit the Tools Management Page by clicking on the radio button in the sidebar.
First click on the Reset API toolset button. Use Add New Tool form to add new tools to the API list. You may add as many as tools required at once. 
Further, if you wish to update any tool name & description, then choose the tool from the drop down list "Select a tool", and fill up the required fields and click Update tool or directly click on the delete tool button to delete the tool.
To add new arguments to a tool, scroll to the corresponding form. In this form you should fill the argument name, argument description, allowed values of the argument if present, make sure to input them as a list of strings only, for example ['p0', 'p1', 'p2']. Also add the argument type. 
Now, if the user wants to update or Delete arguments move to the following form and the selected tool will be mentioned below the heading then select the argument from the select an argument box then add the argument name to the new argument name at the argument description to the new argument description and at the new argument allowed values in the corresponding works also add the new argument type and then update the argument or else directly delete the argument using the delete button. 
If the user wants to delete multiple arguments from tool then select all the required arguments from the Select arguments to delete from the tool drop down list. Now finally press the Delete selected arguments button to delete the selected arguments from the selected tool. 


