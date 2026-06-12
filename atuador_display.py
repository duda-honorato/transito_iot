import socket
import struct
from shared.config import MULTICAST_GROUP, MULTICAST_PORT

class DisplayVelocidade:
    def __init__(self, nome="DISP-01"):
        self.nome = nome
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', MULTICAST_PORT))
        
        mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        print(f"📟 Display {self.nome} inscrito no grupo {MULTICAST_GROUP}:{MULTICAST_PORT}")
        
    def executar(self):
        print(f"🟢 {self.nome} aguardando mensagens...")
        
        try:
            while True:
                data, addr = self.sock.recvfrom(1024)
                mensagem = data.decode()
                
                if mensagem.startswith("DISPLAY"):
                    # Formato: DISPLAY;velocidade;limite;mensagem_alerta
                    partes = mensagem.split(';')
                    if len(partes) >= 4:
                        velocidade = partes[1]
                        limite = partes[2]
                        alerta = partes[3]
                        
                        print("\n" + "┌" + "─"*38 + "┐")
                        print(f"│ 📟 {self.nome}") 
                        print(f"│ SUA VELOCIDADE: {velocidade} km/h")
                        print(f"│ LIMITE: {limite} km/h")
                        print(f"│ ⚠️ {alerta} ⚠️")
                        print("└" + "─"*38 + "┘")
                        
        except KeyboardInterrupt:
            print(f"\n🔴 Display {self.nome} encerrado")
            self.sock.close()

if __name__ == "__main__":
    display = DisplayVelocidade("DISP-01")
    display.executar()
