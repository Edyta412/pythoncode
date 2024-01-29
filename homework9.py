
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)
    return wrapper

contacts = {}

@input_error
def hello_command():
    return "How can I help you?"

@input_error
def add_command(name, phone):
    contacts[name] = phone
    return f"Added contact: {name}, {phone}"

@input_error
def change_command(name, phone):
    contacts[name] = phone
    return f"Changed phone for contact {name} to {phone}"

@input_error
def phone_command(name):
    return f"Phone for contact {name}: {contacts[name]}"

@input_error
def show_all_command():
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def main():
    print("Bot Assistant Console:")
    print("Type 'good bye', 'close', or 'exit' to end.")
    while True:
        user_input = input("Your command: ").lower()

        if user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        elif user_input == "hello":
            print(hello_command())
        elif user_input.startswith("add"):
            _, name, phone = user_input.split()
            print(add_command(name, phone))
        elif user_input.startswith("change"):
            _, name, phone = user_input.split()
            print(change_command(name, phone))
        elif user_input.startswith("phone"):
            _, name = user_input.split()
            print(phone_command(name))
        elif user_input == "show all":
            print(show_all_command())
        else:
            print("Invalid command. Type 'hello' to start.")

if __name__ == "__main__":
    main()