import json
# Não precisamos mais importar BlobClient do azure.storage.blob

# O conteúdo JSON a ser salvo
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

# Caminho completo para o arquivo local onde você quer salvar
caminho_arquivo_local = r"C:\Users\bdi12\Documents\codigos_python\AB\HikAb\cameras.txt"

# Converter a estrutura de dados Python (lista de dicionários) em uma string JSON
# O indent=4 formata o JSON para ser mais legível no arquivo
json_data_formatado = json.dumps(data, indent=4, ensure_ascii=False) # Adicionado ensure_ascii=False para caracteres especiais

# Salvar o conteúdo JSON no arquivo local especificado
# O modo 'w' abre o arquivo para escrita, criando-o se não existir ou sobrescrevendo se existir.
# Usamos 'encoding="utf-8"' para garantir que o arquivo seja salvo com a codificação correta.
try:
    with open(caminho_arquivo_local, 'w', encoding='utf-8') as arquivo_local:
        arquivo_local.write(json_data_formatado)

    print(f"O conteúdo JSON foi salvo com sucesso em {caminho_arquivo_local}")

except Exception as e:
    print(f"Ocorreu um erro ao tentar salvar o arquivo: {e}")
    print(f"Verifique se o caminho '{caminho_arquivo_local}' existe e se você tem permissões de escrita.")

