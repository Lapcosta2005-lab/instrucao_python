from azure.storage.blob import BlobClient
import json

# URL SAS do seu contêiner
sas_url = "https://storageprivadospia.blob.core.windows.net/intelbras?sp=racwdli&st=2025-05-14T14:44:18Z&se=2030-05-14T22:44:18Z&sv=2024-11-04&sr=c&sig=xvHwKrxe5gl24xLcVxD8plgeUwkpnNFnnW1WB9jhBA8%3D"

# Nome do arquivo a ser enviado
blob_name = "cameras.txt"

# Conteúdo JSON a ser enviado
data = [
    {
        "ID": "1",
        "COD_CID": "4316907",
        "CIDADE": "SANTA MARIA",
        "INDEX": "286",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR BR158 KM321 - 1",
        "NOME_PONTO_2": "LPR BR158 KM321 - 2",
        "LAT": "-29690022",
        "LONG": "-53773932",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
    {
        "ID": "2",
        "COD_CID": "4306601",
        "CIDADE": "DOM PEDRITO",
        "INDEX": "260",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR BR 293 KM 254 LVMTO X DPO",
        "NOME_PONTO_2": "LPR BR 293 KM 254 LVMTO X DPO",
        "LAT": "-30957267",
        "LONG": "-54687174",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
    {
        "ID": "3",
        "COD_CID": "4306601",
        "CIDADE": "DOM PEDRITO",
        "INDEX": "264",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR BR 293 KM 254 DPO X LVMTO",
        "NOME_PONTO_2": "LPR BR 293 KM 254 DPO X LVMTO",
        "LAT": "-30957024",
        "LONG": "-54687602",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
    {
        "ID": "4",
        "COD_CID": "4310702",
        "CIDADE": "ITAARA",
        "INDEX": "299",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR-ITAARA-307-1",
        "NOME_PONTO_2": "LPR-ITAARA-307-2",
        "LAT": "-29589719",
        "LONG": "-53766150",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
    {
        "ID": "5",
        "COD_CID": "4310504",
        "CIDADE": "IRAI",
        "INDEX": "112",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR-IRAI-1",
        "NOME_PONTO_2": "LPR-IRAI-2",
        "LAT": "-27176139",
        "LONG": "-53234917",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
    {
        "ID": "6",
        "COD_CID": "4310702",
        "CIDADE": "ITAARA",
        "INDEX": "282",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR-PERAU-1",
        "NOME_PONTO_2": "LPR-PERAU-1",
        "LAT": "-29640735",
        "LONG": "-53770819",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
    {
        "ID": "7",
        "COD_CID": "4303004",
        "CIDADE": "CACHOEIRA DO SUL",
        "INDEX": "327",
        "IP_PORTA": "138.122.112.98:443",
        "APP_KEY": "28054293",
        "SECRET_KEY": "tgQbsqMGcNdplBdlZXcU",
        "NOME_PONTO_1": "LPR-CACHOEIRA-1",
        "NOME_PONTO_2": "LPR-CACHOEIRA-2",
        "LAT": "-30271677",
        "LONG": "-53101124",
        "EMPRESA": "HIKVISION-RS",
        "KEY": "915DC9E2322541649496996A182313"
    },
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
        "LONG": "-55527000",
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