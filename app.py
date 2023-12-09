from imports import *
from pipelines import *
from update_api_toolset import *
from prompts import *
from prompt_templates import * 
from retrieval import *
from all_apis import *
warnings.filterwarnings('ignore')

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Chatbot", "Tool Management"])

if page == "Chatbot":
    # Chatbot UI Code
    st.title("Simple chat")

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        
        print("okay")
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        print(f"User query: {prompt}")
        query = prompt
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            json_answer = pipeline(query, API_LIST, available_arguments, available_tools, allowed_args_dict, vector_db)
            full_response = json_answer
            # for response in openai.ChatCompletion.create(
            #     model=st.session_state["openai_model"],
            #     messages=[
            #         {"role": m["role"], "content": m["content"]}
            #         for m in st.session_state.messages
            #     ],
            #     stream=True,
            # ):
            #     full_response += response.choices[0].delta.get("content", "")
            #     message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

elif page == "Tool Management":
    print("TOOLS")
    # Tool Management Code
    st.title("Tool Management")

    st.subheader("Add, Delete, or Update Tools")
    operation = st.radio("Select Operation", ["Add", "Delete", "Update"])
    tool_json = st.text_area("Enter Tool JSON", height=300)

    if st.button(f"{operation} Tool"):
        if tool_json:
            try:
                tool_data = json.loads(tool_json)
                API_LIST = manage_tools(operation, tool_data, API_LIST)
                if operation.lower()=="update":
                    st.success(f"Tool successfully {operation}d.")
                else:
                    st.success(f"Tool successfully {operation}ed.")
                st.write(API_LIST)
            except json.JSONDecodeError:
                st.error("Invalid JSON.")
        else:
            st.error("Please enter tool JSON.")
