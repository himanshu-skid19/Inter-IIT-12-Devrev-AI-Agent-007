from imports import *
from pipelines import *
from hal_check import *
from prompts import *
from prompt_templates import * 
from retrieval import *
from all_apis import *
from prompts import *
from update_api_toolset import *
warnings.filterwarnings('ignore')

# retrieval examples
retrieval_loader = CSVLoader(file_path='/content/Seed_Dataset.csv', source_column = 'QUERY')
retrieval_data = retrieval_loader.load()
retrieval_embeddings = HuggingFaceEmbeddings()
retrieval_vector_db = FAISS.from_documents(
    documents=retrieval_data,
    embedding=retrieval_embeddings,
)

arg_allowed_values_dict = {'works-update/priority': ['p0', 'p1', 'p2', 'p3'],
 'works-update/type': ['issue', 'task', 'ticket'],
 'works_list/issue.priority': ['p0', 'p1', 'p2', 'p3'],
 'works_list/ticket.needs_response': ['true', 'false'],
 'works_list/ticket.severity': ['blocker', 'low', 'medium', 'high'],
 'works_list/type': ['issue', 'task', 'ticket'],
 'works-create/issue.priority': ['p0', 'p1', 'p2', 'p3'],
 'works-create/type': ['issue', 'task', 'ticket'],
 'works-create/title': ['issue', 'ticket']}

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to clear the session state variable
def clear_api_list_updated():
    st.session_state.api_list_updated = API_LIST


file_path = 'Updated_API_list.json'

# Page navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Chatbot", "Tool Management"])

if page == "Chatbot":
    # Chatbot UI Code
    st.title("DevRev AI Agent")

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        with open(file_path, 'r') as file:
            api_list = json.load(file)


        tools_ = [tool['name'] for tool in api_list]
        args_ = []
        for tool in api_list:
            tool_name = tool['name']
            arguments = tool['arguments']

            for argument in arguments:
                argument_name = argument['argument_name']
                args_.append(f"{tool_name}/{argument_name}")

        print("okay")

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        print(f"User query: {prompt}")
        query = prompt
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            json_answer = pipeline(query, api_list, args_, tools_, allowed_args_dict, retrieval_vector_db) # allowed args dict ka placeholder modify karna bacha
            full_response = json_answer
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

elif page == "Tool Management":
    print("TOOLS")
    # Tool Management Code
    st.title("API Tool Management")

    # Load or initialize the API list in session state
    if "api_list_updated" not in st.session_state:
        st.session_state.api_list_updated = API_LIST
    
    # Button to trigger the clearing action
    if st.button("Reset API list"):
        clear_api_list_updated()

    # Add a new tool
    st.header("Add a New Tool")
    with st.form("new_tool_form"):
        new_tool_name = st.text_input("Tool Name")
        new_tool_desc = st.text_area("Tool Description")
        submitted = st.form_submit_button("Add Tool")
        if submitted:
            st.session_state.api_list_updated = add_tool(st.session_state.api_list_updated, new_tool_name, new_tool_desc)
            st.success("Tool Added Successfully!")

    # Update or Delete Tools
    st.header("Update or Delete Tools")
    if st.session_state.api_list_updated:
        selected_tool_name = st.selectbox("Select a tool", options=[tool["name"] for tool in st.session_state.api_list_updated])
        selected_tool = next((tool for tool in st.session_state.api_list_updated if tool['name'] == selected_tool_name), None)

        if selected_tool:
            with st.form("update_delete_tool_form"):
                st.write(f"Selected Tool: {selected_tool_name}")
                new_name = st.text_input("New Name", value=selected_tool['name'])
                new_description = st.text_area("New Description", value=selected_tool['description'])
                update_button = st.form_submit_button("Update Tool")
                delete_button = st.form_submit_button("Delete Tool")

                if update_button:
                    st.session_state.api_list_updated = update_tool(st.session_state.api_list_updated, selected_tool_name, new_name, new_description, vector_db)
                    st.success("Tool Updated Successfully!")

                if delete_button:
                    st.session_state.api_list_updated = delete_tool(st.session_state.api_list_updated, selected_tool_name, vector_db)
                    st.success("Tool Deleted Successfully!")


    # Add a New Argument to a Tool
    st.header("Add a New Argument to a Tool")
    if st.session_state.api_list_updated:  # Check if there are tools available
        selected_tool_name = st.selectbox("Select a tool to add an argument", options=[tool["name"] for tool in st.session_state.api_list_updated])
        with st.form("new_argument_form"):
            new_arg_name = st.text_input("Argument Name")
            new_arg_desc = st.text_area("Argument Description")
            new_arg_allowed_values = st.text_area("Argument Allowed Values")
            new_arg_type = st.text_input("Argument Type")
            submitted_arg = st.form_submit_button("Add Argument")
            if submitted_arg:
                st.session_state.api_list_updated = add_argument(st.session_state.api_list_updated, selected_tool_name, new_arg_name, new_arg_desc, new_arg_type, vector_db)
                arg_allowed_values_dict[f"{selected_tool_name}/{new_arg_name}"] = new_arg_allowed_values
                st.success("Argument Added Successfully!")
    else:
        st.write("No tools available. Add a tool first.")


    # Update or Delete Arguments
    st.header("Update or Delete Arguments")
    if selected_tool:
        st.write(f"Selected Tool: {selected_tool_name}")
        selected_arg_name = st.selectbox("Select an argument", options=[arg["argument_name"] for arg in selected_tool["arguments"]])
        selected_arg = next((arg for arg in selected_tool['arguments'] if arg['argument_name'] == selected_arg_name), None)

        if selected_arg:
            with st.form("update_delete_arg_form"):
                new_arg_name = st.text_input("New Argument Name", value=selected_arg['argument_name'])
                new_arg_desc = st.text_area("New Argument Description", value=selected_arg['argument_description'])
                if f"{selected_tool_name}/{selected_arg_name}" in arg_allowed_values_dict:    
                    new_arg_allowed_values = st.text_area("New Argument Allowed Values", value=arg_allowed_values_dict[f"{selected_tool_name}/{selected_arg_name}"])
                else:
                    new_arg_allowed_values = st.text_area("New Argument Allowed Values")
                new_arg_type = st.text_input("New Argument Type", value=selected_arg['argument_type'])
                update_arg_button = st.form_submit_button("Update Argument")
                delete_arg_button = st.form_submit_button("Delete Argument")

                if update_arg_button:
                    st.session_state.api_list_updated = update_argument(st.session_state.api_list_updated, selected_tool_name, selected_arg_name, new_arg_name, new_arg_desc, new_arg_type, vector_db)
                    arg_allowed_values_dict[f"{selected_tool_name}/{new_arg_name}"] = new_arg_allowed_values
                    st.success("Argument Updated Successfully!")

                if delete_arg_button:
                    st.session_state.api_list_updated = delete_argument(st.session_state.api_list_updated, selected_tool_name, selected_arg_name, vector_db)
                    st.success("Argument Deleted Successfully!")

    # Delete Multiple Arguments
    if selected_tool:
        st.header("Delete Multiple Arguments from Tool")
        all_arg_names = [arg["argument_name"] for arg in selected_tool["arguments"]]
        selected_args_to_delete = st.multiselect("Select arguments to delete from the tool", options=all_arg_names)
        if st.button("Delete Selected Arguments"):
            st.session_state.api_list_updated = delete_multiple_arguments(st.session_state.api_list_updated, selected_tool_name, selected_args_to_delete, vector_db)
            st.success("Selected Arguments Deleted Successfully!")
    
    # Display the current API list
    st.header("Current API List")
    st.text(json.dumps(st.session_state.api_list_updated, indent=2))

    with open(file_path, 'w') as file:
        json.dump(st.session_state.api_list_updated, file)

