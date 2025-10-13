# in a seperate termnial you can run this .py file to print the contents of the file.

def print_temp_log():
    try:
        with open("tempLog.txt", "r") as file:
            contents = file.read()
            print("=== Temperature Log ===")
            print(contents)
    except FileNotFoundError:
        print("No temperature log found. Has the logging script ran")
    except Exception as e:
        print(f"An error occurred: {e}")

print_temp_log()