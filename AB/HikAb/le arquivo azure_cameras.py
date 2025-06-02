from azure.storage.blob import BlobClient
import json

# URL SAS do seu contêiner
sas_url = "https://storageprivadospia.blob.core.windows.net/intelbras?sp=racwdli&st=2025-05-14T14:44:18Z&se=2030-05-14T22:44:18Z&sv=2024-11-04&sr=c&sig=xvHwKrxe5gl24xLcVxD8plgeUwkpnNFnnW1WB9jhBA8%3D"

# Nome do arquivo a ser lido
blob_name = "cameras_hik_rs.txt"
#blob_name = "4JARDIM_ALEGRE.txt"
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
#print(data.get('dataHora'))