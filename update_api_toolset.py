from imports import *
from retrieval import *
from prompt_templates import *

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
    global FEW_SHOT
    tool_name = tool['name']
    delete_tool_from_allowed_tools(tool_name)
    add_tool_to_allowed_tools(updated_tool)
    delete_tool_examples(store, tool_name)
    for i in range(len(API_LIST)):
        if API_LIST[i]['name'] == tool_name:
            API_LIST[i] = updated_tool
    example = generate_examples(tool_name, FEW_SHOT)
    add_to_vector_store(store, example)
    FEW_SHOT.append(example)


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
        add_tool(tool, store)
        print("add")
    elif operation == 'delete':
        tool_name = tool['name']
        delete_tool(tool_name, store)
        print("delete")
    elif operation == 'update':
        update_tool(tool, updated_tool, store)
        print("update")

api_weights = {'works_list': 0,  'prioritize_objects' : 0, 'add_work_items_to_sprint' : 0, 'get_sprint_id' : 0, 'get_similar_work_items' : 0, 'search_object_by_name' : 0,
               'create_actionable_tasks_from_text' : 0, 'who_am_i' : 0,  'get_works_id' : 0, }

api_list = list(api_weights.keys())


def add_argument(api_list, tool_name, arg_name, arg_desc, arg_type):
    for tool in api_list:
        if tool['name'] == tool_name:
            tool['arguments'].append({
                "argument_name": arg_name,
                "argument_description": arg_desc,
                "argument_type": arg_type
            })
            break
    return api_list

# Function to delete an argument from a tool
def delete_argument(api_list, tool_name, arg_name):
    for tool in api_list:
        if tool['name'] == tool_name:
            tool['arguments'] = [arg for arg in tool['arguments'] if arg['argument_name'] != arg_name]
            break
    return api_list

# Function to update an argument
def update_argument(api_list, tool_name, old_arg_name, new_arg_name, new_arg_desc, new_arg_type):
    for tool in api_list:
        if tool['name'] == tool_name:
            for arg in tool['arguments']:
                if arg['argument_name'] == old_arg_name:
                    arg['argument_name'] = new_arg_name
                    arg['argument_description'] = new_arg_desc
                    arg['argument_type'] = new_arg_type
                    break
            break
    return api_list

# Function to delete multiple tools
def delete_multiple_tools(api_list, names):
    api_list = [tool for tool in api_list if tool['name'] not in names]
    return api_list

# Function to delete multiple arguments from a tool
def delete_multiple_arguments(api_list, tool_name, arg_names):
    for tool in api_list:
        if tool['name'] == tool_name:
            tool['arguments'] = [arg for arg in tool['arguments'] if arg['argument_name'] not in arg_names]
            break
    return api_list