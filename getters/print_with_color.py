import colorama

colorama.init(autoreset = True)

def print_green(text):
    text = str(text)
    print(colorama.Fore.GREEN + text)

def print_yellow(text):
    text = str(text)
    print(colorama.Fore.YELLOW + text)

def print_red(text):
    text = str(text)
    print(colorama.Fore.RED + text)