import socket
import struct
from shared.config import MULTICAST_GROUP, MULTICAST_PORT

class PainelMensagem:
    def __init__(self, nome="PMV-01"):
        self.nome = nome
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', MULTICAST_PORT))
        
        # Inscreve no grupo multicast
        mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        print(f"🪧 Painel {self.nome} inscrito no grupo {MULTICAST_GROUP}:{MULTICAST_PORT}")
        
    def executar(self):
        print(f"🟢 {self.nome} aguardando mensagens...")
        
        try:
            while True:
                data, addr = self.sock.recvfrom(1024)
                mensagem = data.decode()
                
                if mensagem.startswith("ALERTA"):
                    # Formato: ALERTA;tipo_evento;velocidade;mensagem
                    partes = mensagem.split(';')
                    if len(partes) >= 4:
                        tipo = partes[1]
                        velocidade = partes[2]
                        texto = partes[3]
                        
                        print("\n" + "="*50)
                        print(f"🪧 [PAINEL {self.nome}]")
                        if tipo == "EXCESSO":
                            print(f"   ⚠️ {texto} ⚠️")
                            print(f"   Velocidade detectada: {velocidade} km/h")
                        else:
                            print(f"   ℹ️ {texto}")
                        print("="*50)
                        
        except KeyboardInterrupt:
            print(f"\n🔴 Painel {self.nome} encerrado")
            self.sock.close()

if __name__ == "__main__":
    painel = PainelMensagem("PMV-01")
    painel.executar()
