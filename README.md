# jTempl
---

This utility allow to create jupyter notebook with user defined structure and python modules that common for most data science and machine learning project.

# Config structure
1. Root section should be `sections`
2. First section is `ToC`
3. `Toc` contain following attrs: [(cell) *type*, *heading_level*, flag *is_toc*, *content*]
4. In ToC you can describe structure of your project
5. `Imports` sections contain all information that used to generate code cell with correct module imports. Specific attrs here: [flag *is_imports*, *modules* that contain *module*, *alias*, *imports*]
6. Common attrs for all sections: [*name*, (cell) *type*, *heading_level*]
---

**You can explore default generation config in source folder.**
