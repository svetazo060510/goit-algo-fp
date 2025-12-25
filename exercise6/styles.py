from colorama import init, Fore, Style

# Ініціалізація colorama з автоматичним скиданням стилів
init(autoreset=True)

# Колірні константи для консольного виводу
COLOR_HEADER = Fore.CYAN + Style.BRIGHT
COLOR_GREEDY = Fore.YELLOW
COLOR_DP = Fore.MAGENTA
COLOR_WINNER = Fore.GREEN + Style.BRIGHT
COLOR_DEFAULT = Fore.WHITE
COLOR_INFO = Fore.BLUE

# Стилі тексту
STYLE_BRIGHT = Style.BRIGHT
STYLE_RESET = Style.RESET_ALL