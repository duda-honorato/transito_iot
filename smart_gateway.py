import socket
import struct
import threading
import time
from datetime import datetime
from shared.config import (
    UDP_PORT_GATEWAY, UDP_HOST_GATEWAY,
    TCP_HOST_NUVEM, TCP_PORT_NUVEM,
    MULTICAST_GROUP, MULTICAST_PORT,
    LIMITE_VELOCIDADE, ID_GATEWAY
)

class SmartGateway:
    def __init__(self):
        # UDP socket para receber sensores
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.bind((UDP_HOST_GATEWAY, UDP_PORT_GATEWAY))
        
        # TCP socket para enviar à nuvem
        self.tcp_sock = None
        self.conectar_nuvem()
        
        # Multicast socket para enviar alertas
        self.multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        
        self.ultimo_alerta = {}  # controle de frequência de alertas
        print("✅ SmartGateway inicializado")
        
    def conectar_nuvem(self):
        """Estabelece conexão TCP com servidor na nuvem"""
        try:
            self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_sock.connect((TCP_HOST_NUVEM, TCP_PORT_NUVEM))
            print(f"📡 Conectado ao servidor nuvem em {TCP_HOST_NUVEM}:{TCP_PORT_NUVEM}")
        except Exception as e:
            print(f"⚠️ Erro ao conectar nuvem: {e}")
            self.tcp_sock = None
            
    def enviar_para_nuvem(self, id_radar, velocidade, status):
        """Envia infração via TCP para nuvem"""
        if not self.tcp_sock:
            self.conectar_nuvem()
            if not self.tcp_sock:
                return False
                
        timestamp = datetime.now().isoformat()
        # Formato: INFRACAO;<id_gateway>;<id_radar>;<velocidade>;<limite_via>;<timestamp>;<status>
        mensagem = f"INFRACAO;{ID_GATEWAY};{id_radar};{velocidade};{LIMITE_VELOCIDADE};{timestamp};{status}"
        
        try:
            self.tcp_sock.send(mensagem.encode())
            # Aguarda ACK
            ack = self.tcp_sock.recv(1024).decode()
            print(f"☁️ Nuvem ACK: {ack}")
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar para nuvem: {e}")
            self.tcp_sock = None
            return False
    
    def enviar_alerta_multicast(self, velocidade, status):
        """Envia alerta multicast para atuadores locais"""
        if status == "ALERTA":
            # Mensagem para Painel
            msg_painel = f"ALERTA;EXCESSO;{velocidade};REDUZA A VELOCIDADE"
            # Mensagem para Display
            msg_display = f"DISPLAY;{velocidade};{LIMITE_VELOCIDADE};REDUZA"
            
            try:
                # Envia via multicast
                self.multicast_sock.sendto(msg_painel.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
                self.multicast_sock.sendto(msg_display.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
                print(f"📢 MULTICAST enviado: {msg_painel}")
                print(f"📢 MULTICAST enviado: {msg_display}")
            except Exception as e:
                print(f"❌ Erro no multicast: {e}")
    
    def processar_mensagem_radar(self, dados):
        """Processa mensagem do radar"""
        # Formato: RADAR;id_radar;velocidade;timestamp
        partes = dados.split(';')
        if len(partes) >= 4 and partes[0] == "RADAR":
            id_radar = partes[1]
            velocidade = int(partes[2])
            timestamp = partes[3]
            
            status = "ALERTA" if velocidade > LIMITE_VELOCIDADE else "NORMAL"
            
            print(f"\n🚗 [RADAR] Velocidade: {velocidade} km/h | Limite: {LIMITE_VELOCIDADE} km/h | Status: {status}")
            
            if status == "ALERTA":
                # Evita spam de alertas para mesma velocidade
                if id_radar not in self.ultimo_alerta or time.time() - self.ultimo_alerta[id_radar] > 10:
                    self.ultimo_alerta[id_radar] = time.time()
                    # Envia para nuvem
                    self.enviar_para_nuvem(id_radar, velocidade, status)
                    # Envia multicast para atuadores
                    self.enviar_alerta_multicast(velocidade, status)
            return status
        return None
    
    def processar_mensagem_fluxo(self, dados):
        """Processa mensagem do sensor de fluxo"""
        # Formato: FLUXO;id_sensor;qtde;periodo;timestamp
        partes = dados.split(';')
        if len(partes) >= 5 and partes[0] == "FLUXO":
            id_sensor = partes[1]
            qtde = int(partes[2])
            periodo = int(partes[3])
            print(f"🚦 [FLUXO] {qtde} veículos nos últimos {periodo}s | Sensor: {id_sensor}")
            return {"id": id_sensor, "qtde": qtde, "periodo": periodo}
        return None
    
    def executar(self):
        """Loop principal do gateway"""
        print("🟢 SmartGateway rodando - aguardando sensores...")
        print(f"   UDP porta {UDP_PORT_GATEWAY} | Multicast grupo {MULTICAST_GROUP}:{MULTICAST_PORT}")
        
        try:
            while True:
                data, addr = self.udp_sock.recvfrom(2048)
                mensagem = data.decode()
                
                # Tenta processar como radar ou fluxo
                if mensagem.startswith("RADAR"):
                    self.processar_mensagem_radar(mensagem)
                elif mensagem.startswith("FLUXO"):
                    self.processar_mensagem_fluxo(mensagem)
                else:
                    print(f"⚠️ Mensagem desconhecida: {mensagem}")
                    
        except KeyboardInterrupt:
            print("\n🔴 SmartGateway encerrado")
            self.udp_sock.close()
            if self.tcp_sock:
                self.tcp_sock.close()
            self.multicast_sock.close()
          
if __name__ == "__main__":
    gateway = SmartGateway()
    gateway.executar()
