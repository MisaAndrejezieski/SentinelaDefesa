import time
from datetime import datetime

import psutil


class MonitorRecursos:
    def __init__(self, config):
        self.config = config
        self.limite_cpu = config['configuracoes']['limite_cpu_alerta']
        self.historico_cpu = []
        self.historico_memoria = []
        self.alertas = []
        
    def monitorar(self, duracao=30):
        """Monitora recursos do sistema"""
        print(f"\n📊 Monitorando sistema por {duracao} segundos...")
        print(f"Limite de alerta: {self.limite_cpu}% CPU")
        
        self.historico_cpu = []
        self.historico_memoria = []
        
        for i in range(duracao):
            # Coleta dados
            cpu = psutil.cpu_percent(interval=1)
            memoria = psutil.virtual_memory().percent
            
            self.historico_cpu.append(cpu)
            self.historico_memoria.append(memoria)
            
            # Verifica alertas
            if cpu > self.limite_cpu:
                alerta = {
                    'timestamp': datetime.now().isoformat(),
                    'tipo': 'CPU_ALTA',
                    'valor': cpu,
                    'limite': self.limite_cpu
                }
                self.alertas.append(alerta)
                print(f"   ⚠️ ALERTA: CPU em {cpu}%")
            
            # Progresso
            if i % 5 == 0:
                print(f"   Progresso: {i}/{duracao} segundos")
        
        return self.analisar_dados()
    
    def analisar_dados(self):
        """Analisa os dados coletados"""
        if not self.historico_cpu:
            return None
            
        media_cpu = sum(self.historico_cpu) / len(self.historico_cpu)
        media_memoria = sum(self.historico_memoria) / len(self.historico_memoria)
        max_cpu = max(self.historico_cpu)
        picos = sum(1 for cpu in self.historico_cpu if cpu > self.limite_cpu)
        
        # Classifica o risco
        if media_cpu > 80 or picos > len(self.historico_cpu) * 0.5:
            risco = "CRÍTICO"
        elif media_cpu > 60 or picos > len(self.historico_cpu) * 0.3:
            risco = "ALTO"
        elif media_cpu > 40 or picos > len(self.historico_cpu) * 0.1:
            risco = "MÉDIO"
        else:
            risco = "BAIXO"
        
        return {
            'media_cpu': round(media_cpu, 1),
            'media_memoria': round(media_memoria, 1),
            'max_cpu': max_cpu,
            'picos': picos,
            'total_amostras': len(self.historico_cpu),
            'alertas': len(self.alertas),
            'nivel_risco': risco,
            'timestamp': datetime.now().isoformat()
        }
    
    def monitoramento_continuo(self, intervalo=5):
        """Monitoramento em tempo real"""
        try:
            while True:
                cpu = psutil.cpu_percent(interval=1)
                memoria = psutil.virtual_memory().percent
                
                # Mostra barra de progresso simples
                barra_cpu = '█' * int(cpu / 5) + '░' * (20 - int(cpu / 5))
                barra_mem = '█' * int(memoria / 5) + '░' * (20 - int(memoria / 5))
                
                print(f"\rCPU: [{barra_cpu}] {cpu:3.0f}% | MEM: [{barra_mem}] {memoria:3.0f}%", end='')
                
                time.sleep(intervalo - 1)  # Ajusta pelo 1 segundo do cpu_percent
                
        except KeyboardInterrupt:
            print("\n\n✅ Monitoramento encerrado")