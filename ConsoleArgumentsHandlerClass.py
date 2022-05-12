import argparse


class ConsoleArgumentsHandler:

    # Read args from terminal
    def __init__(self):
        parser = argparse.ArgumentParser(description='Land simulation')
        parser.add_argument('-c', '--console', action='store_true', help="GUI in console", default=True)
        parser.add_argument('-w', '--window', action='store_true', help="GUI as window", default=False)

        self.args = parser.parse_args()

    # Return args
    def get_args(self):
        return self.args
