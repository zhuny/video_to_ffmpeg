import argparse
import inspect
import re


class FunctionDoc:
    def __init__(self, doc: str, param_doc: dict[str, str]):
        self.doc = doc
        self.param_doc = param_doc

    @classmethod
    def parse(cls, doc: str):
        main_doc = []
        param_doc = {}

        pattern = re.compile(r':param (\w+):(.+)')

        for line in doc.splitlines():
            line = line.strip()
            g = pattern.fullmatch(line)
            if g is None:
                main_doc.append(line)
            else:
                name, desc = g.groups()
                param_doc[name] = desc

        return cls("\n".join(main_doc).strip(), param_doc)


class MyParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="main.py")
        self.subparser = self.parser.add_subparsers(title="cli", required=True)

    def bind(self):
        from app.command.cmd_create import run as create_run
        self._register(create_run)

    def run(self):
        args = self.parser.parse_args()
        print(args)

    def _register(self, func):
        doc = FunctionDoc.parse(func.__doc__)

        parser = self.subparser.add_parser(
            self._get_cmd_name(func),
            help=doc.doc
        )

        result = inspect.signature(func)
        for name, anno in result.parameters.items():
            parser.add_argument(
                name,
                type=anno.annotation,
                help=doc.param_doc.get(name, '-')
            )

        parser.set_defaults(func=func)

    def _get_cmd_name(self, func):
        return func.__module__.split('.')[-1].removeprefix('cmd_')


def main():
    parser = MyParser()
    parser.bind()
    parser.run()


if __name__ == '__main__':
    main()
