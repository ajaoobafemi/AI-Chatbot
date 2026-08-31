import random
responses = {
    "hello": ["Hi there!", "Hey!", "Hello! How can I help?"],
    "how are you": ["I'm doing great, thanks!", "I'm just a bot, but I'm good!"],
}
user_name = None
while True:
  user = input("You: ").lower()
  if "my name is" in user:
    parts = user.split("my name is")
    user_name = parts[1].strip().capitalize()
    print(f"Bot: Nice to meet you {user_name}!")
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