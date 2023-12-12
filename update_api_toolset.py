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

def generate_examples(tool_name, api_list, store, num_examples = 2, arg_name = None):
  APIs = API_CHOICE(2, tool_name, api_list)
  if len(list(store.docstore._dict.values()))>=2:
    few_shot_examples = random.sample(list(store.docstore._dict.values()), 2)
    few_shot_examples = [few_shot_examples[0].page_content, few_shot_examples[1].page_content]
  elif len(list(store.docstore._dict.values()))==1:

    few_shot_examples = random.sample(list(store.docstore._dict.values()), 1)
    few_shot_examples = [few_shot_examples[0].page_content]
  else:
    few_shot_examples=[]
    
  examples = []
  if arg_name is not None:
    MODIFIED_ARG = f'Now you must only use {APIs} and {tool_name} to generate a query, its reasoning and the finar answer. You, also must use the argument {arg_name} for the tool {tool_name} to generate the query. Now generate a query and give your output in the form of the following dictionary.'
  else:
    MODIFIED_ARG = f'Now you must only use {APIs} and {tool_name} to generate a query, its reasoning and the finar answer. Now generate a query and give your output in the form of the following dictionary.'
  for i in range(num_examples):
    examples.append(generation_chain.run(API_LIST = api_list, FEW_SHOT = few_shot_examples, MODIFIED_ARG = MODIFIED_ARG))
  return examples

api_weights = {'works_list': 0,  'prioritize_objects' : 0, 'add_work_items_to_sprint' : 0, 'get_sprint_id' : 0, 'get_similar_work_items' : 0, 'search_object_by_name' : 0,
               'create_actionable_tasks_from_text' : 0, 'who_am_i' : 0,  'get_works_id' : 0, }

api_list = list(api_weights.keys())

# Function to add a new tool
def add_tool(api_list, name, description, available_tools, available_arguments, store):
    available_tools.append(name)
    api_list.append({"name": name, "description": description, "arguments": []})
    available_arguments.append(f"{name}/")
    example = generate_examples(name, api_list, store)
    add_to_vector_store(store, example)
    return api_list, available_tools, available_arguments

def delete_tool(api_list, tool_name, available_tools, available_arguments, arg_allowed_values_dict, args_in_list_dict, store):
    delete_tool_examples(store, tool_name)
    available_tools.remove(tool_name)
    available_arguments = [s for s in available_arguments if not s.startswith(tool_name)]
    arg_allowed_values_dict = {key: value for key, value in arg_allowed_values_dict.items() if not key.startswith(tool_name)}
    args_in_list_dict = {key: value for key, value in args_in_list_dict.items() if not key.startswith(tool_name)}
    api_list = [tool for tool in api_list if tool['name'] != tool_name]
    return api_list, available_tools, available_arguments, arg_allowed_values_dict, args_in_list_dict, store

# Function to update a tool
def update_tool(api_list, old_tool_name, new_tool_name, new_description, available_tools, available_arguments, arg_allowed_values_dict, args_in_list_dict, store):
    delete_tool_examples(store, old_tool_name)
    for tool in api_list:
        if tool['name'] == old_tool_name:
            tool['name'] = new_tool_name
            tool['description'] = new_description
            break
    example = generate_examples(new_tool_name, api_list, store, num_examples = 4)
    add_to_vector_store(store, example)
    available_tools.remove(old_tool_name)
    available_tools.append(new_tool_name)
    available_arguments = [s.replace(old_tool_name, new_tool_name, 1) if s.startswith(old_tool_name) else s for s in available_arguments]
    keys_to_replace1 = [key for key in arg_allowed_values_dict if key.startswith(old_tool_name)]
    for key in keys_to_replace1:
      new_key = key.replace(old_tool_name, new_tool_name)
      arg_allowed_values_dict[new_key] = arg_allowed_values_dict[key]
      del arg_allowed_values_dict[key]
    keys_to_replace2 = [key for key in args_in_list_dict if key.startswith(old_tool_name)]
    for key in keys_to_replace2:
      new_key = key.replace(old_tool_name, new_tool_name)
      args_in_list_dict[new_key] = args_in_list_dict[key]
      del args_in_list_dict[key]
    return api_list, available_tools, available_arguments, arg_allowed_values_dict, args_in_list_dict

# Function to add an argument to a tool
def add_argument(api_list, tool_name, arg_name, arg_desc, arg_type, arg_allowed_values, available_arguments, arg_allowed_values_dict, args_in_list_dict, store):
    delete_tool_examples(store, tool_name)
    for tool in api_list:
      if tool['name'] == tool_name:
        tool['arguments'].append({
                "argument_name": arg_name,
                "argument_description": arg_desc,
                "argument_type": arg_type
            })
        break
    if 'array' in arg_type.lower() :
      args_in_list_dict[f'{tool_name}/{arg_name}'] = 1
    else:
      args_in_list_dict[f'{tool_name}/{arg_name}'] = 0
    example = generate_examples(tool_name, api_list, store, num_examples = 4)
    add_to_vector_store(store, example)
    available_arguments.append(f"{tool_name}/{arg_name}")
    if len(arg_allowed_values) is not 0:
      arg_allowed_values_dict[f'{tool_name}/{arg_name}'] = ast.literal_eval(arg_allowed_values)
    return api_list, available_arguments, arg_allowed_values_dict, args_in_list_dict

# Function to delete an argument from a tool
def delete_argument(api_list, tool_name, arg_name, available_arguments, arg_allowed_values_dict, args_in_list_dict, store):
    delete_tool_examples(store, tool_name, arg_name)
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
    if arg_to_delete in args_in_list_dict:
      del args_in_list_dict[arg_to_delete]
    return api_list, available_arguments, arg_allowed_values_dict, args_in_list_dict

# Function to update an argument
def update_argument(api_list, tool_name, old_arg_name, new_arg_name, new_arg_desc, new_arg_type, new_arg_allowed_values, available_arguments, arg_allowed_values_dict, args_in_list_dict, store):
    delete_tool_examples(store, tool_name, old_arg_name)
    for tool in api_list:
        if tool['name'] == tool_name:
            for arg in tool['arguments']:
                if arg['argument_name'] == old_arg_name:
                    arg['argument_name'] = new_arg_name
                    arg['argument_description'] = new_arg_desc
                    arg['argument_type'] = new_arg_type
                    break
            break
    examples = generate_examples(tool_name, api_list, store, arg_name = new_arg_name)
    add_to_vector_store(store, examples)
    available_arguments.remove(f"{tool_name}/{old_arg_name}")
    available_arguments.append(f"{tool_name}/{new_arg_name}")
    if f"{tool_name}/{old_arg_name}" in arg_allowed_values_dict:
      del arg_allowed_values_dict[f"{tool_name}/{old_arg_name}"]
    if f"{tool_name}/{old_arg_name}" in args_in_list_dict:
      del args_in_list_dict[f"{tool_name}/{old_arg_name}"]
    if len(new_arg_allowed_values) is not 0:
      arg_allowed_values_dict[f'{tool_name}/{new_arg_name}'] = ast.literal_eval(new_arg_allowed_values)
    if 'array' in new_arg_type.lower() :
      args_in_list_dict[f'{tool_name}/{new_arg_name}'] = 1
    else:
      args_in_list_dict[f'{tool_name}/{new_arg_name}'] = 0
    return api_list, available_arguments, arg_allowed_values_dict, args_in_list_dict

# Function to delete multiple arguments from a tool
def delete_multiple_arguments(api_list, tool_name, arg_names, available_arguments, arg_allowed_values_dict, args_in_list_dict, store):
  for arg_name in arg_names :
      delete_tool_examples(store, tool_name, arg_name)
      arg_to_delete = f"{tool_name}/{arg_name}"
      available_arguments.remove(arg_to_delete)
      if arg_to_delete in arg_allowed_values_dict:
        del arg_allowed_values_dict[arg_to_delete]
      if arg_to_delete in args_in_list_dict:
        del args_in_list_dict[arg_to_delete]
  for tool in api_list:
      if tool['name'] == tool_name:
          tool['arguments'] = [arg for arg in tool['arguments'] if arg['argument_name'] not in arg_names]
          break
  examples = generate_examples(tool_name, api_list, store)
  add_to_vector_store(store, examples)
  return api_list, available_arguments, arg_allowed_values_dict, args_in_list_dict
