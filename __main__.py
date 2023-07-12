import api_call
print(api_call.start_conversation(input("you: "))["content"])

while True:
    print(api_call.userinput(input("you: "))["content"])

