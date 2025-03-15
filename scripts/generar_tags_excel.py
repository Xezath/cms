import requests
import openpyxl
from datetime import datetime
from decouple import config

# Configuración
repo_owner = "Xezath"  # Tu nombre de usuario en GitHub
repo_name = "cms"  # El nombre de tu repositorio
token = config('TOKEN_GITHUB') # Tu token de acceso personal de GitHub
github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/tags"

# Encabezados para la autenticación
headers = {
    "Authorization": f"token {token}"
}

# Hacer la petición a la API de GitHub para obtener los tags
response = requests.get(github_api_url, headers=headers)

# Verificar si la petición fue exitosa
if response.status_code != 200:
    print(f"Error al obtener los tags: {response.status_code}")
else:
    # Crear un nuevo archivo Excel
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Versiones de Proyecto"

    # Escribir los encabezados
    sheet.append(["Versión", "Tag", "Fecha de Creación", "Descripción", "Notas Adicionales"])

    # Procesar los tags
    tags = response.json()
    for tag in tags:
        tag_name = tag['name']
        commit_sha = tag['commit']['sha']
        
        # Obtener información sobre el commit usando la API de GitHub
        commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}"
        commit_response = requests.get(commit_url, headers=headers)

        if commit_response.status_code == 200:
            commit_data = commit_response.json()
            commit_date = commit_data['commit']['committer']['date']
            commit_message = commit_data['commit']['message']
        else:
            commit_date = "Desconocida"
            commit_message = "Sin mensaje disponible"

        # Formatear la fecha del commit
        fecha_commit = datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

        # Escribir la fila con la información del tag y commit
        sheet.append([tag_name, tag_name, fecha_commit, commit_message, "Notas adicionales aquí"])

    # Guardar el archivo Excel
    wb.save(f"versiones_{repo_name}.xlsx")
    print(f"Archivo Excel generado: versiones_{repo_name}.xlsx")
