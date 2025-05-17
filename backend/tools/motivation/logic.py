import random

def generate_motivation(query: str) -> str:
    quotes = [
        "You're crushing it! 💪",
        "Keep pushing—progress is progress!",
        "Success starts with believing in yourself.",
        "Every line of code is one step closer to greatness.",
        "Bugs fear the determined. Keep going!",
        "What is this sticky stuff all over the floor?",
        "It's Fiddlesticks time!"
    ]

    return random.choice(quotes)