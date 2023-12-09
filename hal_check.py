from imports import *

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

allowed_args_dict = {'works-update/priority': ['p0', 'p1', 'p2', 'p3'],
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
    #         x = re.search("<.*>", str(argument_value))
    #         if x:
    #             return 1
    # return 0

json_response = [{'name': 'prioritize_objects', 'description': 'Returns a list of objects sorted by priority. The logic of what constitutes priority for a given object is an internal implementation detail.', 'arguments': [{'argument_name': 'objects', 'argument_description': 'A list of objects to be prioritized', 'argument_type': 'array of objects'}]},
                 {'name': 'add_work_ite ms_to_sprint', 'description': 'Adds the given work items to the sprint', 'arguments': [{'argument_name': 'work_ids', 'argument_description': 'A list of work item IDs to be added to the sprint.', 'argument_type': 'array of strings'}, {'argument_name': 'sprint_id', 'argument_description': 'The ID of the sprint to which the work items should be added', 'argument_type': 'string'}]}]


placeholder_check(json_response)