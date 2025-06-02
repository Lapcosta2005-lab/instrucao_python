from azure.storage.blob import BlobClient
import json

# URL SAS do seu contêiner
sas_url = "https://storageprivadospia.blob.core.windows.net/hikvision?sp=racwdli&st=2024-11-19T18:47:55Z&se=2027-11-20T02:47:55Z&sv=2022-11-02&sr=c&sig=SzM2nM6aZf01JPxrmyTozw%2FZDfo7YwbLK1XY9Y9jQ8E%3D"

# Nome do arquivo a ser enviado - padrao: códigocidade.txt
blob_name = "12MACAMBARA.txt"

# Conteúdo JSON a ser enviado
data = {
    "dataHora": "2025-06-02T16:00:45-03:00"
}

# Converter o dicionário em uma string JSON
json_data = json.dumps(data)

# Separar a URL base e o token SAS
base_url = sas_url.split('?')[0]
sas_token = sas_url.split('?')[1]

# Construir a URL completa do blob
blob_url = f"{base_url}/{blob_name}?{sas_token}"

# Criar um BlobClient usando a URL do blob
blob_client = BlobClient.from_blob_url(blob_url)

# Enviar o conteúdo para o Azure Blob Storage
blob_client.upload_blob(json_data, overwrite=True)

print(f"O arquivo {blob_name} foi enviado com sucesso.")