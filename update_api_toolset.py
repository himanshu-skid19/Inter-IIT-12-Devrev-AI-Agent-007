from imports import *
from retrieval import *
from prompt_templates import *
from hal_check import *

def API_CHOICE(n, tool_name, api_list):
  l = []
  apis = api_list.copy()
  if tool_name in apis:
    apis.remove(tool_name)
  for i in range(n):
    choice = random.choice(apis)
    apis.remove(choice)
    l.append(choice)
  return l

def generate_examples(tool_name, api_list, store, num_examples = 2):
  APIs = API_CHOICE(2, tool_name, api_list)
  few_shot_examples = random.sample(list(store.docstore._dict.values()), 2)
  few_shot_examples = [few_shot_examples[0].page_content, few_shot_examples[1].page_content]
  examples = []
  for i in range(num_examples):
    examples.append(generation_chain.run(API_LIST = api_list, FEW_SHOT = few_shot_examples, APIS = APIs, TOOL_NAME = tool_name))
  return examples

api_weights = {'works_list': 0,  'prioritize_objects' : 0, 'add_work_items_to_sprint' : 0, 'get_sprint_id' : 0, 'get_similar_work_items' : 0, 'search_object_by_name' : 0,
               'create_actionable_tasks_from_text' : 0, 'who_am_i' : 0,  'get_works_id' : 0, }

api_list = list(api_weights.keys())

# Function to add a new tool
def add_tool(api_list, name, description):
    available_tools.append(name)
    api_list.append({"name": name, "description": description, "arguments": []})
    return api_list

def delete_tool(api_list, tool_name, available_tools, available_arguments, allowed_args_dict, args_in_list_dict, store):
    delete_tool_examples(store, tool_name)
    available_tools.remove(tool_name)
    available_arguments = [s for s in available_arguments if not s.startswith(tool_name)]
    allowed_args_dict = {key: value for key, value in allowed_args_dict.items() if not key.startswith(tool_name)}
    args_in_list_dict = {key: value for key, value in args_in_list_dict.items() if not key.startswith(tool_name)}
    api_list = [tool for tool in api_list if tool['name'] != tool_name]
    return api_list, available_tools, available_arguments, allowed_args_dict, args_in_list_dict, store

# Function to update a tool
def update_tool(api_list, old_tool_name, new_tool_name, new_description, store):
    delete_tool_examples(store, old_tool_name)
    for tool in api_list:
        if tool['name'] == old_tool_name:
            tool['name'] = new_tool_name
            tool['description'] = new_description
            break
    example = generate_examples(new_tool_name, api_list, store)
    add_to_vector_store(store, example)
    available_tools.remove(old_tool_name)
    available_tools.append(new_tool_name)
    return api_list

# Function to add an argument to a tool
def add_argument(api_list, tool_name, arg_name, arg_desc, arg_type, store):
    for tool in api_list:
        if tool['name'] == tool_name:
            tool['arguments'].append({
                "argument_name": arg_name,
                "argument_description": arg_desc,
                "argument_type": arg_type
            })
            break
    example = generate_examples(tool_name, api_list, store)
    add_to_vector_store(store, example)
    available_arguments.append(f"{tool_name}/{arg_name}")
    return api_list

# Function to delete an argument from a tool
def delete_argument(api_list, tool_name, arg_name, available_arguments, arg_allowed_values_dict, args_in_list_dict, store):
    delete_tool_examples(store, arg_name)
    for tool in api_list:
        if tool['name'] == tool_name:
            tool['arguments'] = [arg for arg in tool['arguments'] if arg['argument_name'] != arg_name]
            break
    examples = generate_examples(tool_name, api_list, store)
    add_to_vector_store(store, examples)
    arg_to_delete = f"{tool_name}/{arg_name}"
    available_arguments.remove(arg_to_delete)
    if arg_to_delete in arg_allowed_values_dict:
      del arg_allowed_values_dict[arg_to_delete]
    if arg_to_delete in arg_in_list_dict:
      del arg_in_list_dict[arg_to_delete]
    return api_list, available_arguments, arg_allowed_values_dict, args_in_list_dict

# Function to update an argument
def update_argument(api_list, tool_name, old_arg_name, new_arg_name, new_arg_desc, new_arg_type, store):
    delete_tool_examples(store, old_arg_name)
    for tool in api_list:
        if tool['name'] == tool_name:
            for arg in tool['arguments']:
                if arg['argument_name'] == old_arg_name:
                    arg['argument_name'] = new_arg_name
                    arg['argument_description'] = new_arg_desc
                    arg['argument_type'] = new_arg_type
                    break
            break
    example = generate_examples(tool_name, api_list, store)
    add_to_vector_store(store, example)
    available_arguments.remove(f"{tool_name}/{old_arg_name}")
    available_arguments.append(f"{tool_name}/{new_arg_name}")
    return api_list

# Function to delete multiple arguments from a tool
def delete_multiple_arguments(api_list, tool_name, arg_names, store):
  for arg_name in arg_names :
    delete_tool_examples(store, arg_name)
    available_arguments.remove(f"{tool_name}/{arg_name}")
  for tool in api_list:
      if tool['name'] == tool_name:
          tool['arguments'] = [arg for arg in tool['arguments'] if arg['argument_name'] not in arg_names]
          break
  example = generate_examples(tool_name, api_list, store)
  add_to_vector_store(store, example)
  return api_list
