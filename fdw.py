from src.argument_parser import FDWArgs, cli_args


class FDW:

    args: FDWArgs

    def __init__(self, args: FDWArgs):
        self.args = args

        self.states = {}


def main():

    app = FDW(cli_args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
