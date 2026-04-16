from pathlib import Path

import nbformat
import yaml
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


class NotebookTemplateBuilder:
    __slots__ = ("config_path", "output_path", "config", "nb")

    def __init__(self, config_path: str | Path, output_path: str | Path):
        self.config_path = Path(config_path)
        self.output_path = Path(output_path)
        self.config = self._load_config()
        self.nb = new_notebook()

    def _load_config(self) -> dict:
        with self.config_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _validate(self) -> None:
        sections = self.config.get("sections", [])
        if not sections:
            raise ValueError(
                "Конфигурация не содержит раздел 'sections'."
            )
        if len(sections) != 1:
            raise ValueError(
                "Ожидается ровно один корневой раздел 'sections'."
            )
        if not sections[0].get("is_toc"):
            raise ValueError(
                "Первый раздел в 'sections' должен быть оглавлением."
            )
        if not sections[0].get("content"):
            raise ValueError(
                "Раздел оглавления должен содержать 'content'."
            )

    def _build_toc(self) -> str:
        toc = self.config["sections"][0]
        level = toc.get("heading_level", 1)
        title = toc.get("name", "Содержание")
        lines = [f"{'#' * level} {title}"]
        lines += [
            f"- [{item.get('name', 'Раздел')}](#id{i})"
            for i, item in enumerate(toc["content"])
        ]
        return "\n".join(lines)

    def _build_imports(self, modules: list) -> str:
        if not modules:
            raise ValueError(
                "Раздел помечен как импорты, но список модулей пуст."
            )

        imports = []
        for mod in modules:
            name = mod.get("module", "unknown_module")
            alias = mod.get("alias")
            funcs = mod.get("imports", [])

            if alias and funcs:
                raise NotImplementedError(
                    "Импорт функций с алиасом пока не поддерживается."
                )
            if alias:
                imports.append(f"import {name} as {alias}")
            elif funcs:
                imports.append(f"from {name} import {', '.join(funcs)}")
            else:
                imports.append(f"import {name}")
        return "\n".join(imports)

    def generate(self) -> None:
        self._validate()

        self.nb.cells.append(new_markdown_cell(self._build_toc()))

        for section in self.config["sections"][0]["content"]:
            level = section.get("heading_level", 1)
            name = section.get("name", "Раздел")
            self.nb.cells.append(new_markdown_cell(f"{'#' * level} {name}"))

            if section.get("is_imports"):
                self.nb.cells.append(
                    new_code_cell(
                        self._build_imports(section.get("modules", []))
                    )
                )
            else:
                self.nb.cells.append(new_code_cell())

        nbformat.write(self.nb, self.output_path)
        print(f"Шаблон успешно сохранён: {self.output_path}")
