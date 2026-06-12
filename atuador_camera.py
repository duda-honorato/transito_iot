import socket
import struct
from datetime import datetime
from shared.config import MULTICAST_GROUP, MULTICAST_PORT

class CameraInteligente:
    def __init__(self, nome="CAM-01"):
        self.nome = nome
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', MULTICAST_PORT))
        
        mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        print(f"📷 Câmera {self.nome} inscrita no grupo {MULTICAST_GROUP}:{MULTICAST_PORT}")
        
    def registrar_ocorrencia(self, velocidade, mensagem):
        """Simula registro de imagem/vídeo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"ocorrencia_{timestamp}_{velocidade}kmh.txt"
        
        with open(nome_arquivo, "w") as f:
            f.write(f"Ocorrência registrada pela {self.nome}\n")
            f.write(f"Velocidade: {velocidade} km/h\n")
            f.write(f"Mensagem: {mensagem}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        
        print(f"📸 [CÂMERA] Ocorrência salva em {nome_arquivo}")
        return nome_arquivo
        
    def executar(self):
        print(f"🟢 {self.nome} aguardando eventos...")
        
        try:
            while True:
                data, addr = self.sock.recvfrom(1024)
                mensagem = data.decode()
                
                if mensagem.startswith("ALERTA"):
                    partes = mensagem.split(';')
                    if len(partes) >= 4:
                        tipo = partes[1]
                        velocidade = partes[2]
                        texto = partes[3]
                        
                        print(f"\n📹 [CÂMERA {self.nome}] Evento detectado!")
                        print(f"   Tipo: {tipo} | Velocidade: {velocidade} km/h")
                        
                        # Registra a ocorrência
                        self.registrar_ocorrencia(velocidade, texto)
                        
        except KeyboardInterrupt:
            print(f"\n🔴 Câmera {self.nome} encerrada")
            self.sock.close()

if __name__ == "__main__":
    camera = CameraInteligente("CAM-01")
    camera.executar()
