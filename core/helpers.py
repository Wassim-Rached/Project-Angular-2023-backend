from dotenv import load_dotenv
import os

ENV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env')


def load_dotenv_file(dotenv_file_name: str):
    load_dotenv(os.path.join(ENV_DIR, dotenv_file_name))

    Console.log("==> env file loaded : " + dotenv_file_name, Console.OKCYAN)


class Console:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def log(text, color_code):
        return print(f"{color_code}{text}{Console.ENDC}")
