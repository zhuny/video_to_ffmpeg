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

        from app.command.cmd_file import run as file_run
        self._register(file_run)

        from app.command.cmd_piece import run as piece_run
        self._register(piece_run)

        from app.command.cmd_gen import run as gen_run
        self._register(gen_run)

        from app.command.cmd_list import run as list_run
        self._register(list_run)

        from app.command.cmd_piece_update import run as piece_update_run
        self._register(piece_update_run)

        from app.command.cmd_video_update import run as video_update_run
        self._register(video_update_run)

        from app.command.cmd_upload import run as upload_run
        self._register(upload_run)

    def run(self):
        args = self.parser.parse_args()
        kwargs = dict(vars(args))
        kwargs.pop('func')
        args.func(**kwargs)

    def _register(self, func):
        doc = FunctionDoc.parse(func.__doc__)

        parser = self.subparser.add_parser(
            self._get_cmd_name(func),
            help=doc.doc
        )

        result = inspect.signature(func)
        for name, anno in result.parameters.items():
            anno_type = anno.annotation
            # pydantic support for custom type
            anno_type = getattr(anno_type, 'validate', anno_type)
            parser.add_argument(
                name,
                type=anno_type,
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
