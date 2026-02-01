import logging

# Console colors
red = '\x1b[31m'
green = '\x1b[32m'
yellow = '\x1b[33m'
blue = '\x1b[34m'
purple = '\x1b[35m'
cyan = '\x1b[36m'
white = '\x1b[37m'

# Help text
help = f'''{yellow}
Simple usage: {red}python3 {green}logic.py {cyan}target(with/without http-https) {blue}delay
Example : {red}python3 {green}logic.py {cyan}google.com {blue}1
'''

logging.basicConfig(
    level=logging.INFO,
    format=f'{cyan}%(asctime)s {red}[%(levelname)s] {white}%(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def info(message):
    logging.info(f'{green}{message}')

def warning(message):
    logging.warning(f'{yellow}{message}')

def error(message):
    logging.error(f"{red}{message}")
