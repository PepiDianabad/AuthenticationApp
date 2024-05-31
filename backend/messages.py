messages_store = []

def get_messages():
    return messages_store

def add_message(username, content):
    messages_store.append({"user": username, "content": content})
