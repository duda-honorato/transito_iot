import socket 
import time
import random
from datetime import datetime
from shared.config import UDP_HOST_GATEWAY, UDP_PORT_GATEWAY

class SensorRadar:
    def __init__(self, id_sensor="R01"):
        self.id_sensor = id_sensor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.gateway_addr = (UDP_HOST_GATEWAY, UDP_PORT_GATEWAY)
        
    def gerar_velocidade(self):
        # Simula leitura de radar: entre 40 e 120 km/h
        return random.randint(40, 120)
    
    def enviar_leitura(self):
        velocidade = self.gerar_velocidade()
        timestamp = datetime.now().isoformat()
        # Formato: RADAR;<id_radar>;<velocidade>;<timestamp>
        mensagem = f"RADAR;{self.id_sensor};{velocidade};{timestamp}"
        
        self.sock.sendto(mensagem.encode(), self.gateway_addr)
        print(f"[RADAR {self.id_sensor}] Enviado: {velocidade} km/h às {timestamp}")
        
    def executar(self, intervalo=2):
        print(f"🟢 Sensor Radar {self.id_sensor} iniciado (UDP cliente)")
        try:
            while True:
                self.enviar_leitura()
                time.sleep(intervalo)
        except KeyboardInterrupt:
            print(f"\n🔴 Sensor Radar {self.id_sensor} encerrado")
            self.sock.close()

if __name__ == "__main__":
    radar = SensorRadar("R01")
    radar.executar()
