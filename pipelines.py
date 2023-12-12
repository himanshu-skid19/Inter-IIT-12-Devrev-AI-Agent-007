from imports import *
from hal_check import *
from prompt_templates import *
from api_json_to_doc import *
from mem_check import *

ENV_HOST = "https://cloud.langfuse.com"
ENV_SECRET_KEY = "sk-lf-d86b4406-8aa2-49e0-829f-8367aa67c98e"
ENV_PUBLIC_KEY = "pk-lf-0304359e-b115-403e-8eb4-45429fbe037f"

def dynamic_k(query):
  word_count = len(query.split())
  if word_count <= 10:
    k = 1
  elif word_count <= 20:
    k = 2
  else:
    k = 3
  return k

def pipeline(query, API_LIST, available_arguments, available_tools, arg_allowed_values_dict, args_in_list_dict, vector_db):
  handler = CallbackHandler(ENV_PUBLIC_KEY, ENV_SECRET_KEY, ENV_HOST)
  print(f"PreviousQuery: {st.session_state.PREV_QUERY}")
  print(f"PreviousResponse: {st.session_state.PREV_RESPONSE}")
  print(f"PastQuery: {st.session_state.PAST_QUERY}")
  print(f"PastResponse: {st.session_state.PAST_RESPONSE}")
  API_LIST = convert_json_to_doc(API_LIST)
  done = False
  max_reprompts = 1
  cntr = 1
  num_examples = dynamic_k(query)
  docs = vector_db.max_marginal_relevance_search(query, k = num_examples)
  RAG_examples = ''
  for i in range(num_examples)
    RAG_examples += f'{docs[i].page_content}' + '\n'
  classification = False
  if(st.session_state.PREV_QUERY!=""):
    if(st.session_state.PAST_QUERY=="NO PAST QUERIES"):
      mem_resp = mem_chain.run(QUERY = query, PREV_QUERY = st.session_state.PREV_QUERY)
    else:
      mem_resp = mem_chain.run(QUERY = query, PREV_QUERY = st.session_state.PAST_QUERY)

    print(f"0. Memory output- {cntr} ##################")
    print(mem_resp)
    print(f"##################")
    classification = verify_follow_up_query(mem_resp)
    if(classification==False):
      st.session_state.PAST_QUERY = "NO PAST QUERIES"
      st.session_state.PAST_RESPONSE = "NO PAST RESPONSES"
      resp = query_chain.run(QUERY = query , API_LIST = API_LIST, RAG = RAG_examples)
      print(f"1. Pseudo code output- {cntr} ##################")
      print(resp)
      print(type(resp))
      print(len(resp))
      print(f"##################")
      
    
    else:
      if(st.session_state.PAST_RESPONSE =="NO PAST RESPONSES"):
        st.session_state.PAST_QUERY = st.session_state.PREV_QUERY
        st.session_state.PAST_RESPONSE = st.session_state.PREV_RESPONSE
      resp = query_chain_memory.run(QUERY = query , API_LIST = API_LIST, RAG = RAG_examples, PAST_QUERY= st.session_state.PAST_QUERY, PAST_RESPONSE = st.session_state.PAST_RESPONSE)
      print(f"1. Pseudo code output- {cntr} ##################")
      print(resp)
      print(type(resp))
      print(len(resp))
      print(f"##################")
  
  else:  
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

  print(f"Response formatted:{resp_formatted}")
  json_response = ast.literal_eval(resp_formatted)
  print(f"3. JSON decoded output- {cntr} ##################")
  print(json_response)
  print(type(json_response))
  print(len(json_response))
  print(f"##################")

  while not done:
    # hall = True
    hallucinated_args, hallucinated_tools, hallucinated_args_values, hallucinated_args_values_prev = find_hallucinations(json_response, arg_allowed_values_dict, available_tools, available_arguments, args_in_list_dict)

    print('##############')
    print(f'wrong stuff : {hallucinated_args}, {hallucinated_tools}, {hallucinated_args_values}, {hallucinated_args_values_prev}')
    print('#############')
    if ((len(hallucinated_args) + len(hallucinated_tools) + len(hallucinated_args_values)) + len(hallucinated_args_values_prev) is 0 ):
      if(st.session_state.PREV_QUERY ==""):
        st.session_state.PREV_QUERY = query
        st.session_state.PREV_RESPONSE = str(json_response)
      else:
        if(classification==True):
          st.session_state.PAST_QUERY = st.session_state.PAST_QUERY + '.\n' + query
          st.session_state.PAST_RESPONSE = st.session_state.PAST_RESPONSE + '.\n' + str(json_response)
        st.session_state.PREV_QUERY = query
        st.session_state.PREV_RESPONSE = str(json_response)
      return json_response
    if cntr>max_reprompts:
        done=True
    Correction_prompt = correction(hallucinated_args, hallucinated_args_values, hallucinated_tools, hallucinated_args_values_prev, json_response)
    print(f"4. Correction prompt- {cntr} ##################")
    print(Correction_prompt)
    print(type(Correction_prompt))
    print(len(Correction_prompt))
    print(f"##################")

    json_response = reprompt_chain.run(QUERY = query, API_LIST = API_LIST, CORRECTION_PROMPT = Correction_prompt, callbacks=[handler])
    try:
      json_response = ast.literal_eval(json_response)
    except SyntaxError:
      json_response = reprompt_chain.run(QUERY=query, API_LIST=API_LIST, CORRECTION_PROMPT=Correction_prompt,
                                         callbacks=[handler])
      json_response = ast.literal_eval(json_response)
    cntr+=1
    print(f"4. JSON decoded output- {cntr} ##################")
    print(json_response)
    print(type(json_response))
    print(len(json_response))
    print(f"##################")
    json_response = structure_check(json_response)
    if placeholder_check(json_response):
      if(classification==True):
        st.session_state.PAST_QUERY = st.session_state.PAST_QUERY + '.\n' + query
        st.session_state.PAST_RESPONSE = st.session_state.PAST_RESPONSE + '.\n' + '[]'
      st.session_state.PREV_QUERY = query
      st.session_state.PREV_RESPONSE = '[]'
      return []
    
    if unsolvable_check(json_response):
      if(classification==True):
        st.session_state.PAST_QUERY = st.session_state.PAST_QUERY + '.\n' + query
        st.session_state.PAST_RESPONSE = st.session_state.PAST_RESPONSE + '.\n' + '[]'
      st.session_state.PREV_QUERY = query
      st.session_state.PREV_RESPONSE = '[]'
      return []
  
  if(st.session_state.PREV_QUERY ==""):
    st.session_state.PREV_QUERY = query
    st.session_state.PREV_RESPONSE = str(json_response)
  else:
    if(classification==True):
      st.session_state.PAST_QUERY = st.session_state.PAST_QUERY + '.\n' + query
      st.session_state.PAST_RESPONSE = st.session_state.PAST_RESPONSE + '.\n' + str(json_response)
    st.session_state.PREV_QUERY = query
    st.session_state.PREV_RESPONSE = str(json_response)
  return json_response
