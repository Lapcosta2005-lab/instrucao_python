from azure.storage.blob import BlobClient
import json

# URL SAS do seu contêiner
sas_url = "https://storageprivadospia.blob.core.windows.net/intelbras?sp=racwdli&st=2025-05-14T14:44:18Z&se=2030-05-14T22:44:18Z&sv=2024-11-04&sr=c&sig=xvHwKrxe5gl24xLcVxD8plgeUwkpnNFnnW1WB9jhBA8%3D"

# Nome do arquivo a ser enviado
blob_name = "cameras.txt"

# Conteúdo JSON a ser enviado
data = [
    {    
        "ID": "8",
        "COD_CID": "4318002",
        "CIDADE": "SAO BORJA",
        "INDEX": "190",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR BR287 KM 534",
        "NOME_PONTO_2": "LPR BR287 KM 534",
        "LAT": "-29475511",
        "LONG": "-54689568",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
    {    
        "ID": "9",
        "COD_CID": "4311106",
        "CIDADE": "JAGUARI",
        "INDEX": "307",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR BR287 KM 534-1",
        "NOME_PONTO_2": "LPR BR287 KM 534-2",
        "LAT": "-29475511",
        "LONG": "-54689568",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
   {        
        "ID": "10",
        "COD_CID": "4304655",
        "CIDADE": "CAPAO DO CIPO",
        "INDEX": "27",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR RS377 KM231-1",
        "NOME_PONTO_2": "LPR RS377 KM231-2",
        "LAT": "-29014000",
        "LONG": "-54543275",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
   {
        "ID": "11",
        "COD_CID": "4318903",
        "CIDADE": "SAO LUIZ GONZAGA",
        "INDEX": "131",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR RS168 KM80-1",
        "NOME_PONTO_2": "LPR RS168 KM80-2",
        "LAT": "-28423703",
        "LONG": "-54964625",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
   {
        "ID": "12",
        "COD_CID": "4311718",
        "CIDADE": "MACAMBARA",
        "INDEX": "340",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR BR287 KM477-1",
        "NOME_PONTO_2": "LPR BR287 KM477-2",
        "LAT": "-28972298",
        "LONG": "-55527000",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    }
]

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