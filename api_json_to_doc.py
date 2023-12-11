from all_apis import API_LIST

# Function to convert JSON to documentation format
def convert_json_to_doc(API_LIST):
    documentation = ""
    for idx, api in enumerate(API_LIST):
        documentation += f"#### {idx+1}. {api['name']}\n"
        documentation += f"- *API Description:* {api['description']}\n"
        if api["arguments"]:
            documentation += "- **Arguments:**\n"
            for arg in api["arguments"]:
                try:
                    documentation += f"  - {arg['argument_name']}:\n"
                except:
                    pass
                try:
                    documentation += f"     - Argument Description: {arg['argument_description']}\n"
                except:
                    pass
                try:
                    documentation += f"     - Argument Type: {arg['argument_type']}\n"
                except:
                    pass
    return documentation