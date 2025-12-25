from colorama import init, Fore, Style

# Ініціалізація colorama з автоматичним скиданням стилів
init(autoreset=True)

# Колірні константи для консольного виводу
COLOR_HEADER = Fore.CYAN + Style.BRIGHT
COLOR_MC = Fore.BLUE
COLOR_ANALYTICAL = Fore.YELLOW
COLOR_DIFF = Fore.RED
COLOR_SUCCESS = Fore.GREEN + Style.BRIGHT
COLOR_DEFAULT = Fore.WHITE

# Стилі тексту
STYLE_BRIGHT = Style.BRIGHT
STYLE_RESET = Style.RESET_ALL