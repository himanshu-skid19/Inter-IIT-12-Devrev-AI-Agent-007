from imports import *
from prompts import *

def update_tool(tool, updated_tool):
    global API_LIST
    # global FEW_SHOT
    tool_name = tool['name']
    for i in range(len(API_LIST)):
        if API_LIST[i]['name'] == tool_name:
            API_LIST[i] = updated_tool

    # FEW_SHOT = generate_examples(tool_name, FEW_SHOT)
# update_tool(tool_update_example, tool_updated_example)

def delete_tool(tool_name, apis, store):
    for i in range(len(apis)):
        if apis[i]['name'] == tool_name:
            apis.remove(API_LIST[i])
            delete_tool(store, tool_name)
            break

#   for i in range(len(FEW_SHOT)):
#     if tool_name in FEW_SHOT[i]['ANSWER']:
#       FEW_SHOT.remove(FEW_SHOT[i])

# print(FEW_SHOT)
# delete_tool('who_am_i', API_LIST)
# print(FEW_SHOT)

def add_tool(tool):
    global FEW_SHOT
    API_LIST.append(tool)
    tool_name = tool['name']
    # FEW_SHOT = generate_examples(tool, FEW_SHOT)

def manage_tools(operation, tool_json, api_list):
    # make operation to lower case
    operation = operation.lower()
    if operation == 'add':
        api_list.append(tool_json)
        print("add")
    elif operation == 'delete':
        for i in range(len(api_list)):
            if api_list[i]['name'] == tool_json['name']:
                api_list.pop(i)
                break
        print("delete")
    elif operation == 'update':
        tool_name = tool_json['name']
        for i in range(len(api_list)):
            if api_list[i]['name'] == tool_name:
                api_list[i] = tool_json
        print("update")
    return api_list

api_weights = {'works_list': 0,  'prioritize_objects' : 0, 'add_work_items_to_sprint' : 0, 'get_sprint_id' : 0, 'get_similar_work_items' : 0, 'search_object_by_name' : 0,
               'create_actionable_tasks_from_text' : 0, 'who_am_i' : 0,  'get_works_id' : 0, }

api_list = list(api_weights.keys())

def API_CHOICE(n, tool_name):
    l = []
    apis = api_list.copy()
    if tool_name in apis:
        apis.remove(tool_name)
    for i in range(n):
        choice = random.choice(apis)
        apis.remove(choice)
        l.append(choice)
    return l

def generate_examples(tool_name, FEW_SHOT, API_LIST, APIs, generation_prompt_template):
    APIs = API_CHOICE(2, tool_name)

    generation_prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                generation_prompt_template
            ),
        ]
    )

    llm = ChatOpenAI(temperature = 0.0, model =  "gpt-3.5-turbo-1106")

    query_chain = LLMChain(llm=llm,
                            prompt=generation_prompt,
                            output_key = 'QUERY',
                            verbose=False)

    baseline_chain = SequentialChain(
    chains=[query_chain],
    input_variables = ['API_LIST', 'FEW_SHOT', 'APIs', 'tool_name'],
    output_variables = ['QUERY'],
    verbose=False)

    resp = baseline_chain.run(API_LIST = API_LIST, FEW_SHOT = FEW_SHOT, APIs = APIs, tool_name = tool_name)
    example = json.loads(resp)
    return example