from imports import *

# Function to verify follow-up queries

def verify_follow_up_query(mem_response):

    classification_index = mem_response.find("Classification:")
    extracted_part = mem_response[classification_index:].split("\n", 1)[0]
    extracted_text = extracted_part.replace("Classification:", "").strip()
    if(extracted_text=="Follow-up"):
       return True
    return False
