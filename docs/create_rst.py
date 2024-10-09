# create_rst.py

import os

# Define el directorio donde están tus módulos
modules = ['Contenidos',
            'Categoria',
            'Plantilla',
            'TableroKanban',
            'Usuario',
            ]  # Agrega más módulos si es necesario

for module in modules:
    # Crea un archivo .rst para cada módulo
    rst_filename = f"{module}.rst"
    with open(rst_filename, 'w') as rst_file:
        rst_file.write(f"{module} Module\n")
        rst_file.write("=" * len(module) + "\n\n")
        rst_file.write(f".. automodule:: {module}\n")
        rst_file.write("   :members:\n")
        rst_file.write("   :undoc-members:\n")
        rst_file.write("   :show-inheritance:\n\n")

print("Archivos .rst generados.")
