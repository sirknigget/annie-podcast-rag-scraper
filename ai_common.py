def add_user_message(user, messages):
    messages.append({"role": "user", "content": user})
    return messages

def add_system_message(system, messages):
    messages.append({"role": "system", "content": system})
    return messages

def add_assistant_message(assistant, messages):
    messages.append({"role": "assistant", "content": assistant})
    return messages