import os
from typing import List

import django


def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "match_maker_bot.settings")
    django.setup()


setup_django()

from telegram.models import Keyboard


class CodeGeneratorBackend:
    code = None
    tab = None
    level = None

    def begin(self, tab="\t"):
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        return "".join(self.code)

    def lb(self, count=1):
        self.code.append(self.tab * self.level + "\n" * count)

    def write(self, string):
        self.code.append(self.tab * self.level + string + "\n")

    def indent(self):
        self.level = self.level + 1

    def dedent(self):
        if self.level == 0:
            raise SyntaxError("internal error in code generator")
        self.level = self.level - 1


def get_keyboards() -> List[Keyboard]:
    return list(Keyboard.objects.all())


def main():
    keyboards = get_keyboards()
    codegen = CodeGeneratorBackend()
    codegen.begin(tab="    ")
    codegen.write("from enum import Enum")
    codegen.lb(2)
    codegen.write("class Keyboards(str, Enum):")
    codegen.indent()
    for keyboard in keyboards:
        codegen.write(f"{keyboard.key} = \"{keyboard.key}\"")
    codegen.lb()
    codegen.write("def __str__(self) -> str:")
    codegen.indent()
    codegen.write("return str.__str__(self)")
    codegen.dedent()
    codegen.dedent()
    code = codegen.end()
    with open("tgbot/shared/keyboards/keyboards_enum.py", "w", encoding="utf-8") as file:
        file.write(code)


if __name__ == '__main__':
    main()
