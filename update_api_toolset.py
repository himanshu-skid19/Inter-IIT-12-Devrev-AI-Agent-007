from imports import *
from prompts import *



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

def generate_examples(tool_name, FEW_SHOT):
  global API_LIST
  APIs = API_CHOICE(2, tool_name)
  example = generation_chain.run(API_LIST = API_LIST, FEW_SHOT = FEW_SHOT, APIS = APIs, TOOL_NAME = tool_name)
  return example


def delete_tool_from_allowed_tools(tool_name):
  global available_tools
  global available_arguments
  global allowed_args_dict
  available_tools.remove(tool_name)
  available_arguments = [s for s in available_arguments if not s.startswith(tool_name)]
  allowed_args_dict = {key: value for key, value in allowed_args_dict.items() if not key.startswith(tool_name)}

def add_tool_to_allowed_tools(tool):
  global available_tools
  global available_arguments
  global allowed_args_dict
  tool_name = tool['name']
  available_tools.append(tool_name)
  for i in tool["arguments"]:
    available_arguments.append(f'{tool_name}/{i["argument_name"]}')


def update_tool(tool, updated_tool, store):
    global API_LIST
    # global FEW_SHOT
    tool_name = tool['name']
    for i in range(len(API_LIST)):
        if API_LIST[i]['name'] == tool_name:
            API_LIST[i] = updated_tool

    example = generate_examples(tool_name, FEW_SHOT)
    add_to_vector_store(store, example)
    FEW_SHOT.append(example)


    # FEW_SHOT = generate_examples(tool_name, FEW_SHOT)
# update_tool(tool_update_example, tool_updated_example)


def delete_tool(tool_name, store):
  global API_LIST
  global FEW_SHOT
  delete_tool_examples(store, tool_name)
  delete_tool_from_allowed_tools(tool_name)
  for i in range(len(API_LIST)):
    if API_LIST[i]['name'] == tool_name:
      API_LIST.remove(API_LIST[i])
      break
  to_remove = []
  for i in range(len(FEW_SHOT)):
    if tool_name in FEW_SHOT[i]['ANSWER']:
      to_remove = FEW_SHOT[i]
  FEW_SHOT = [item for item in to_remove if item not in FEW_SHOT]

def add_tool(tool, store):
  global FEW_SHOT
  API_LIST.append(tool)
  add_tool_to_allowed_tools(tool)
  example = generate_examples(tool, FEW_SHOT)
  add_to_vector_store(store, example)
  FEW_SHOT.append(example)
def manage_tools(operation, tool, store, updated_tool = None):
    memory.clear()
    if operation == 'add':
        api_list.append(tool_json)
        print("add")
    elif operation == 'delete':
        tool_name = tool['name']
        delete_tool(tool_name, store)
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