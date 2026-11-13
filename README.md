# AI Chatbot (Phase 4: Context and Memory)

A console-based chatbot built in Python. It started as a simple rule-based bot and is growing in phases. It now understands many ways of saying the same thing, remembers facts about each user, and can recall what you talked about in earlier sessions. Real AI integration is planned next.

## Current features (Phases 1 to 4)

- Keyword responses with variety (several possible replies per keyword, chosen randomly)
- **Flexible name detection** using regex: "my name is Bob", "call me Bob", "I'm Bob" and "I am Bob" all work
- **Fact extraction** from natural sentences: age ("I'm 19"), location ("I live in Ibadan") and interests ("I like football")
- **Follow-up questions**: after you say what you like, the bot asks a question and treats your next message as the answer
- **Per-user persistent memory**: log in with a username, and your name, facts and recent conversation are saved to your own JSON file
- **Recall commands**: ask "what do you know about me" or "what did we talk about"
- Whole-word keyword matching, so "hi" doesn't trigger inside "this"
- Exits on "bye", "goodbye", "exit" or "quit"
- Safe usernames: special characters are stripped before a filename is created

## How it works

**Pattern matching.** Regular expressions pull the name, age, location and interests out of a sentence instead of requiring one exact phrase. Keywords are matched as whole words using word boundaries.

**Memory.** Each username maps to its own file, `memory_<username>.json`, which stores the user's name, facts and the last 50 exchanges. The file is saved after every message, so nothing is lost if the terminal is closed suddenly. Files from earlier versions that only contain a name still load correctly.

**Short-term state.** The bot keeps a small `pending` marker. When it asks a question, the next message is treated as the answer and stored, instead of being matched against keywords again.

## How to run

```bash
python main.py
```

No external libraries are needed. It uses only Python's standard library (`json`, `os`, `random`, `re`).

## Example conversation

```
Enter your username: bob
Bot: Welcome! I don't think we've met.
You: hi, call me bob
Bot: Nice to meet you Bob!
You: I live in Ibadan and I like football
Bot: Ibadan sounds like a great place! Nice, football! What do you enjoy most about it?
You: the goals
Bot: Got it, I'll remember that about football.
You: what do you know about me
Bot: So far I know that your name is Bob; you live in Ibadan; you like football; about football you said "the goals".
You: bye
Bot: Goodbye, Bob!
```

Next time, the same username is greeted back and reminded of what was said last.

## Privacy note

Memory files contain what users type, so `memory_*.json` is listed in `.gitignore` and is never pushed to GitHub.

## Roadmap

- [x] Phase 1: Rule-based keyword matching and session memory
- [x] Phase 2: Persistent per-user memory using JSON files
- [x] Phase 3: Regex pattern matching and expanded keyword coverage
- [x] Phase 4: Conversation context, stored facts and recall
- [ ] Phase 5: Real AI integration through an LLM API
- [ ] Phase 6: GUI version (Tkinter)