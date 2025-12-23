from colorama import init, Fore, Style

# Ініціалізація colorama
# autoreset=True автоматично повертає колір до стандартного після кожного виводу
init(autoreset=True)

# Колірні константи для консольного виводу
COLOR_HEADER = Fore.CYAN
COLOR_SHORTEST = Fore.GREEN
COLOR_LONGEST = Fore.RED
COLOR_DEFAULT = Fore.WHITE
COLOR_INFO = Fore.YELLOW

# Стилі тексту
STYLE_BRIGHT = Style.BRIGHT
STYLE_RESET = Style.RESET_ALL

# Текстові мітки (статуси)
LABEL_SHORTEST = " [НАЙШВИДШЕ]"
LABEL_LONGEST = " [НАЙДОВШЕ]"