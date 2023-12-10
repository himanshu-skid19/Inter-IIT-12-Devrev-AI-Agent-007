def find_hallucinations(json_response, allowed_args_dict, available_tools, available_arguments, args_in_list_dict):
    # check errors in names of tools and arguments
    tool_names = [tool["tool_name"] for tool in json_response]
    valid_tools = [tool_name for tool_name in tool_names if tool_name in available_tools]
    hallucinated_tools = [tool_name for tool_name in tool_names if tool_name not in available_tools]

    argument_names = []
    for item in json_response:
        if item["tool_name"] in valid_tools:
            arguments = item.get("arguments", [])
            for argument in arguments:
                argument_name = argument.get("argument_name")
                if argument_name:
                    argument_names.append(item["tool_name"]+"/"+argument_name)

    # valid_args = [arg_name for arg_name in argument_names if arg_name in merged_arguments]
    hallucinated_args = [arg_name for arg_name in argument_names if arg_name not in available_arguments]

    # check the validity of argument values using allowed_arg_values_dict
    json_args_dict = {}
    for item in json_response:
        if item["tool_name"] in available_tools:
            arguments = item.get("arguments", [])
            for argument in arguments:
                argument_name = argument.get("argument_name")
                concat_arg = item["tool_name"] + "/" + argument_name
                argument_names.append(concat_arg)
                if args_in_list_dict[concat_arg] == 1: ## fixes the arguments that are supposed to be in a list format but are not
                    arg_val = argument.get("argument_value")
                    if type(arg_val) is not list:
                        l = []
                        l.append(arg_val)
                        argument["argument_value"] = l

    hallucinated_args_values = []
    for arg_name, arg_value in json_args_dict.items():
        if arg_name in allowed_args_dict:
            if arg_value not in allowed_args_dict[arg_name]:
                hallucinated_args_values.append(arg_name)
    return hallucinated_args, hallucinated_tools, hallucinated_args_values

def correction(hallucinated_args, hallucinated_args_values, hallucinated_tools, json_response):

  Correction_prompt = ''
  Correction_prompt += f'There are following errors in your previous json response \n {json_response} \n'
  for i in hallucinated_args:
    Correction_prompt += f"The argument {i} is used but is not present in the provided API list. \n"
  for i in hallucinated_tools:
    Correction_prompt += f"The tool {i} is used but is not present in the provided API list. \n"
  for i in hallucinated_args_values:
    Correction_prompt += f"Argument_value '{i}' is not valid according to the specified API list. \n"
  Correction_prompt += "You have to give the corrected solution to the product manager's query by modifying the provided JSON. You have to remove hallucinations and only output the corrected JSON. \n"
  return Correction_prompt


def placeholder_check(json_response):
    argument_names = []
    for item in json_response:
        arguments = item.get("arguments", [])
        print(arguments)
        for argument in arguments:
            argument_name = argument.get("argument_name")
            argument_value = argument["argument_value"]
            x = re.search("<.*>", str(argument_value))
            if x:

                return 1
    return 0
