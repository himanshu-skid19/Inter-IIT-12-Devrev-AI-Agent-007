from imports import *
from hal_check import *
from prompt_templates import *

def pipeline(query, API_LIST, available_arguments, available_tools, allowed_args_dict, vector_db):
  done = False
  max_reprompts = 1
  cntr = 1
  docs = vector_db.max_marginal_relevance_search(query,k=3)
  RAG_examples = f'{docs[0].page_content}' + '\n' + f'{docs[1].page_content}' + '\n' + f'{docs[2].page_content}'
  resp = query_chain.run(QUERY = query , API_LIST = API_LIST, RAG = RAG_examples)
  print(f"1. Pseudo code output- {cntr} ##################")
  print(resp)
  print(type(resp))
  print(len(resp))
  print(f"##################")
  # json_response = []
  # try:
  #   # Extract json via python code
  #   pass
  # except:
  resp_formatted= format_chain.run(QUERY = "")
  print(f"2. JSON string output- {cntr} ##################")
  print(resp_formatted)
  print(type(resp_formatted))
  print(len(resp_formatted))
  print(f"##################")
  print(f"Reprompt Number: {cntr} #################")

  json_response = ast.literal_eval(resp_formatted)
  print(f"3. JSON decoded output- {cntr} ##################")
  print(json_response)
  print(type(json_response))
  print(len(json_response))
  print(f"##################")

  while not done:
    # hall = True
    hallucinated_args, hallucinated_tools, hallucinated_args_values = find_hallucinations(json_response, allowed_args_dict, available_tools, available_arguments, args_in_list_dict)

    print('##############')
    print(f'wrong stuff : {hallucinated_args}, {hallucinated_tools}, {hallucinated_args_values}')
    print('#############')
    if ((len(hallucinated_args) + len(hallucinated_tools) + len(hallucinated_args_values))is 0 ):
      return json_response
    if cntr>max_reprompts:
        done=True
    Correction_prompt = correction(hallucinated_args, hallucinated_args_values, hallucinated_tools, json_response)
    print(f"4. Correction prompt- {cntr} ##################")
    print(Correction_prompt)
    print(type(Correction_prompt))
    print(len(Correction_prompt))
    print(f"##################")

    json_response = reprompt_chain.run(QUERY = query, API_LIST = API_LIST, CORRECTION_PROMPT = Correction_prompt)
    json_response = ast.literal_eval(json_response)
    cntr+=1
    print(f"4. JSON decoded output- {cntr} ##################")
    print(json_response)
    print(type(json_response))
    print(len(json_response))
    print(f"##################")
    if placeholder_check(json_response):
      return []
  return json_response
