import json
import os
from datetime import datetime


class GeradorRelatorios:
    def __init__(self):
        self.relatorios_path = "logs"
        if not os.path.exists(self.relatorios_path):
            os.makedirs(self.relatorios_path)
    
    def salvar_log(self, dados, tipo="monitoramento"):
        """Salva dados em arquivo JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{self.relatorios_path}/{tipo}_{timestamp}.json"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        return nome_arquivo
    
    def gerar_relatorio_texto(self, dados_monitoramento, processos_suspeitos, estatisticas_honeypot=None):
        """Gera relatório formatado"""
        relatorio = []
        
        # Cabeçalho
        relatorio.append("="*60)
        relatorio.append("RELATÓRIO DO SENTINELA".center(60))
        relatorio.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}".center(60))
        relatorio.append("="*60)
        
        # Resumo do Monitoramento
        if dados_monitoramento:
            relatorio.append("\n📊 RESUMO DO MONITORAMENTO:")
            relatorio.append(f"   • CPU Média: {dados_monitoramento['media_cpu']}%")
            relatorio.append(f"   • Memória Média: {dados_monitoramento['media_memoria']}%")
            relatorio.append(f"   • Pico de CPU: {dados_monitoramento['max_cpu']}%")
            relatorio.append(f"   • Alertas Gerados: {dados_monitoramento['alertas']}")
            relatorio.append(f"   • Nível de Risco: {dados_monitoramento['nivel_risco']}")
        
        # Processos Suspeitos
        if processos_suspeitos:
            relatorio.append("\n🚨 PROCESSOS SUSPEITOS ENCONTRADOS:")
            for p in processos_suspeitos:
                relatorio.append(f"   • {p['nome']} (PID: {p['pid']}) - CPU: {p['cpu']}%")
                relatorio.append(f"     Razão: {p['razao']}")
        else:
            relatorio.append("\n✅ Nenhum processo suspeito encontrado")
        
        # Honeypot
        if estatisticas_honeypot:
            relatorio.append("\n🍯 ESTATÍSTICAS DO HONEYPOT:")
            relatorio.append(f"   • Total de tentativas: {estatisticas_honeypot['total_ataques']}")
            relatorio.append(f"   • IPs únicos: {estatisticas_honeypot['ips_unicos']}")
        
        # Recomendações
        relatorio.append("\n🛡️ RECOMENDAÇÕES DE SEGURANÇA:")
        relatorio.append("   1. Mantenha o Windows e antivírus atualizados")
        relatorio.append("   2. Use uBlock Origin no navegador")
        relatorio.append("   3. Evite sites desconhecidos")
        relatorio.append("   4. Monitore uso de CPU regularmente")
        relatorio.append("   5. Desconfie de emails com anexos")
        
        relatorio.append("\n" + "="*60)
        
        return "\n".join(relatorio)
    
    def listar_logs_anteriores(self):
        """Lista logs salvos"""
        if not os.path.exists(self.relatorios_path):
            return []
        
        arquivos = os.listdir(self.relatorios_path)
        logs = [f for f in arquivos if f.endswith('.json')]
        return sorted(logs, reverse=True)
    
    def carregar_log(self, nome_arquivo):
        """Carrega um log específico"""
        caminho = os.path.join(self.relatorios_path, nome_arquivo)
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None