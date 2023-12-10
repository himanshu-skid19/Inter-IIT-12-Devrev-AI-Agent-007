from imports import *

# Function to add a new tool
def add_tool(api_list, name, description):
    api_list.append({"name": name, "description": description, "arguments": []})
    return api_list

# Function to delete a tool
def delete_tool(api_list, tool_name):
    return [tool for tool in api_list if tool['name'] != tool_name]

# Function to update a tool
def update_tool(api_list, old_tool_name, new_tool_name, new_description):
    for tool in api_list:
        if tool['name'] == old_tool_name:
            tool['name'] = new_tool_name
            tool['description'] = new_description
            break
    return api_list

# Function to add an argument to a tool
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