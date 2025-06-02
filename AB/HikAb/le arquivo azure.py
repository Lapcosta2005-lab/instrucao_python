from azure.storage.blob import BlobClient
import json

# URL SAS do seu contêiner
sas_url = "https://storageprivadospia.blob.core.windows.net/hikvision?sp=racwdli&st=2024-11-19T18:47:55Z&se=2027-11-20T02:47:55Z&sv=2022-11-02&sr=c&sig=SzM2nM6aZf01JPxrmyTozw%2FZDfo7YwbLK1XY9Y9jQ8E%3D"

# Nome do arquivo a ser lido
#blob_name = "1JARDIM_ALEGRE.txt"
#blob_name = "29SANTA_HELENA.txt"
blob_name = "12MACAMBARA.txt"

# Separar a URL base e o token SAS
base_url = sas_url.split('?')[0]
sas_token = sas_url.split('?')[1]

# Construir a URL completa do blob
blob_url = f"{base_url}/{blob_name}?{sas_token}"

# Criar um BlobClient usando a URL do blob
blob_client = BlobClient.from_blob_url(blob_url)

# Baixar o conteúdo do blob
download_stream = blob_client.download_blob()
conteudo = download_stream.readall()

# Converter o conteúdo para string (assumindo que é texto)
conteudo_texto = conteudo.decode('utf-8')

# Se o conteúdo for JSON, podemos carregá-lo como um dicionário
data = json.loads(conteudo_texto)

# Exibir os dados
print("Conteúdo do arquivo:")
print(conteudo_texto)

print("\nDados JSON:")
print(type(data))
print(data.get('dataHora'))