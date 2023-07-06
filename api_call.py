import openai
import json
import functions
api_key = open("openai_api_key", "r")
start_conversation = [
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
                    "type" : "int",
                    "description" : "1 to move forward, 0 to move backward"
                    },
                "amount" : {
                    "type" : "int",
                    "description" : "amount of centimeters to move"
                    },
                },
            "required" : ["direction", "amount"]
         }
}
]
def start_conversation(message):
    global conversation
    conversation = start_conversation
    conversation.append({ "role" : "user", "content" : message}) 
def continue_conversation(message_json):
    global conversation
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
                "move" : functions.move
                }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
                function_args.get("direction"),
                function_args.get("amount")
                )
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
def userinput(input):
    input = {"role":"user","content":input}
    continue_conversation(input)

