# AI Chatbot (Phase 1: Rule-Based)

A console-based chatbot built in Python. This is Phase 1 of an evolving project — starting as a simple rule-based bot, with planned upgrades toward persistent memory, smarter pattern matching, and eventually real AI API integration.

## Current features (Phase 1)

- Keyword-based responses with variation (multiple possible replies per keyword, chosen randomly so it doesn't feel robotic)
- Detects and remembers the user's name within a session (e.g. "my name is Obafemi")
- Personalizes later responses once it knows your name
- Clean exit on "bye"

## How it works

The bot checks user input against a dictionary of keywords mapped to possible responses. If no keyword matches, it falls back to a default "I don't understand" message. Name detection uses simple string splitting to extract the name from a fixed phrase pattern.

## How to run

```bash
python main.py
```

No external libraries required for this phase — built entirely with Python's standard library (`random`).

## Example conversation

```
You: hello
Bot: Hi there!
You: my name is Obafemi
Bot: Nice to meet you Obafemi!
You: hello
Bot: Hey Obafemi, good to see you again!
You: bye
Bot: Goodbye!
```

## Roadmap

- [x] Phase 1: Rule-based keyword matching + session memory
- [ ] Phase 2: Persistent memory (remember users across separate runs, via a saved file)
- [ ] Phase 3: Smarter pattern matching with regex, expanded keyword coverage
- [ ] Phase 4: Basic conversation context/state tracking
- [ ] Phase 5: Real AI integration via an LLM API for open-ended responses
- [ ] Phase 6: GUI version (Tkinter)
- [ ]    
