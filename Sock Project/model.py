import requests
from main import user_messages

def use_deepseek_api(type_of_data, data):
    """
    This function uses the Deepseek API provided by Hack Club to analyze and critique messages.
    """
    url = "https://ai.hackclub.com/chat/completions"
    headers = {"Content-Type": "application/json"}

    # Construct the prompt based on the type of data
    if type_of_data == "messages_eval":
        prompt = data + " Based on this messaging history, which is given as a list of user ids with what they said next to it, critique all the messages from one user id, your response will be sent back to the user so stay friendly. Critique the user's messages and suggest improvements. Make sure to stay positive and constructive, but don't be afraid to be honest. Here are some examples of things you could critique: tone, use of insults/cuss words, use of emojis, helpfulness, etc."
    
    elif type_of_data == "messages_eval_level":
        prompt = data + " Based on this messaging history, critique the user's messages and suggest improvements. Make sure to stay positive and constructive, but don't be afraid to be honest. Here are some examples of things you could critique: tone, use of insults/cuss words, use of emojis, helpfulness, etc. Make this level out of 10, 1 being like an internet troll messaging at 12:00 in the night and 10 being J.K Rowling."
    
    elif type_of_data == "improve_message":
        prompt = data + " Critique this message, but based on past history, explain what the user did better or worse. Also, provide a refined message in its place. Make it small, just the the new message and the critique."
    
    else:
        print("Error: Invalid type_of_data.")
        return

    # Construct the payload
    payload = {
        "messages": [{"role": "user", "content": prompt}]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Debugging: Print status code and raw response
    print("Status code:", response.status_code)
    print("Response:", response.text)

    # Check if the request was successful
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
    else:
        print(f"API Error: {response.status_code} - {response.text}")

# Example usage
while true do:
    use_deepseek_api("messages_eval", user_messages)