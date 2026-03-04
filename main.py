import json
import os

# Importando nossos módulos
from detector_processos import DetectorProcessos
from honeypot_simples import HoneypotSimples
from monitor_recursos import MonitorRecursos
from relatorios import GeradorRelatorios

# Tenta importar colorama para cores (opcional)
try:
    from colorama import Fore, Style, init
    init()
    CORES = True
except ImportError:
    CORES = False
    # Cria classes dummy se colorama não estiver instalado
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = RESET = ''
    class Style:
        BRIGHT = RESET_ALL = ''

class Sentinela:
    def __init__(self):
        self.config = self.carregar_config()
        self.relatorios = GeradorRelatorios()
        
        # Inicializa módulos
        self.detector = DetectorProcessos(self.config)
        self.monitor = MonitorRecursos(self.config)
        self.honeypot = HoneypotSimples(self.config)
        
        self.running = True
        
    def carregar_config(self):
        """Carrega configurações do arquivo JSON"""
        config_padrao = {
            "configuracoes": {
                "nome_sistema": "Sentinela - Sistema de Defesa",
                "versao": "1.0.0",
                "autor": "Usuário",
                "limite_cpu_alerta": 70,
                "intervalo_monitoramento": 5,
                "salvar_logs": True,
                "modo_honeypot": False
            },
            "processos_suspeitos": [
                "miner", "xmr", "coin", "crypto", "pool",
                "hash", "cpuminer", "xmrig", "minerd"
            ],
            "portas_honeypot": [3333, 4444, 5555, 8080]
        }
        
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Cria config padrão
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(config_padrao, f, indent=2, ensure_ascii=False)
                return config_padrao
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
            return config_padrao
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_banner(self):
        """Mostra banner do programa"""
        banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════╗
║                    S E N T I N E L A                     ║
║                Sistema de Defesa Cibernética             ║
║                     v{self.config['configuracoes']['versao']} - Educacional                ║
╚══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """
        print(banner)
    
    def mostrar_menu(self):
        """Mostra menu principal"""
        print(f"\n{Fore.GREEN}MENU PRINCIPAL:{Style.RESET_ALL}")
        print("="*50)
        print("1. 🔍 Escanear Processos Suspeitos")
        print("2. 📊 Monitorar Recursos (30s)")
        print("3. ⏱️  Monitoramento Contínuo (Ctrl+C para parar)")
        print("4. 🚀 Análise Completa Rápida")
        print("5. 📋 Ver Logs Anteriores")
        print("6. ⚙️  Configurações")
        print("7. 🍯 Ativar/Desativar Honeypot")
        print("8. ❓ Ajuda/Sobre")
        print("0. 👋 Sair")
        print("="*50)
    
    def opcao_escanear(self):
        """Opção 1: Escanear processos"""
        self.limpar_tela()
        print(f"\n{Fore.CYAN}🔍 ESCANEANDO PROCESSOS...{Style.RESET_ALL}")
        
        resultado = self.detector.escanear()
        
        print(f"\nTotal de processos: {resultado['total_processos']}")
        
        if resultado['suspeitos']:
            print(f"\n{Fore.RED}🚨 PROCESSOS SUSPEITOS ENCONTRADOS:{Style.RESET_ALL}")
            for i, proc in enumerate(resultado['suspeitos'], 1):
                print(f"\n{i}. {Fore.YELLOW}{proc['nome']}{Style.RESET_ALL}")
                print(f"   PID: {proc['pid']}")
                print(f"   CPU: {proc['cpu']:.1f}%")
                print(f"   Memória: {proc['memoria']:.1f}%")
                print(f"   Razão: {proc['razao']}")
                
                # Pergunta se quer matar
                if i == 1:  # Pergunta apenas no primeiro
                    matar = input(f"\n{Fore.RED}Deseja encerrar algum processo? (s/n): {Style.RESET_ALL}")
                    if matar.lower() == 's':
                        pid = input("Digite o PID: ")
                        sucesso, msg = self.detector.matar_processo(int(pid))
                        print(msg)
        else:
            print(f"\n{Fore.GREEN}✅ Nenhum processo suspeito encontrado{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def opcao_monitorar(self):
        """Opção 2: Monitorar por 30s"""
        self.limpar_tela()
        print(f"\n{Fore.CYAN}📊 INICIANDO MONITORAMENTO (30 segundos)...{Style.RESET_ALL}")
        
        resultado = self.monitor.monitorar(30)
        
        print(f"\n{Fore.GREEN}RESULTADOS:{Style.RESET_ALL}")
        print(f"   CPU Média: {resultado['media_cpu']}%")
        print(f"   Memória Média: {resultado['media_memoria']}%")
        print(f"   Pico de CPU: {resultado['max_cpu']}%")
        print(f"   Alertas: {resultado['alertas']}")
        print(f"   Nível de Risco: {resultado['nivel_risco']}")
        
        # Salva log
        if self.config['configuracoes']['salvar_logs']:
            arquivo = self.relatorios.salvar_log(resultado, "monitoramento")
            print(f"\n📁 Log salvo em: {arquivo}")
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def opcao_continua(self):
        """Opção 3: Monitoramento contínuo"""
        self.limpar_tela()
        print(f"\n{Fore.CYAN}⏱️  MONITORAMENTO CONTÍNUO{Style.RESET_ALL}")
        print("Pressione Ctrl+C para parar\n")
        
        self.monitor.monitoramento_continuo(5)
    
    def opcao_analise_completa(self):
        """Opção 4: Análise completa rápida"""
        self.limpar_tela()
        print(f"\n{Fore.MAGENTA}🚀 INICIANDO ANÁLISE COMPLETA...{Style.RESET_ALL}")
        
        # 1. Escaneia processos
        print("\n1. Verificando processos...")
        processos = self.detector.escanear()
        
        # 2. Monitora por 15 segundos
        print("2. Monitorando recursos...")
        monitor = self.monitor.monitorar(15)
        
        # 3. Gera relatório
        print("3. Gerando relatório...")
        estatisticas = self.honeypot.get_estatisticas() if self.config['configuracoes']['modo_honeypot'] else None
        
        relatorio = self.relatorios.gerar_relatorio_texto(
            monitor, 
            processos['suspeitos'],
            estatisticas
        )
        
        print("\n" + "="*60)
        print(relatorio)
        
        # Salva relatório
        if self.config['configuracoes']['salvar_logs']:
            dados_completos = {
                'processos': processos,
                'monitoramento': monitor,
                'honeypot': estatisticas
            }
            arquivo = self.relatorios.salvar_log(dados_completos, "analise_completa")
            print(f"\n📁 Relatório salvo em: {arquivo}")
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def opcao_logs(self):
        """Opção 5: Ver logs anteriores"""
        self.limpar_tela()
        print(f"\n{Fore.CYAN}📋 LOGS ANTERIORES{Style.RESET_ALL}")
        
        logs = self.relatorios.listar_logs_anteriores()
        
        if not logs:
            print("\nNenhum log encontrado.")
            input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"\nLogs disponíveis:")
        for i, log in enumerate(logs[:10], 1):  # Mostra últimos 10
            print(f"{i}. {log}")
        
        escolha = input("\nDigite o número do log para ver (Enter para voltar): ")
        
        if escolha.isdigit():
            idx = int(escolha) - 1
            if 0 <= idx < len(logs):
                dados = self.relatorios.carregar_log(logs[idx])
                if dados:
                    print(f"\n{Fore.YELLOW}CONTEÚDO DO LOG:{Style.RESET_ALL}")
                    print(json.dumps(dados, indent=2, ensure_ascii=False)[:1000])  # Mostra primeiros 1000 chars
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def opcao_config(self):
        """Opção 6: Configurações"""
        self.limpar_tela()
        print(f"\n{Fore.CYAN}⚙️  CONFIGURAÇÕES{Style.RESET_ALL}")
        
        print(f"\nConfigurações atuais:")
        for chave, valor in self.config['configuracoes'].items():
            print(f"   {chave}: {valor}")
        
        print(f"\nProcessos suspeitos monitorados:")
        for p in self.config['processos_suspeitos'][:5]:
            print(f"   • {p}")
        
        alterar = input(f"\n{Fore.YELLOW}Deseja alterar o limite de CPU? (s/n): {Style.RESET_ALL}")
        
        if alterar.lower() == 's':
            novo_limite = input("Novo limite (%): ")
            try:
                self.config['configuracoes']['limite_cpu_alerta'] = int(novo_limite)
                self.monitor.limite_cpu = int(novo_limite)
                
                # Salva config
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                
                print(f"{Fore.GREEN}Configuração atualizada!{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Valor inválido{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def opcao_honeypot(self):
        """Opção 7: Ativar/Desativar Honeypot"""
        self.limpar_tela()
        print(f"\n{Fore.CYAN}🍯 HONEYPOT{Style.RESET_ALL}")
        
        estado_atual = self.config['configuracoes']['modo_honeypot']
        print(f"Status atual: {'ATIVADO' if estado_atual else 'DESATIVADO'}")
        
        print(f"\n{Fore.YELLOW}ATENÇÃO: Honeypot atrai conexões para estudo.{Style.RESET_ALL}")
        print("Use apenas em sua própria rede!")
        
        if not estado_atual:
            ativar = input("Ativar honeypot? (s/n): ")
            if ativar.lower() == 's':
                self.config['configuracoes']['modo_honeypot'] = True
                self.honeypot = HoneypotSimples(self.config)
                self.honeypot.iniciar()
                
                # Salva config
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
        else:
            desativar = input("Desativar honeypot? (s/n): ")
            if desativar.lower() == 's':
                self.config['configuracoes']['modo_honeypot'] = False
                self.honeypot.parar()
                
                # Salva config
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def opcao_ajuda(self):
        """Opção 8: Ajuda"""
        self.limpar_tela()
        print(f"\n{Fore.CYAN}❓ AJUDA E SOBRE{Style.RESET_ALL}")
        print("="*60)
        print(f"\n{Fore.GREEN}SENTINELA - Sistema de Defesa Cibernética{Style.RESET_ALL}")
        print(f"Versão: {self.config['configuracoes']['versao']}")
        print(f"\n{Fore.YELLOW}O que este programa faz?{Style.RESET_ALL}")
        print("   • Detecta processos suspeitos de mineração")
        print("   • Monitora uso de CPU e memória")
        print("   • Gera alertas de atividade anormal")
        print("   • Salva logs para análise posterior")
        print("   • Simula servidores vulneráveis (honeypot)")
        
        print(f"\n{Fore.YELLOW}Como usar:{Style.RESET_ALL}")
        print("   1. Comece com uma análise completa (opção 4)")
        print("   2. Monitore processos suspeitos regularmente")
        print("   3. Verifique os logs para padrões")
        print("   4. Ajuste as configurações conforme necessário")
        
        print(f"\n{Fore.YELLOW}Aviso Legal:{Style.RESET_ALL}")
        print("   Este programa é EDUCACIONAL. Use apenas")
        print("   em seus próprios sistemas para aprendizado.")
        
        print(f"\n{Fore.GREEN}Bons estudos! 🚀{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def executar(self):
        """Loop principal do programa"""
        try:
            # Inicia honeypot se configurado
            if self.config['configuracoes']['modo_honeypot']:
                self.honeypot.iniciar()
            
            while self.running:
                self.limpar_tela()
                self.mostrar_banner()
                self.mostrar_menu()
                
                opcao = input(f"\n{Fore.GREEN}Escolha uma opção: {Style.RESET_ALL}")
                
                if opcao == '1':
                    self.opcao_escanear()
                elif opcao == '2':
                    self.opcao_monitorar()
                elif opcao == '3':
                    self.opcao_continua()
                elif opcao == '4':
                    self.opcao_analise_completa()
                elif opcao == '5':
                    self.opcao_logs()
                elif opcao == '6':
                    self.opcao_config()
                elif opcao == '7':
                    self.opcao_honeypot()
                elif opcao == '8':
                    self.opcao_ajuda()
                elif opcao == '0':
                    print(f"\n{Fore.YELLOW}Encerrando Sentinela...{Style.RESET_ALL}")
                    if self.config['configuracoes']['modo_honeypot']:
                        self.honeypot.parar()
                    self.running = False
                else:
                    print(f"{Fore.RED}Opção inválida!{Style.RESET_ALL}")
                    input("Pressione Enter para continuar...")
                    
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Programa interrompido pelo usuário{Style.RESET_ALL}")
            if self.config['configuracoes']['modo_honeypot']:
                self.honeypot.parar()

# Ponto de entrada do programa
if __name__ == "__main__":
    sentinela = Sentinela()
    sentinela.executar()