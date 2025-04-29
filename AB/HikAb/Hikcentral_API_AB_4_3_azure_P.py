import requests
import urllib3
import base64
import hashlib
import hmac
import logging
import json
from PIL import Image, ImageFile
import io
import threading
from datetime import datetime, timedelta
import pytz
import pandas as pd
import time
from azure.storage.blob import BlobClient
from concurrent.futures import ThreadPoolExecutor, as_completed

#time.sleep(10)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(
     level=logging.ERROR,
     format='%(asctime)s - %(levelname)s - %(message)s'
)

class CameraProcessor:
    def __init__(self, config):
        self.id = config['ID']
        self.cod_cid = config['COD_CID']
        self.cidade = config['CIDADE']
        self.index = config['INDEX']
        self.ip_porta = config['IP_PORTA']
        self.app_key = str(config['APP_KEY'])
        self.secret_key = str(config['SECRET_KEY'])
        self.nome_ponto_1 = config['NOME_PONTO_1']
        self.nome_ponto_2 = config['NOME_PONTO_2']
        self.lat = str(config['LAT'])
        self.long = str(config['LONG'])
        self.empresa = config['EMPRESA']
        self.key = config['KEY']
        ip, port = config['IP_PORTA'].split(':')
        self.url_base = f"https://{ip}.sslip.io:{port}/artemis/api/"
        self.session = requests.Session()  # Cria uma sessão persistente
        self.session.verify = False  # Desativa avisos de certificado SSL

    def get_signature(self, message, key):
        byte_key = bytes(key, 'UTF-8')
        enc_msg = message.encode()
        h = hmac.new(byte_key, enc_msg, hashlib.sha256).digest()
        return base64.b64encode(h)

    def get_records(self, dt_start, dt_end, num_max):
    
        message_rec = f'POST\napplication/json\napplication/json;charset=UTF-8\nx-ca-key:{self.app_key}\n/artemis/api/pms/v1/crossRecords/page'
        headers_rec = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'x-ca-key': self.app_key,
            'x-ca-signature-headers': 'x-ca-key',
            'x-ca-signature': self.get_signature(message_rec, self.secret_key),
        }
        data_rec = {
            'cameraIndexCode': str(self.index),
            'startTime': dt_start,
            'endTime': dt_end,
            'pageNo': 1,
            'pageSize': num_max
        }
        try:
            url_rec = self.url_base + 'pms/v1/crossRecords/page'
            res_rec = self.session.post(url_rec, headers=headers_rec, data=json.dumps(data_rec), timeout=10)
            #print(url_rec)
            #print(res_rec.text) #consigo ver a resposta do servid0r
            return json.loads(res_rec.text)
        except requests.exceptions.RequestException as e:
            #print(f"Erro ao obter registros: {e}")
            return None

    def get_pictures(self, pic_uri):
        message_img = f'POST\napplication/json\napplication/json;charset=UTF-8\nx-ca-key:{self.app_key}\n/artemis/api/pms/v1/image'
        headers_img = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'x-ca-key': self.app_key,
            'x-ca-signature-headers': 'x-ca-key',
            'x-ca-signature': self.get_signature(message_img, self.secret_key),
        }
        data_img = {'picUri': pic_uri}
        url_img = self.url_base + 'pms/v1/image'
        try:
            res_img = self.session.post(url_img, headers=headers_img, data=json.dumps(data_img), verify=False, timeout=10)
            img = base64.b64decode(res_img.text.replace('data:image/jpeg;base64,', ''))
            #print('adiquirida imagem')
            return img
        except requests.exceptions.RequestException as e:
            #print(f"Erro ao obter imagem: {e}")

            return None
    
    def enviaAB(self, line,placa,datahora,carType,imagem): #função responsável pelo envio dos dados ao AB, é enviado os dados veículo por veículo
    
        ponto = None  # Inicializa a variável
        imagem_base64 = base64.b64encode(imagem)
        # Converter os bytes codificados em uma string, se necessário
        imagem_base64_string = imagem_base64.decode('utf-8')
        if len(imagem_base64_string)>1000000:
            print('tamanaho payload excedido')    
        #print(len(imagem_base64_string))      
    
        #print(type(base64_string))
        #essa parte realiza a separação dos fluxos. Para ver o sentido do veículo.
        if line == 1:
            ponto = self.nome_ponto_1
        if line == 2:
            ponto = self.nome_ponto_2
        latitude = self.corrigir_Latlong(self.lat)
        longitude = self.corrigir_Latlong(self.long)
        #print(latitude)
        #print(longitude)
        # URL para onde será enviada a requisição
        ab_url = "https://spiaeventos.servicebus.windows.net/stream09/messages"  #P
        #ab_url = "https://poc-eventos-prf.servicebus.windows.net/spia-hmg/messages"  #H

        # Payload (dados) que você deseja enviar
        payload = {
            "placa" : placa,
            "dataHoraTz": datahora,
            "camera": {
                "numero": ponto,
                "latitude": latitude,
                "longitude": longitude
            },
            "empresa":self.empresa,
            "key": self.key,
            "tipoVeiculo": carType,
            "imagem": {
            "imgVeiculo": imagem_base64_string
            },
         }

        # Headers opcionais (por exemplo, para autenticação ou especificar o formato do payload)
        headers = {
         "Content-Type": "application/json",  # Se o payload for JSON, use esse Content-Type
         "Authorization": "SharedAccessSignature sr=spiaeventos.servicebus.windows.net%2Fstream09&sig=2W6jUkqrlEmu3FjoyeRxF2BAkphNYd6sfl%2F85xhl34A%3D&se=1872219041&skn=prf-hikivision", #P
         #"Authorization": "SharedAccessSignature sr=poc-eventos-prf.servicebus.windows.net%2Fspia-hmg&sig=owa9Ba%2FWfc0fGvNG7pFFIMVesvH5luCPMYhq6uRyv6k%3D&se=1764889987&skn=envio" #H        
        }
        #print(payload)
        # Enviar a requisição POST

        try:
            response = requests.post(ab_url, json=payload, headers=headers,timeout=10)
            #Exibir o código de status da resposta e o conteúdo da resposta
            #print(f"Status Code: {response.status_code} enviada passagem do ponto {self.index} do local {self.empresa} no time: {datahora} ")
            if response.status_code == 413:
                print(f' Payload excedido : {len(imagem_base64_string)}')
            #logging.info(f"Status Code: {response.status_code} enviada passagem do ponto {self.index} do local {self.empresa} ")
        
        except requests.exceptions.Timeout:
            print(f"Timeout! A requisição demorou mais do que o esperado index:{self.index} do local {self.cidade} ")
            #logging.info(f"Timeout! A requisição demorou mais do que o esperado index:/{self.index} do local {self.cidade} ")
        

        except requests.exceptions.RequestException as e:
            #print(f"Erro na requisição: {e}")
            logging.ERROR(f"Erro na requisição: {e}")

    def hora_atual_formatada(self):
        # Definir o fuso horário, no caso, o horário de Brasília (GMT-3)
        fuso_horario = pytz.timezone("America/Sao_Paulo")
        # Obter a hora atual com o fuso horário
        hora_atual = datetime.now(fuso_horario)
        # Formatar com os dois pontos no fuso horário (-03:00)
        hora_formatada = hora_atual.strftime('%Y-%m-%dT%H:%M:%S%z')
        return hora_formatada[:-2] + ':' + hora_formatada[-2:]

    def corrigir_Latlong(self,numero_str):
         # Verifica se é uma string e remove espaços, se necessário
        numero_str = numero_str.strip()
        # Adiciona o ponto decimal após os dois primeiros dígitos
        numero_corrigido_str = numero_str[:3] + "." + numero_str[3:]
        # Converte para float
        return float(numero_corrigido_str)

    def process_camera_once(self):
            try:
                datahora = None
                #car_type = "indisponivel"
                dt_start = self.le_ArquivoAzure(f"{self.id}{self.cidade}.txt") #azure
                dt_start_2 = datetime.fromisoformat(dt_start)
                dt_start_2 = dt_start_2 + timedelta(seconds=1) #necessario para nao repetir o ultimo veiculo
                dt_start_3 = dt_start_2.isoformat() 
                #dt_start = "2025-01-21T10:30:00-03:00"
                hora_formatada_atual = self.hora_atual_formatada()
                dt_end = hora_formatada_atual
       
                data1 = datetime.fromisoformat(dt_start)
                data2 = datetime.fromisoformat(dt_end)
                diferenca = abs(data2 - data1) #necessário para saber se houve 30 dias transcorridos
                
                if diferenca > timedelta(days=30):
                   dt_start_3 = data2 - timedelta(seconds=60)
                   print('hikcenter ficou 30 dias fora')
                   dt_start_3 = dt_start_3.isoformat()
                   print(dt_start_3)

                contador = 0                
                print(f'iniciado o processamento a partir {dt_start_3} do ponto INDEX {self.index}, da empresa {self.cidade} ')
                records = self.get_records(dt_start_3, dt_end, 50)
                if not records:
                     print('Camera off line ou erro')
                else:
                    for record in records['data']['list']:
                        linha = record['vehicleDirectionType']
                        placa = record['plateNo']
                        #print(placa)
                        datahora = record['crossTime']
                        car_type = record['vehicleType']
                      
                        foto = self.get_pictures(record['vehiclePicUri'])
                        if (len(foto)) > 750000:
                            foto = self.converter_imagem_para_webp(foto)
                        if foto:
                            self.enviaAB(linha, placa, datahora, car_type, foto)
                            contador = contador + 1    
                    self.salva_DadosAzure(self.id,self.cidade,datahora) #azure 
                    print(f'enviadas {contador} imagens ao AB do ponto {self.cidade}')          
            except Exception as e:
                if datahora:
                    print('Encontrei algum erro na hora de enviar, estou salvando ultima data/hora dos ja enviados')
                    self.salva_DadosAzure(self.id,self.cidade,datahora) #azure 
                erro = str(e)
                #logging.ERROR(f"Erro no processamento da câmera {self.index}: {e}")
                if "list" in erro:  # Verificar se a mensagem contém 'list'
                   print(f"Sem passagens no tempo determinado")
                else:
                    print(f"Erro no processamento da câmera {self.index}/{self.cidade}:erro encontrado: {e}")

    def converter_imagem_para_webp(self,image_bytes):
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        # Carregar a imagem a partir dos bytes
        img = Image.open(io.BytesIO(image_bytes))
        # Buffer de memória para armazenar a imagem convertida
        img_bytes_io = io.BytesIO()
         # Salvar a imagem no formato WebP com compressão padrão
        img.save(img_bytes_io, format='JPEG', quality=20)  # Você pode ajustar a qualidade se necessário
        # Retornar a imagem como bytes
        img_bytes_io.seek(0)  # Retornar ao início do buffer
        return img_bytes_io.getvalue()
    
    def hora_atual_formatada(self):
        # Definir o fuso horário, no caso, o horário de Brasília (GMT-3)
        fuso_horario = pytz.timezone("America/Sao_Paulo")
        # Obter a hora atual com o fuso horário
        hora_atual = datetime.now(fuso_horario)
        # Formatar com os dois pontos no fuso horário (-03:00)
        hora_formatada = hora_atual.strftime('%Y-%m-%dT%H:%M:%S%z')
        return hora_formatada[:-2] + ':' + hora_formatada[-2:]

    def corrigir_Latlong(self,numero_str):
         # Verifica se é uma string e remove espaços, se necessário
        numero_str = numero_str.strip()
        # Adiciona o ponto decimal após os dois primeiros dígitos
        numero_corrigido_str = numero_str[:3] + "." + numero_str[3:]
        # Converte para float
        return float(numero_corrigido_str)
    
    def le_ArquivoAzure(self, name):
        #print(name)
        # URL SAS do seu contêiner
        sas_url = "https://storageprivadospia.blob.core.windows.net/hikvision?sp=racwdli&st=2024-11-19T18:47:55Z&se=2027-11-20T02:47:55Z&sv=2022-11-02&sr=c&sig=SzM2nM6aZf01JPxrmyTozw%2FZDfo7YwbLK1XY9Y9jQ8E%3D"

        # Nome do arquivo a ser lido
        blob_name = name

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
        #print("Conteúdo do arquivo:")
        #rint(conteudo_texto)

        #print("\nDados JSON:")
        #print(data)
        return data.get('dataHora')
    
    def salva_DadosAzure(self, name, cidade, datahora):
        
        # URL SAS do seu contêiner
        sas_url = "https://storageprivadospia.blob.core.windows.net/hikvision?sp=racwdli&st=2024-11-19T18:47:55Z&se=2027-11-20T02:47:55Z&sv=2022-11-02&sr=c&sig=SzM2nM6aZf01JPxrmyTozw%2FZDfo7YwbLK1XY9Y9jQ8E%3D"

        # Nome do arquivo a ser enviado
        blob_name = str(name) + cidade + ".txt"

        # Conteúdo JSON a ser enviado
        data = {
             "dataHora": datahora
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

        #logging.INFO(f"O arquivo {blob_name} foi enviado com sucesso.") #NÃO habilitar pq esta dano erro.
        print(f"O arquivo {blob_name} foi enviado com sucesso.")

    def corrigir_Latlong(self,numero_str):
        # Verifica se é uma string e remove espaços, se necessário
        numero_str = numero_str.strip()
        # Adiciona o ponto decimal após os dois primeiros dígitos
        numero_corrigido_str = numero_str[:3] + "." + numero_str[3:]
        # Converte para float
        return float(numero_corrigido_str)

def main():
    # Lê o arquivo CSV
    local_arquivo =r'C:\Users\SEINT-RS\Documents\python_Exercícios\AB\HikAb\config_hikcenter.csv' #dados acesso
    #local_arquivo = 'https://storageprivadospia.blob.core.windows.net/hikvision/dados_Jardim_Alegre_PR.csv?sp=racwdyti&st=2025-01-21T17:47:21Z&se=2026-06-18T01:47:21Z&sv=2022-11-02&sr=b&sig=xOe0n8h%2BwMUvqHj6%2BgFKlbMZdZOM5tzCy%2FBfPnzdVfU%3D'
    path_dados = local_arquivo
    df = pd.read_csv(path_dados, encoding='UTF-8', delimiter=';')
    # Cria um ThreadPoolExecutor com um número fixo de threads
    max_threads = 7  # Ajuste conforme a capacidade do seu sistema
    executor = ThreadPoolExecutor(max_threads)
 
    while True:
        futures = []
        for _, row in df.iterrows():
            config = row.to_dict()
            camera_processor = CameraProcessor(config)
            # Agendar o processamento de uma câmera
            futures.append(executor.submit(camera_processor.process_camera_once))
           
        for future in as_completed(futures):
            try:
                future.result()  # Isso levantará exceções, se ocorrerem
            except Exception as e:
                print(f"Erro em uma thread: {e}")

        print("Aguardando antes da próxima execução...")
        time.sleep(60)  # Aguarda um intervalo antes de processar novamente

if __name__ == "__main__":
    main()
