from AppClass import App
from ConsoleArgumentsHandlerClass import ConsoleArgumentsHandler

if __name__ == "__main__":
    args = ConsoleArgumentsHandler().get_args()
    App(args=args).run()
