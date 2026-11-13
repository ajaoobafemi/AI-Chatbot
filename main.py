import json
import os
import random
import re

# ---------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------
MAX_HISTORY = 50  # how many past exchanges we keep per user

GREETINGS = ["Hi there!", "Hey!", "Hello! How can I help?"]

responses = {
    "hello": GREETINGS,
    "hi": GREETINGS,
    "hey": GREETINGS,
    "how are you": ["I'm doing great, thanks!", "I'm just a bot, but I'm good!"],
    "thank": ["You're welcome!", "Anytime!"],
    "who are you": ["I'm a chatbot you're building, one phase at a time!"],
    "help": ["Tell me your name, where you live, or what you like. "
             "Ask 'what do you know about me' or 'what did we talk about'."],
}

# Words that look like names after "I'm ..." but aren't
NOT_NAMES = {"fine", "good", "great", "okay", "ok", "happy", "sad", "tired",
             "hungry", "bored", "well", "here", "back", "sorry", "sure",
             "ready", "busy", "glad"}

EXIT_PATTERN = r"\b(bye|goodbye|exit|quit)\b"


# ---------------------------------------------------------------
# MEMORY (Phase 2 + Phase 4)
# Each user's file looks like:
# {"name": "Bob",
#  "facts": {"age": 19, "location": "Ibadan", "likes": ["football"],
#            "details": {"football": "the goals"}},
#  "history": [{"you": "hello", "bot": "Hi there!"}, ...]}
# ---------------------------------------------------------------
def clean_username(raw):
    """Keep only letters, numbers and underscores so the filename is safe."""
    cleaned = re.sub(r"[^a-z0-9_]", "", raw.strip().lower())
    return cleaned or "guest"


def load_memory(filename):
    memory = {"name": None, "facts": {}, "history": []}
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                memory.update(json.load(f))  # old files with only a name still work
        except json.JSONDecodeError:
            print("Bot: (Your memory file was damaged, so I'm starting fresh.)")
    return memory


def save_memory(filename, memory):
    with open(filename, "w") as f:
        json.dump(memory, f, indent=2)


# ---------------------------------------------------------------
# PATTERN MATCHING (Phase 3)
# ---------------------------------------------------------------
def extract_name(text):
    """Catches: 'my name is Bob', 'call me Bob', 'I'm Bob', 'I am Bob'.
    The 'I'm ...' patterns need a capital letter, otherwise
    'I'm going' would be treated as the name 'Going'."""
    patterns = [
        (r"\bmy name is (\w+)", re.IGNORECASE),
        (r"\bcall me (\w+)", re.IGNORECASE),
        (r"\b[Ii] am ([A-Z][a-z]+)\s*[.!]?$", 0),
        (r"\b[Ii]'?m ([A-Z][a-z]+)\s*[.!]?$", 0),
    ]
    for pattern, flags in patterns:
        match = re.search(pattern, text, flags)
        if match:
            word = match.group(1)
            if word.lower() in NOT_NAMES or word.isdigit():
                continue
            return word.capitalize()
    return None


def extract_facts(text):
    """Pulls out age, location and likes from natural sentences."""
    found = {}

    match = re.search(r"\bi(?:'?m|\s+am)\s+(\d{1,3})\b", text, re.IGNORECASE)
    if match:
        found["age"] = int(match.group(1))

    match = re.search(r"\bi live in ([a-zA-Z ]+?)\s*(?:[.!,?]|\band\b|$)",
                      text, re.IGNORECASE)
    if match:
        found["location"] = match.group(1).strip().title()

    match = re.search(r"\bi (?:really )?(?:like|love|enjoy) ([a-zA-Z ]+?)\s*(?:[.!,?]|\band\b|$)",
                      text, re.IGNORECASE)
    if match:
        found["like"] = match.group(1).strip().lower()

    return found


def keyword_reply(lower, name):
    """Whole-word keyword matching, so 'hi' won't match inside 'this'."""
    for keyword, options in responses.items():
        if re.search(rf"\b{re.escape(keyword)}\b", lower):
            if keyword in ("hello", "hi", "hey") and name:
                return f"Hey {name}, good to see you again!"
            return random.choice(options)
    return "I don't understand that yet."


# ---------------------------------------------------------------
# RECALL (Phase 4)
# ---------------------------------------------------------------
def describe_memory(memory):
    facts = memory["facts"]
    known = []
    if memory["name"]:
        known.append(f"your name is {memory['name']}")
    if "age" in facts:
        known.append(f"you're {facts['age']}")
    if "location" in facts:
        known.append(f"you live in {facts['location']}")
    if facts.get("likes"):
        known.append("you like " + ", ".join(facts["likes"]))
    for topic, detail in facts.get("details", {}).items():
        known.append(f'about {topic} you said "{detail}"')

    if not known:
        return "I don't know much about you yet. Tell me your name or what you like!"
    return "So far I know that " + "; ".join(known) + "."


def recall_topics(memory):
    recent = [h["you"] for h in memory["history"][-5:]]
    if not recent:
        return "We haven't talked about much yet."
    return "Recently you told me: " + " | ".join(f'"{m}"' for m in recent)


# ---------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------
def main():
    username = clean_username(input("Enter your username: "))
    filename = f"memory_{username}.json"
    memory = load_memory(filename)

    # "pending" is the bot's short-term state (Phase 4): if the bot just asked
    # a question, the user's NEXT message is treated as the answer.
    pending = None

    if memory["name"]:
        print(f"Bot: Welcome back {memory['name']}!")
        if memory["history"]:
            print(f"Bot: Last time, you told me: \"{memory['history'][-1]['you']}\"")
    else:
        print("Bot: Welcome! I don't think we've met.")

    while True:
        text = input("You: ").strip()
        if not text:
            continue
        lower = text.lower()

        # --- exit ---
        if re.search(EXIT_PATTERN, lower):
            name_part = f", {memory['name']}" if memory["name"] else ""
            print(f"Bot: Goodbye{name_part}!")
            break

        previous_pending, pending = pending, None
        reply = None
        log_it = True  # questions about memory shouldn't be stored as "things you told me"

        # --- memory commands ---
        if re.search(r"what do you know about me", lower):
            reply = describe_memory(memory)
            log_it = False
        elif re.search(r"what did we (talk|discuss)|do you remember", lower):
            reply = recall_topics(memory)
            log_it = False
        else:
            # --- learn new things from the sentence ---
            name = extract_name(text)
            found = extract_facts(text)
            parts = []

            if name:
                memory["name"] = name
                parts.append(f"Nice to meet you {name}!")

            if "age" in found:
                memory["facts"]["age"] = found["age"]
                parts.append(f"{found['age']}, nice!")

            if "location" in found:
                memory["facts"]["location"] = found["location"]
                parts.append(f"{found['location']} sounds like a great place!")

            if "like" in found:
                thing = found["like"]
                likes = memory["facts"].setdefault("likes", [])
                if thing not in likes:
                    likes.append(thing)
                parts.append(f"Nice, {thing}! What do you enjoy most about it?")
                pending = ("like", thing)

            if parts:
                reply = " ".join(parts)
            elif previous_pending:
                # the bot asked a question last turn, so this message is the answer
                _, topic = previous_pending
                memory["facts"].setdefault("details", {})[topic] = text
                reply = f"Got it, I'll remember that about {topic}."
            else:
                reply = keyword_reply(lower, memory["name"])

        print("Bot:", reply)

        # --- remember this exchange, saved right away ---
        if log_it:
            memory["history"].append({"you": text, "bot": reply})
            memory["history"] = memory["history"][-MAX_HISTORY:]
        save_memory(filename, memory)


if __name__ == "__main__":
    main()