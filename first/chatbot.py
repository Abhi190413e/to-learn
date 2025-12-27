import random

class Chatbot:
    def __init__(self, name):
        self.name = name
        self.greetings = ["Hello! How can I help you today?", "Hi there! Shoot your doubt!", "Welcome to New Educate Academy. Ask away!"]
        self.farewells = ["Goodbye! Keep learning.", "See you soon!", "Happy studying!"]
        self.unknown = ["I'm not sure about that. Can you rephrase?", "That's interesting. Tell me more.", "I'm still learning!"]

    def get_response(self, message):
        message = message.lower()
        
        if "hello" in message or "hi" in message:
            return random.choice(self.greetings)
        elif "bye" in message:
            return random.choice(self.farewells)
        elif "course" in message:
            return "We offer a variety of courses including Web Development, Data Science, and Python. Check out the Courses page!"
        elif "calendar" in message or "schedule" in message:
            return "You can view your upcoming classes and tasks on the Schedule page."
        elif "live" in message or "meet" in message:
            return "Join the live sessions from the Live Meets page. Don't miss out!"
        elif "doubt" in message or "help" in message:
            return "I'm here to clear your doubts! Please ask your specific question."
        elif "price" in message or "cost" in message:
            return "Our courses are affordably priced. Visit the course details for specific pricing."
        else:
            return random.choice(self.unknown)
