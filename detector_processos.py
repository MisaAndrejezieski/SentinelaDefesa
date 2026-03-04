import psutil


class DetectorProcessos:
    def __init__(self, config):
        self.config = config
        self.processos_suspeitos = config.get('processos_suspeitos', [])
        self.historico = []
        
    def escanear(self):
        """Escaneia processos em execução"""
        suspeitos = []
        todos_processos = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                nome = info['name'].lower() if info['name'] else ''
                
                # Registra todos processos
                todos_processos.append({
                    'pid': info['pid'],
                    'nome': info['name'],
                    'cpu': info['cpu_percent'] or 0,
                    'memoria': info['memory_percent'] or 0
                })
                
                # Verifica nomes suspeitos
                for padrao in self.processos_suspeitos:
                    if padrao in nome:
                        suspeitos.append({
                            'pid': info['pid'],
                            'nome': info['name'],
                            'cpu': info['cpu_percent'] or 0,
                            'memoria': info['memory_percent'] or 0,
                            'razao': f'Nome contém "{padrao}"'
                        })
                        break
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return {
            'total_processos': len(todos_processos),
            'suspeitos': suspeitos,
            'todos': todos_processos
        }
    
    def matar_processo(self, pid):
        """Mata um processo suspeito (com confirmação)"""
        try:
            proc = psutil.Process(pid)
            nome = proc.name()
            
            print(f"⚠️ Processo: {nome} (PID: {pid})")
            confirmar = input("Deseja encerrar este processo? (s/n): ")
            
            if confirmar.lower() == 's':
                proc.terminate()
                return True, f"Processo {nome} encerrado"
            else:
                return False, "Operação cancelada"
                
        except Exception as e:
            return False, f"Erro: {e}"