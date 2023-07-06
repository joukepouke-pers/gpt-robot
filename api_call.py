import openai
import json
import gpt_functions
openai.api_key_path = "openai_api_key"
default_conversation = [
        {
            "role" : "system",
            "content" : 'you are a language model made by openai wich is intergrated into a voice assistant. give short responses. only call functions provided to you.'
            }
        ]
functions = [
{
    "name" : "move",
    "description" : "move yourself forward or backward",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "direction" : {
                    "type" : "integer",
                    "description" : "either forward(1) or backward(0)"
                    },
                "amount" : {
                    "type" : "integer",
                    "description" : "amount of centimeters to move"
                    },
                },
            "required" : ["direction", "amount"]
         }
}
]
def start_conversation(message):
    global conversation
    conversation = default_conversation
    return continue_conversation({ "role" : "user", "content" : message})
    
def continue_conversation(message_json):
    global conversation
    try:
        conversation.pop(1)
    except:
        pass
    conversation.append(message_json)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=conversation,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        available_functions = {
                "move" : gpt_functions.move
                }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        try:
            function_response = fuction_to_call(
                function_args.get("direction"),
                function_args.get("amount")
                )
        except:
            function_response = "Could not execute function call"
        conversation.append(response_message)
        conversation.append(
                {
                "role": "function",
                "name": function_name,
                "content": function_response,
            })
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=conversation,
        )  # get a new response from GPT where it can see the function response
        continue_conversation(second_response)
    return response_message
def userinput(input):
    input = {"role":"user","content":input}
    return continue_conversation(input)

