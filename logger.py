class PrettyLogger(object):

    def info(self, message: str):
        print(f"\033[94m[i] {message}\033[0m")  # Blue

    def warning(self, message: str):
        print(f"\033[93m[!] {message}\033[0m")  # Yellow

    def error(self, message: str):
        print(f"\033[91m[X] {message}\033[0m")  # Red

    def debug(self, message: str):
        print(f"\033[92m[_] {message}\033[0m")  # Green