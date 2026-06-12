import socket
import threading
import sqlite3
from datetime import datetime
from shared.config import TCP_HOST_NUVEM, TCP_PORT_NUVEM, DB_FILE

class ServidorNuvem:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind((TCP_HOST_NUVEM, TCP_PORT_NUVEM))
        self.server_sock.listen(5)
        self.init_banco()
        print(f"☁️ Servidor Nuvem rodando em {TCP_HOST_NUVEM}:{TCP_PORT_NUVEM}")
        
    def init_banco(self):
        """Inicializa banco de dados SQLite"""
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS infracoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_evento TEXT,
                id_gateway TEXT,
                id_radar TEXT,
                velocidade INTEGER,
                limite_via INTEGER,
                timestamp TEXT,
                status TEXT,
                data_registro TEXT
            )
        ''')
        self.conn.commit()
        print("🗄️ Banco de dados inicializado")
        
    def salvar_infracao(self, dados):
        """Salva infração no banco"""
        # Formato: INFRACAO;id_gateway;id_radar;velocidade;limite_via;timestamp;status
        partes = dados.split(';')
        if len(partes) >= 7 and partes[0] == "INFRACAO":
            id_evento = f"EVT{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            id_gateway = partes[1]
            id_radar = partes[2]
            velocidade = int(partes[3])
            limite_via = int(partes[4])
            timestamp = partes[5]
            status = partes[6]
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO infracoes (id_evento, id_gateway, id_radar, velocidade, limite_via, timestamp, status, data_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (id_evento, id_gateway, id_radar, velocidade, limite_via, timestamp, status, datetime.now().isoformat()))
            self.conn.commit()
            
            print(f"💾 Infração salva: {id_evento} | {velocidade} km/h | Status: {status}")
            return id_evento
        return None
    
    def tratar_cliente(self, client_sock, addr):
        """Trata conexão de um SmartGateway"""
        print(f"🔗 Conexão estabelecida com {addr}")
        
        try:
            while True:
                data = client_sock.recv(2048)
                if not data:
                    break
                    
                mensagem = data.decode()
                print(f"📨 Recebido de {addr}: {mensagem[:80]}...")
                
                # Salva no banco
                id_evento = self.salvar_infracao(mensagem)
                
                # Envia ACK
                if id_evento:
                    ack = f"ACK;{id_evento};OK;Registro salvo com sucesso"
                else:
                    ack = f"ACK;ERRO;ERRO;Formato inválido"
                    
                client_sock.send(ack.encode())
                print(f"📤 Enviado ACK para {addr}")
                
        except Exception as e:
            print(f"❌ Erro com cliente {addr}: {e}")
        finally:
            client_sock.close()
            print(f"🔌 Conexão fechada com {addr}")
    
    def executar(self):
        """Aceita conexões em loop"""
        print("🟢 Servidor aguardando SmartGateways...")
        
        try:
            while True:
                client_sock, addr = self.server_sock.accept()
                thread = threading.Thread(target=self.tratar_cliente, args=(client_sock, addr))
                thread.daemon = True
                thread.start()
                print(f"📊 Threads ativas: {threading.active_count() - 1}")
                
        except KeyboardInterrupt:
            print("\n🔴 Servidor Nuvem encerrado")
            self.server_sock.close()
            self.conn.close()

def dashboard_simples():
    """Simula Dashboard Web - exibe últimas infrações"""
    import time
    while True:
        time.sleep(15)
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id_evento, velocidade, timestamp, status 
                FROM infracoes 
                ORDER BY id DESC LIMIT 5
            ''')
            print("\n" + "="*60)
            print("📊 DASHBOARD TRÂNSITO - Últimas infrações:")
            print("="*60)
            for row in cursor.fetchall():
                print(f"  🚨 Evento: {row[0]} | Velocidade: {row[1]} km/h | Data: {row[2]} | Status: {row[3]}")
            conn.close()
        except:
            pass

if __name__ == "__main__":
    servidor = ServidorNuvem()
    
    # Thread para dashboard
    dashboard_thread = threading.Thread(target=dashboard_simples, daemon=True)
    dashboard_thread.start()
    
    servidor.executar()
