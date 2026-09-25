# AI Chatbot (Phase 2: Persistent Memory)

A console-based chatbot built in Python. This is an evolving project — starting as a simple rule-based bot, now with persistent per-user memory, and planned upgrades toward smarter pattern matching and eventually real AI API integration.

## Current features (Phase 1 + 2)

- Keyword-based responses with variation (multiple possible replies per keyword, chosen randomly so it doesn't feel robotic)
- Detects the user's name from natural input (e.g. "my name is Obafemi")
- Personalizes responses once it knows your name
- **Persistent, per-user memory** — enter a username at startup, and your name is remembered across separate runs of the program, saved to your own JSON file
- Clean exit on "bye"

## How it works

The bot checks user input against a dictionary of keywords mapped to possible responses. If no keyword matches, it falls back to a default "I don't understand" message. Name detection uses simple string splitting to extract the name from a fixed phrase pattern.

For memory, each username maps to its own file (`memory_<username>.json`). On startup, the bot checks if that file already exists — if so, it loads the saved name; if not, it treats the user as new. Whenever a name is set, it's saved immediately to that user's file.

## How to run

```bash
python main.py
```

No external libraries required — built entirely with Python's standard library (`random`, `json`, `os`).

## Example conversation

**First run (new user):**
```
Enter your username: obafemi
Bot: Welcome! I don't think we've met.
You: hello
Bot: Hi there!
You: my name is Obafemi
Bot: Nice to meet you Obafemi!
You: bye
Bot: Goodbye!
```

**Second run (same username):**
```
Enter your username: obafemi
Bot: Welcome back Obafemi!
You: hello
Bot: Hey Obafemi, good to see you again!
You: bye
Bot: Goodbye!
```

## Roadmap

- [x] Phase 1: Rule-based keyword matching + session memory
- [x] Phase 2: Persistent memory (remember users across separate runs, via per-user saved files)
- [ ] Phase 3: Smarter pattern matching with regex, expanded keyword coverage
- [ ] Phase 4: Basic conversation context/state tracking
- [ ] Phase 5: Real AI integration via an LLM API for open-ended responses
- [ ] Phase 6: GUI version (Tkinter)