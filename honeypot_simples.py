import socket
import threading
from datetime import datetime


class HoneypotSimples:
    def __init__(self, config):
        self.config = config
        self.portas = config.get('portas_honeypot', [3333, 4444, 5555])
        self.ataques = []
        self.ativo = False
        
    def iniciar(self):
        """Inicia o honeypot (apenas se configurado)"""
        if not self.config['configuracoes']['modo_honeypot']:
            print("🔒 Honeypot desativado na configuração")
            return
            
        self.ativo = True
        print("\n🍯 Iniciando Honeypot Educacional...")
        
        for porta in self.portas:
            thread = threading.Thread(target=self._simular_servidor, args=(porta,))
            thread.daemon = True
            thread.start()
            print(f"   ✅ Monitorando porta {porta}")
    
    def _simular_servidor(self, porta):
        """Simula um servidor vulnerável"""
        try:
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind(('0.0.0.0', porta))
            servidor.listen(5)
            
            while self.ativo:
                try:
                    cliente, endereco = servidor.accept()
                    
                    # Registra tentativa
                    ataque = {
                        'timestamp': datetime.now().isoformat(),
                        'ip': endereco[0],
                        'porta': porta,
                        'tipo': 'conexao_detectada'
                    }
                    
                    self.ataques.append(ataque)
                    print(f"\n🚨 Tentativa de conexão detectada de {endereco[0]}:{porta}")
                    
                    cliente.close()
                    
                except:
                    pass
                    
        except Exception as e:
            if self.ativo:
                print(f"   ⚠️ Erro na porta {porta}: {e}")
    
    def parar(self):
        """Para o honeypot"""
        self.ativo = False
        print("🛑 Honeypot encerrado")
    
    def get_estatisticas(self):
        """Retorna estatísticas do honeypot"""
        ips_unicos = set(a['ip'] for a in self.ataques)
        return {
            'total_ataques': len(self.ataques),
            'ips_unicos': len(ips_unicos),
            'portas_atingidas': len(set(a['porta'] for a in self.ataques)),
            'ultimos_ataques': self.ataques[-5:] if self.ataques else []
        }