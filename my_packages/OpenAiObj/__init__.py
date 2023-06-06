import openai
import os
import time
import pprint as pp
# from dotenv import load_dotenv
# load_dotenv()


class OpenAiObj:
    def __init__(self, name, data={}):
        # print('Key!')
        self.name = name
        self.data = data
        self.data.update({self.name: []})

        # Set up your OpenAI API credentials
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Define the conversation history
        self.conversation_history = [{
            "response": {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        }, ]

    def generate_image(self, prompt):
        # Create a list of messages from the conversation history
        messages = []
        for message in self.conversation_history:
            # print('message:', message)
            messages.append(message['response'])

        # Add the current prompt as a user message
        messages.append({'role': 'user', 'content': prompt})

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256",
            # response_format="b64_json",
        )

        # print(response)
        # Extract and return the model's reply
        model_reply = response["data"][0]["url"]
        # model_reply = response["data"][0]["b64_json"][:50]
        return model_reply

    def chat_with_gpt(self, prompt):
        # Create a list of messages from the conversation history
        messages = []
        for message in self.conversation_history:
            # print('message:', message)
            if 'content' in message['response'] and 'image' not in message['response']:
                # print('NO IMAGE message:', message)
                messages.append(message['response'])

        # Add the current prompt as a user message
        messages.append({'role': 'user', 'content': prompt})
        pp.pprint('final_message:')
        pp.pprint(messages)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        print(response)
        # Extract and return the model's reply
        model_reply = response.choices[0].message
        return model_reply

    def k_func(self, str_config, v_val):
        bol_config = False
        if str_config == 'True':
            bol_config = True
        elif str_config == 'conversation_history':
            bol_config = False
            self.conversation_history = v_val
            print('self.conversation_history: ')
            pp.pprint(self.conversation_history)
            self.data[self.name] = v_val
        elif str_config == 'generate_image':
            bol_config = False

            self.data[self.name].append(
                {"prompt": v_val, "response": self.generate_image(v_val)})

        return bol_config

    def v_func(self, v_val):
        print('v_func: ', v_val)
        prompt = v_val

        # Get ChatGPT's response
        response = self.chat_with_gpt(prompt)

        self.data[self.name].append({"prompt": prompt, "response": response})
        print("response: ", response)
        for_img_response = self.chat_with_gpt(" " + response['content'] + ""
            "Summarize the following into a prompt description for a text to image process. No words or letters.")
        # print("for_img_response: ", for_img_response['content'])
        img_response = self.generate_image(for_img_response['content'])
        # print("img_response: ", img_response)
        self.data[self.name].append(
            {"prompt": for_img_response['content'], "response": {"image": img_response}})

        return True


if __name__ == "__main__":
    openAiObj = OpenAiObj('openAiObj')
    # Main execution loop
    while True:
        # Get user input
        prompt = input("User: ")

        # End the loop if user enters 'exit'
        if prompt.lower() == 'exit':
            break

        # Get ChatGPT's response
        response = openAiObj.chat_with_gpt(prompt)

        # Print the response
        print("ChatGPT:", response)

        # Add the user's input and model's response to the conversation history
        # openAiObj.conversation_history.append(prompt)
        # openAiObj.conversation_history.append(response)
