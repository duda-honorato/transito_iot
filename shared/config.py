#Conf do sistema IOT de transito

#UDP - Sensores de Gateway 
UPD_POR_GATEWAY = 5000
UDP_HOST_GATEWAY = "127.0.0.1"  # Local para simulação

#TCP - Gateway para Nuvem
TCP_PORT_NUVEM = 9100
TCP_HOST_NUVEM = "127.0.0.1"

#Multicast - Gateway para Atuadores
MULTICAST_GROUP = "239.10.10.1"
MULTICAST_PORT = 6500

#Conf da Via
LIMITE_VELOCIDADE = 80 #km/h
ID_GATEWAY = "GW01"

#Caminho p banco de dados local (simulação)
DB_FILE = "infracoes.db"
