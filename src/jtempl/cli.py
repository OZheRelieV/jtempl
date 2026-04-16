import argparse

from .template_builder import NotebookTemplateBuilder


def main():
    parser = argparse.ArgumentParser(
        description="Генератор шаблонов jupyter notebook из yaml"
    )
    parser.add_argument(
        "--config",
        default="./jtempl/config.yaml",
        help="Путь к yaml-конфигу"
    )
    parser.add_argument(
        "--output",
        default="template.ipynb",
        help="Путь к выходному .ipynb"
    )
    args = parser.parse_args()

    builder = NotebookTemplateBuilder(args.config, args.output)
    builder.generate()
