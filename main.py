import json
import os
import random
responses = {
    "hello": ["Hi there!", "Hey!", "Hello! How can I help?"],
    "how are you": ["I'm doing great, thanks!", "I'm just a bot, but I'm good!"],
}
username = input("Enter your username: ")
filename = f"memory_{username}.json"

if os.path.exists(filename):
  with open(filename, 'r') as f:
    data = json.load(f)
    name = data["name"]
    print(f"Bot: Welcome back {name}!")
else:
  username = None
  print("Bot: Welcome! I don`t think we`ve met.")

while True:
  user = input("You: ").lower()
  if "my name is" in user:
    parts = user.split("my name is")
    user_name = parts[1].strip().capitalize()
    print(f"Bot: Nice to meet you {user_name}!")
    with open(filename, 'w') as f:
       json.dump({"name": user_name}, f)
    continue
  elif 'bye' in user:
    print("Bot: Goodbye!")
    break
  for keyword in responses.keys():
      if keyword in user:
          if keyword == 'hello' and user_name is not None:
              print(f"Bot: Hey {user_name}, good to see you again!")
          else:
              print("Bot:", random.choice(responses[keyword]))
          break
  else:
      print("Bot: I don`t understand that yet.")