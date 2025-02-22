def use_deepseek_api(type_of_data, data):
    #This function uses the deepseek API that is provided by hack club to do all the actual work. Thanks, hack club!
    url = "https://ai.hackclub.com/chat/completions"
    headers = {"Content-Type": "application/json"}
    
    if type_of_data =="messages_eval":
        data = data + "based on this messaging history, critique the user's messages and suggest improvements. Make sure to stay positive and constructive, but don't be afraid to be honest. Here are some examples of things you could critique: tone, use of insults/cuss words, use of emojis, helpfulness, etc."
    
    elif type_of_data == "messages_eval_level":
        data = data + "based on this messaging history, critique the user's messages and suggest improvements. Make sure to stay positive and constructive, but don't be afraid to be honest. Here are some examples of things you could critique: tone, use of insults/cuss words, use of emojis, helpfulness, etc. Make this level out of 10, 1 being like an internet troll messaging at 12:00 in the night and 10 being J.K Rowling"
    
    elif type_of_data == "improve_message":
        data = data + "Critique this message, but based on past history, explain what the user did better or worse. Also, provide a refined message in it's place."
    data = {"messages":[{"role":"user", "content":data}]}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    json_response = response.json()
