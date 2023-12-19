from imports import *
from hal_check import *
from prompt_templates import *
from api_json_to_doc import *
from mem_check import *



def dynamic_k(query):
  word_count = len(query.split())
  if word_count <= 7:
    k = 1
  elif word_count <= 15:
    k = 2
  else:
    k = 3
  return k

def pipeline(query, API_LIST, available_tools, available_arguments, arg_allowed_values_dict, args_in_list_dict, vector_db):
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
  for i in range(num_examples):
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
      try:
        resp1 = query_chain.run(QUERY = query , API_LIST = API_LIST, RAG = RAG_examples)
      except:
        return []
      print(f"1. Pseudo code output- {cntr} ##################")
      print(resp1)
      print(type(resp1))
      print(len(resp1))
      print(f"##################")
      
    
    else:
      if(st.session_state.PAST_RESPONSE =="NO PAST RESPONSES"):
        st.session_state.PAST_QUERY = st.session_state.PREV_QUERY
        st.session_state.PAST_RESPONSE = st.session_state.PREV_RESPONSE
      try:
        resp2 = query_chain_memory.run(QUERY = query , API_LIST = API_LIST, RAG = RAG_examples, PAST_QUERY= st.session_state.PAST_QUERY, PAST_RESPONSE = st.session_state.PAST_RESPONSE)
      except:
        return resp1
      print(f"1. Pseudo code output- {cntr} ##################")
      print(resp2)
      print(type(resp2))
      print(len(resp2))
      print(f"##################")
  
  else:  
    try:
      resp3 = query_chain.run(QUERY = query , API_LIST = API_LIST, RAG = RAG_examples)
    except:
      return []
    print(f"1. Pseudo code output- {cntr} ##################")
    print(resp3)
    print(type(resp3))
    print(len(resp3))
    print(f"##################")
  # json_response = []
  # try:
  #   # Extract json via python code
  #   pass
  # except:
  try:
    # print(memory.load_memory_variables({})['chat_history'])
    # chat_history_temp = memory.load_memory_variables({})['chat_history'][1]
    # print(chat_history_temp)
    # memory.load_memory_variables({})['chat_history'] = chat_history_temp
    resp_formatted= format_chain.run(QUERY = "")
  except:
    try:
      return resp3
    except:
      return resp2
  print(f"2. JSON string output- {cntr} ##################")
  print(resp_formatted)
  print(type(resp_formatted))
  print(len(resp_formatted))
  print(f"##################")
  print(f"Reprompt Number: {cntr} #################")

  print(f"Response formatted:{resp_formatted}")
  try:
    json_response = ast.literal_eval(resp_formatted)
  except Exception as e:
    Correction_prompt = correction_if_wrong_schema(e, resp_formatted)
    resp_formatted = reprompt_chain.run(QUERY=query, API_LIST=API_LIST, CORRECTION_PROMPT=Correction_prompt)
    try:
      json_response = ast.literal_eval(resp_formatted)
    except:
      return []
  print(f"3. JSON decoded output- {cntr} ##################")
  print(json_response)
  print(type(json_response))
  print(len(json_response))
  print(f"##################")


  json_response_init = json_response

  try:
    while not done:
      # hall = True
      try:
        hallucinated_args, hallucinated_tools, hallucinated_args_values, hallucinated_args_values_prev = find_hallucinations(json_response, arg_allowed_values_dict, available_tools, available_arguments, args_in_list_dict)
      except:
        return json_response_init
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
      try:
        Correction_prompt = correction(hallucinated_args, hallucinated_args_values, hallucinated_tools, hallucinated_args_values_prev, json_response)
      except:
        return json_response_init
      print(f"4. Correction prompt- {cntr} ##################")
      print(Correction_prompt)
      print(type(Correction_prompt))
      print(len(Correction_prompt))
      print(f"##################")

      json_response = reprompt_chain.run(QUERY = query, API_LIST = API_LIST, CORRECTION_PROMPT = Correction_prompt)
      try:
        json_response = ast.literal_eval(json_response)
      except Exception as e:
        Correction_prompt = correction_if_wrong_schema(e, json_response)
        json_response = reprompt_chain.run(QUERY=query, API_LIST=API_LIST, CORRECTION_PROMPT=Correction_prompt)
        try:
          json_response = ast.literal_eval(json_response)
        except:
          return []
      cntr+=1
      print(f"4. JSON decoded output- {cntr} ##################")
      print(json_response)
      print(type(json_response))
      print(len(json_response))
      print(f"##################")
      # json_response = structure_check(json_response)
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
  except:
    return json_response_init    
  return json_response
