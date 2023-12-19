import ast
import re
from collections import OrderedDict

available_tools = [
    "works_list",
    "summarize_objects",
    "prioritize_objects",
    "add_work_items_to_sprint",
    "get_sprint_id",
    "get_similar_work_items",
    "search_object_by_name",
    "create_actionable_tasks_from_text",
    "who_am_i",
    "is_empty",
    "count",
    "works-create",
    "works-delete",
    "works-update",
    "rev-orgs-create",
    "rev-orgs-delete",
    "rev-orgs-update",
    "get_works_id",
    "get_current_date"
]
available_arguments = [
    "works_list/applies_to_part",
    "works_list/created_by",
    "works_list/issue.priority",
    "works_list/issue.rev_orgs",
    "works_list/limit",
    "works_list/owned_by",
    "works_list/stage.name",
    "works_list/ticket.needs_response",
    "works_list/ticket.rev_org",
    "works_list/ticket.severity",
    "works_list/ticket.source_channel",
    "works_list/type",
    "works_list/date_of_creation",
    "works_list/last_modified",
    "works_list/target_close_date",
    "works_list/sprint",
    "summarize_objects/objects",
    "prioritize_objects/objects",
    "add_work_items_to_sprint/work_ids",
    "add_work_items_to_sprint/sprint_id",
    "get_sprint_id/",
    "get_similar_work_items/work_id",
    "search_object_by_name/query",
    "create_actionable_tasks_from_text/text",
    "who_am_i/",
    "is_empty/list_to_check",
    "count/objects",
    "works-create/applies_to_part",
    "works-create/created_by",
    "works-create/issue.priority",
    "works-create/developed_with",
    "works-create/owned_by",
    "works-create/stage.name",
    "works-create/sprint",
    "works-create/type",
    "works-create/target_close_date",
    "works-create/title",
    "works-delete/id",
    "works-update/id",
    "works-update/applies_to_part",
    "works-update/created_by",
    "works-update/owned_by",
    "works-update/stage.name",
    "works-update/type",
    "works-update/target_close_date",
    "works-update/title",
    "works-update/priority",
    "rev-orgs-create/description",
    "rev-orgs-create/display_name",
    "rev-orgs-create/environment",
    "rev-orgs-delete/id",
    "rev-orgs-update/description",
    "rev-orgs-update/display_name",
    "rev-orgs-update/environment",
    "rev-orgs-update/id",
    "get_works_id/objects",
    "get_current_date/"
]

arg_allowed_values_dict = {'works-update/priority': ['p0', 'p1', 'p2', 'p3'],
 'works-update/type': ['issue', 'task', 'ticket'],
 'works_list/issue.priority': ['p0', 'p1', 'p2', 'p3'],
 'works_list/ticket.needs_response': ['true', 'false'],
 'works_list/ticket.severity': ['blocker', 'low', 'medium', 'high'],
 'works_list/type': ['issue', 'task', 'ticket'],
 'works-create/issue.priority': ['p0', 'p1', 'p2', 'p3'],
 'works-create/type': ['issue', 'task', 'ticket'],
 'works-create/title': ['issue', 'ticket']}

args_in_list_dict = {
 'works_list/applies_to_part': 1,
 'works_list/created_by': 1,
 'works_list/issue.priority': 1,
 'works_list/issue.rev_orgs': 1,
 'works_list/limit': 0,
 'works_list/owned_by': 1,
 'works_list/stage.name': 1,
 'works_list/ticket.needs_response': 0,
 'works_list/ticket.rev_org': 1,
 'works_list/ticket.severity': 1,
 'works_list/ticket.source_channel': 1,
 'works_list/type': 1,
 'works_list/date_of_creation': 0,
 'works_list/last_modified': 0,
 'works_list/target_close_date': 0,
 'works_list/sprint': 1,
 'summarize_objects/objects': 1,
 'prioritize_objects/objects': 1,
 'add_work_items_to_sprint/work_ids': 1,
 'add_work_items_to_sprint/sprint_id': 0,
 'get_similar_work_items/work_id': 0,
 'search_object_by_name/query': 0,
 'create_actionable_tasks_from_text/text': 0,
 'is_empty/list_to_check': 0,
 'count/objects': 1,
 'works-create/applies_to_part': 1,
 'works-create/created_by': 1,
 'works-create/issue.priority': 1,
 'works-create/developed_with': 1,
 'works-create/owned_by': 1,
 'works-create/stage.name': 1,
 'works-create/sprint': 1,
 'works-create/type': 1,
 'works-create/target_close_date': 0,
 'works-create/title': 0,
 'works-delete/id': 1,
 'works-update/id': 1,
 'works-update/applies_to_part': 1,
 'works-update/created_by': 1,
 'works-update/owned_by': 1,
 'works-update/stage.name': 1,
 'works-update/type': 1,
 'works-update/target_close_date': 0,
 'works-update/title': 0,
 'works-update/priority': 1,
 'rev-orgs-create/description': 0,
 'rev-orgs-create/display_name': 0,
 'rev-orgs-create/environment': 0,
 'rev-orgs-delete/id': 0,
 'rev-orgs-update/description': 0,
 'rev-orgs-update/display_name': 0,
 'rev-orgs-update/environment': 0,
 'rev-orgs-update/id': 0,
 'get_works_id/objects': 1,
 'get_current_date/': 0
}


def find_hallucinations(json_response, arg_allowed_values_dict, available_tools, available_arguments, args_in_list_dict):
    # check errors in names of tools and arguments
    for i, item in enumerate(json_response):
        print(item)
        if 'tool_name' not in item:
            if type(item) is dict:
                first_key = list(item.keys())[0]
                first_value = item.pop(first_key)
                # Create a new dictionary with 'tool_name' and the rest of the key-value pairs
                new_item = {'tool_name': first_value, **item}
                json_response[i] = new_item
        else:
            item = 'tool_name'

    tool_names = [item['tool_name'] for item in json_response]
    print(f"tool_names:{tool_names}")
    print(f"available_tools:{available_tools}")
    print(f"available_arguments:{available_arguments}")
    valid_tools = [tool_name for tool_name in tool_names if tool_name in available_tools]
    print(f"valid_tools:{valid_tools}")
    hallucinated_tools = [tool_name for tool_name in tool_names if tool_name not in available_tools]
    print(f"hallucinated_tools:{hallucinated_tools}")
    argument_names = []

    for item in json_response:
        for key in item:
            if item[key] in valid_tools:
                # try:
                arguments = item.get("arguments", [])
                for argument in arguments:
                    argument_name = argument.get("argument_name")
                    if argument_name:
                        argument_names.append(item["tool_name"]+"/"+argument_name)
                # except AttributeError:
                    # pass
    # valid_args = [arg_name for arg_name in argument_names if arg_name in merged_arguments]
    hallucinated_args = [arg_name for arg_name in argument_names if arg_name not in available_arguments]
    # check the validity of argument values using allowed_arg_values_dict
    json_args_dict = {}
    for item in json_response:
        for key in item:
            if item[key] in available_tools:
                # try:
                arguments = item.get("arguments", [])
                for argument in arguments:
                    argument_name = argument.get("argument_name")
                    if argument_name:
                        json_args_dict[item["tool_name"]+"/"+argument_name] = argument["argument_value"]
                        concat_arg = item["tool_name"] + "/" + argument_name
                        argument_names.append(concat_arg)
                        # try:
                        if args_in_list_dict[concat_arg] == 1: ## fixes the arguments that are supposed to be in a list format but are not
                            arg_val = argument.get("argument_value")
                            if type(arg_val) is not list:
                                l = []
                                l.append(arg_val)
                                argument["argument_value"] = l
                #         except KeyError:
                #             pass
                # except AttributeError:
                #     pass

    hallucinated_args_values_prev = []
    for idx, item in enumerate(json_response):
        for key in item:
            if item[key] in available_tools:
                # try:
                arguments = item.get("arguments", [])
                for argument in arguments:
                    argument_name = argument.get("argument_name")

                    if argument_name:
                        json_args_dict[item["tool_name"]+"/"+argument_name] = argument["argument_value"]
                        # print("argument value ", argument['argument_value'])
                        # try:
                        print("argument value", argument['argument_value'])
                        arg_list = ast.literal_eval(argument['argument_value'])
                        for arg in arg_list:
                                # print("arument 2, ", arg)
                            if ("$$PREV" in arg and int(arg.split("[")[1].split("]")[0])):
                                hallucinated_args_values_prev.append((item["tool_name"] + "/" + argument_name, arg))
                #         except:
                #             pass
                # except AttributeError:
                #     pass

    hallucinated_args_values = []
    for arg_name, arg_value in json_args_dict.items():
        if arg_name in arg_allowed_values_dict:
            if type(arg_value) is not list:
                if arg_value not in arg_allowed_values_dict[arg_name]:
                    hallucinated_args_values.append((arg_name, arg_value))
            else:
                for i in arg_value:
                    if i not in arg_allowed_values_dict[arg_name]:
                        hallucinated_args_values.append((arg_name, i))
    return hallucinated_args, hallucinated_tools, hallucinated_args_values, hallucinated_args_values_prev

def correction(hallucinated_args, hallucinated_args_values, hallucinated_tools, hallucinated_args_values_prev, json_response):
  Correction_prompt = ''
  Correction_prompt += f'These are the following errors in your previous json response \n {json_response} \n'
  for i in hallucinated_args:
    Correction_prompt += f"The argument {i} is used but is not present in the provided API list. \n"
  for i in hallucinated_tools:
    Correction_prompt += f"The tool {i} is used but is not present in the provided API list. \n"
  for i, j in hallucinated_args_values:
    Correction_prompt += f"Argument_value '{j}' for argument '{i}' is not valid according to the specified API list. \n"
  for i, j in hallucinated_args_values_prev:
    Correction_prompt += f"Argument_value '{j}' for argument '{i}' is not valid since it refers to an item in the API list that does not come before it.\n"
  Correction_prompt += "You have to give the corrected solution to the product manager's query by modifying the provided JSON. You have to remove hallucinations and only output the corrected JSON. \n"
  return Correction_prompt

def correction_if_wrong_schema(exception, json_response):
    Correction_prompt = 'The json you extracted in your response does not follow the appropriate json schema' + '\n'
    Correction_prompt += f'Upon extracting your json response : \n {json_response} \n'
    Correction_prompt += f'The following error is encountered : {exception}' + '\n'
    Correction_prompt += "You have to give the corrected solution to the product manager's query by modifying the provided JSON. You have to remove the error and only output the corrected JSON."
    return Correction_prompt

def placeholder_check(json_response):
    argument_names = []
    if type(json_response) is dict:
        l = []
        l.append(json_response)
        json_response = l
    for item in json_response:
        # try:
        arguments = item.get("arguments", [])
        for argument in arguments:
            # try:
                argument_name = argument.get("argument_name", [])
                argument_value = argument["argument_value"]
                x = re.search("<.*>", str(argument_value))
                if x:
                    return 1
        #         except KeyError:
        #             return 1
        # except AttributeError:
        #     return 0
    return 0


def unsolvable_check(json_response):
    for item in json_response:
        for key in item:
            if type(item[key]) is list:
                return 0
            arg = item[key]
            x = re.search(".*cannot.*", arg)
            if x:
                return 1
    return 0

def complexity(output):
    num_tools = 0
    num_args = 0
    tool_wt = 2
    args_wt = 0.5
    for tool in output:
        num_tools += 1
        arguments = tool.get("arguments", [])
        for argument in arguments:
            num_args += 1
    return num_args*args_wt + num_tools*tool_wt

def structure_check(json_response):
    if type(json_response) is dict:
        l = []
        l.append(json_response)
        json_response = l
    for i, item in enumerate(json_response):        #fixing tool_name issue
        if 'tool_name' not in item:
            if type(item) is dict:
                first_key = list(item.keys())[0]
                first_value = item.pop(first_key)
                # Create a new dictionary with 'tool_name' and the rest of the key-value pairs
                new_item = {'tool_name': first_value, **item}
                json_response[i] = new_item
        else:
            item = 'tool_name'


    restructured_json = []
    for item in json_response:
        d = {}
        d['tool_name'] = item['tool_name']
        x=[]
        try:
            for args in item['arguments']:
                d_ = {}
                d_['argument_name'] = args['argument_name']
                d_['argument_value'] = args['argument_value']
                x.append(d_)
            d['arguments'] = x
            restructured_json.append(d)
        except (KeyError, TypeError) as e:
            if 'arguments' in item:
                if type(item['arguments']) is not list:
                    x = []
                    x.append(item['arguments'])
                    item['arguments'] = x
                # print(item['arguments'])]

                for args in item['arguments']:
                    # print(args)
                    x_ = []
                    n = {}
                    keys = list(args.keys())
                    # print(keys)
                    for j in keys:
                        d_ = {}
                        d_['argument_name'] = j
                        d_['argument_value'] = item['arguments'][0][j]
                        # print(d_)
                        x_.append(d_)
                    n['tool_name'] = item['tool_name']
                    n['arguments'] = x_
                    restructured_json.append(n)
                else:
                    pass

    print(restructured_json)
    return restructured_json
