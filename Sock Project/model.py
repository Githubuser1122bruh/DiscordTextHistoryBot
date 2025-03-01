import requests
def use_deepseek_api(type_of_data, data, user_messages):
    """
    This function uses the Deepseek API provided by Hack Club to analyze and critique messages.
    """
    url = "https://ai.hackclub.com/chat/completions"
    headers = {"Content-Type": "application/json"}

    # Construct the prompt based on the type of data
    if type_of_data == "messages_eval":
        prompt = data +  "This is the history:" + user_messages.join("\n") + " Based on this messaging history, critique the user's messages and suggest improvements. Make sure to stay positive and constructive, but don't be afraid to be honest. Here are some examples of things you could critique: tone, use of insults/cuss words, use of emojis, helpfulness, etc."
    
    elif type_of_data == "messages_eval_level":
        prompt = data + "This is the history:" + "\n".join(user_messages) + "Based on this messaging history, critique the user's messages and suggest improvements. Make sure to stay positive and constructive, but don't be afraid to be honest. Here are some examples of things you could critique: tone, use of insults/cuss words, use of emojis, helpfulness, etc. Make this level out of 10, 1 being like an internet troll messaging at 12:00 in the night and 10 being J.K Rowling."
    
    elif type_of_data == "improve_message":
        prompt = data + "This is the history:" + "\n".join(user_messages) + "this is the message:" + data + "Critique this message, but based on past history, explain what the user did better or worse. Also, provide a refined message in its place. Make it small, just the the new message and the critique."
    
    else:
        print("Error: Invalid type_of_data.")
        return

    payload = {
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)

    print("Status code:", response.status_code)
    print("Response:", response.text)
    if response.status_code == 200:
        try:
            # Parse the JSON response
            response_json = response.json()

            # Extract the content from the response
            content = response_json['choices'][0]['message']['content']

            # Print only the content of the message
            print("Content:", content)
        except KeyError:
            print("Error: The JSON structure is not as expected.")
        except requests.exceptions.JSONDecodeError:
            print("Error: The response is not valid JSON.")
    elif response.status_code == 400:
        print("Deepseek API is dead :(")
    else:
        print(f"API Error: {response.status_code} - {response.text}")
