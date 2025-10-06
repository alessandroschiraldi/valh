def print_hello(string="world"):
    print(f"hello {string} !")

def ask_name():
    print("What is your name?")

def retrieve_name():
    name = input()
    return name

def main():
    ask_name()
    name = retrieve_name()
    print_hello(name)

main()
