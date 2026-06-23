import os
import sys
from datetime import datetime

# ============================================================
# Mission Control AI - Sistema de Monitoramento
# GS2026.1 - Pensamento Computacional e Automação com Python
# Tema: Soluções em Energias Renováveis e Sustentáveis
# ============================================================

NOME_MISSAO = "Missão Hélio-1"
NOME_EQUIPE  = "Solução do multiverso"

# Cores no terminal
RESET    = "\033[0m"
BOLD     = "\033[1m"
VERMELHO = "\033[31m"
VERDE    = "\033[32m"
AMARELO  = "\033[33m"
CIANO    = "\033[36m"
BRANCO   = "\033[37m"
MAGENTA  = "\033[35m"

# Constantes de nível
NORMAL  = 0
ATENCAO = 1
CRITICO = 2

# Áreas monitoradas — todas ligadas ao sistema de energia renovável da missão
areas = [
    "Temperatura dos painéis solares",
    "Comunicação com a base",
    "Carga das baterias de íon-lítio",
    "Suporte de oxigênio",
    "Estabilidade operacional",
]

# Variáveis globais
dados_atuais = {
    "temperatura":  25.0,
    "comunicacao":  1,
    "bateria":      100.0,
    "oxigenio":     100.0,
    "estabilidade": 100.0,
}
historico           = []
pontos_acumulados   = [0, 0, 0, 0, 0]
energia_gerada_kwh  = []   # kWh gerado por ciclo (calculado a partir da bateria)

# ============================================================
# FUNÇÕES AUXILIARES DE INTERFACE
# ============================================================

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def cabecalho():
    print(CIANO + BOLD)
    print("╔══════════════════════════════════════════════════════╗")
    print("║   MISSION CONTROL — ENERGIA SOLAR ESPACIAL           ║")
    print("║   GS2026.1 · Pensamento Computacional com Python     ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(RESET, end="")
    print(f"  Missão : {NOME_MISSAO}   |   Equipe : {NOME_EQUIPE}")
    print(f"  Data   : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print()

def cor_nivel(nivel, texto):
    if nivel == CRITICO:
        return VERMELHO + BOLD + texto + RESET
    elif nivel == ATENCAO:
        return AMARELO + texto + RESET
    else:
        return VERDE + texto + RESET

def barra_progresso(valor, maximo=100, tamanho=20):
    """Retorna uma barra visual de progresso."""
    preenchido = int((valor / maximo) * tamanho)
    barra = "█" * preenchido + "░" * (tamanho - preenchido)
    return f"[{barra}] {valor:.1f}%"

# ============================================================
# FUNÇÕES DE ANÁLISE — com contexto de energia renovável
# ============================================================

def analisar_temperatura(v):
    """
    Painéis solares operam de forma ideal entre 15°C e 35°C.
    Temperaturas extremas reduzem a eficiência fotovoltaica.
    """
    if v < 10:
        return ATENCAO, 1, "Temperatura baixa — eficiência solar reduzida"
    elif v <= 35:
        return NORMAL, 0, "Temperatura ideal para captação solar"
    elif v <= 45:
        return ATENCAO, 1, "Temperatura elevada — perda de rendimento fotovoltaico"
    else:
        return CRITICO, 2, "Superaquecimento — risco de dano aos painéis solares"

def analisar_comunicacao(v):
    if v == 1:
        return NORMAL, 0, "Comunicação ativa com a base"
    else:
        return CRITICO, 2, "Falha de comunicação"

def analisar_bateria(v):
    """
    Baterias de íon-lítio armazenam energia captada pelos painéis.
    Abaixo de 20% ativa modo de emergência para preservar sistemas essenciais.
    """
    if v < 20:
        return CRITICO, 2, "Bateria crítica — captação solar insuficiente"
    elif v < 50:
        return ATENCAO, 1, "Bateria baixa — monitorar painéis solares"
    else:
        return NORMAL, 0, "Energia armazenada em nível seguro"

def analisar_oxigenio(v):
    if v < 80:
        return CRITICO, 2, "Oxigênio em nível crítico"
    elif v < 90:
        return ATENCAO, 1, "Oxigênio abaixo do ideal"
    else:
        return NORMAL, 0, "Oxigênio adequado"

def analisar_estabilidade(v):
    if v < 40:
        return CRITICO, 2, "Estabilidade operacional crítica"
    elif v < 70:
        return ATENCAO, 1, "Estabilidade operacional reduzida"
    else:
        return NORMAL, 0, "Estabilidade operacional adequada"

def calcular_eficiencia_solar(temperatura, bateria):
    """
    Simula a eficiência dos painéis solares com base na temperatura.
    Eficiência de referência: 100% entre 15°C e 25°C.
    Coeficiente de temperatura típico de painel fotovoltaico: -0.45% por °C acima de 25°C.
    """
    eficiencia_base = 100.0
    if temperatura > 25:
        eficiencia_base -= (temperatura - 25) * 0.45
    elif temperatura < 15:
        eficiencia_base -= (15 - temperatura) * 0.30
    eficiencia_base = max(0, min(100, eficiencia_base))

    # kWh estimado por ciclo (painel de 2 kWp, 1h de ciclo)
    kwh = (eficiencia_base / 100) * 2.0 * (bateria / 100)
    return round(eficiencia_base, 2), round(kwh, 3)

def classificar_ciclo(pontuacao):
    if pontuacao <= 2:
        return NORMAL, "MISSÃO ESTÁVEL"
    elif pontuacao <= 5:
        return ATENCAO, "MISSÃO EM ATENÇÃO"
    else:
        return CRITICO, "MISSÃO CRÍTICA"

# ============================================================
# GERAÇÃO DE ALERTAS E RECOMENDAÇÕES
# ============================================================

def gerar_recomendacao(resultados):
    criticos = [areas[i] for i, (nivel, _, _) in enumerate(resultados) if nivel == CRITICO]

    if len(criticos) >= 3:
        print(VERMELHO + BOLD +
              "⚠  ALERTA MÁXIMO: Ativar modo de segurança.\n"
              "   Priorizar suporte à vida e desligar consumidores não essenciais." + RESET)
        return

    msgs = {
        "Temperatura dos painéis solares":
            "Acionar sistema de resfriamento passivo dos painéis solares.",
        "Comunicação com a base":
            "Tentar restabelecer contato; verificar antena e alimentação elétrica.",
        "Carga das baterias de íon-lítio":
            "Ativar modo de economia energética; verificar orientação dos painéis.",
        "Suporte de oxigênio":
            "Acionar protocolo de suporte à vida imediatamente.",
        "Estabilidade operacional":
            "Reduzir operações não essenciais para estabilizar a missão.",
    }

    imprimiu = False
    for area in criticos:
        print(VERMELHO + f"  ► Recomendação [{area}]: {msgs[area]}" + RESET)
        imprimiu = True

    if not imprimiu:
        atencoes = [i for i, (nivel, _, _) in enumerate(resultados) if nivel == ATENCAO]
        if atencoes:
            for i in atencoes:
                print(AMARELO + f"  ► Atenção [{areas[i]}]: Monitorar com frequência maior." + RESET)
        else:
            print(VERDE + "  ► Todos os sistemas dentro dos parâmetros. Manter operação normal." + RESET)

# ============================================================
# ANÁLISES AVANÇADAS
# ============================================================

def analisar_tendencia():
    if len(historico) < 2:
        print(AMARELO + "  Mínimo de 2 leituras necessárias para analisar tendência." + RESET)
        return

    def calcular_risco(leitura):
        res = [
            analisar_temperatura (leitura["temperatura"]),
            analisar_comunicacao (leitura["comunicacao"]),
            analisar_bateria     (leitura["bateria"]),
            analisar_oxigenio    (leitura["oxigenio"]),
            analisar_estabilidade(leitura["estabilidade"]),
        ]
        return sum(pts for _, pts, _ in res)

    risco_primeiro = calcular_risco(historico[0])
    risco_ultimo   = calcular_risco(historico[-1])

    print(CIANO + "\n  ── ANÁLISE DE TENDÊNCIA ──" + RESET)
    print(f"  Risco no 1º ciclo    : {risco_primeiro} ponto(s)")
    print(f"  Risco no ciclo atual : {risco_ultimo} ponto(s)")

    if risco_ultimo > risco_primeiro:
        print(VERMELHO + "  Tendência: Missão com piora progressiva. Intervenção recomendada." + RESET)
    elif risco_ultimo < risco_primeiro:
        print(VERDE + "  Tendência: Missão com melhora. Sistemas se recuperando." + RESET)
    else:
        print(AMARELO + "  Tendência: Missão estável. Sem variação de risco." + RESET)

def identificar_area_mais_afetada():
    idx = pontos_acumulados.index(max(pontos_acumulados))

    print(CIANO + "\n  ── ÁREA MAIS AFETADA ──" + RESET)
    for i, area in enumerate(areas):
        barra = "█" * pontos_acumulados[i] + "░" * max(0, 10 - pontos_acumulados[i])
        print(f"  {area:<40}: [{barra}] {pontos_acumulados[i]} pt(s)")

    print(VERMELHO + f"\n  Área crítica: {areas[idx]} — {pontos_acumulados[idx]} ponto(s) acumulados." + RESET)

def resumo_energia_solar():
    """Exibe o resumo da eficiência energética renovável da missão."""
    if not energia_gerada_kwh:
        print(AMARELO + "\n  Nenhum dado de energia solar registrado ainda." + RESET)
        return

    total_kwh    = sum(energia_gerada_kwh)
    media_kwh    = total_kwh / len(energia_gerada_kwh)
    max_kwh      = max(energia_gerada_kwh)
    min_kwh      = min(energia_gerada_kwh)
    co2_evitado  = total_kwh * 0.233   # fator médio: 0.233 kg CO₂ por kWh (fonte: IPCC)

    print(CIANO + "\n  ── RESUMO DE ENERGIA SOLAR CAPTADA ──" + RESET)
    print(f"  Ciclos com leitura     : {len(energia_gerada_kwh)}")
    print(f"  Total gerado (est.)    : {total_kwh:.3f} kWh")
    print(f"  Média por ciclo        : {media_kwh:.3f} kWh")
    print(f"  Maior geração          : {max_kwh:.3f} kWh")
    print(f"  Menor geração          : {min_kwh:.3f} kWh")
    print(VERDE + f"  CO₂ evitado (est.)     : {co2_evitado:.3f} kg" + RESET)
    print(AMARELO + "  (Base: painéis de 2 kWp — ciclo de 1h — fator IPCC 0.233 kg/kWh)" + RESET)

def gerar_relatorio_final():
    if not historico:
        print(AMARELO + "\n  Nenhuma leitura registrada para gerar relatório." + RESET)
        return

    n = len(historico)
    medias = {
        "temperatura":  sum(h["temperatura"]  for h in historico) / n,
        "comunicacao":  sum(h["comunicacao"]   for h in historico) / n * 100,
        "bateria":      sum(h["bateria"]       for h in historico) / n,
        "oxigenio":     sum(h["oxigenio"]      for h in historico) / n,
        "estabilidade": sum(h["estabilidade"]  for h in historico) / n,
    }

    riscos = []
    for leitura in historico:
        res = [
            analisar_temperatura (leitura["temperatura"]),
            analisar_comunicacao (leitura["comunicacao"]),
            analisar_bateria     (leitura["bateria"]),
            analisar_oxigenio    (leitura["oxigenio"]),
            analisar_estabilidade(leitura["estabilidade"]),
        ]
        riscos.append(sum(pts for _, pts, _ in res))

    maior_risco   = max(riscos)
    ciclo_critico = riscos.index(maior_risco) + 1
    risco_medio   = sum(riscos) / n
    qtd_criticos  = sum(1 for r in riscos if r >= 6)
    nivel_final, classificacao_final = classificar_ciclo(round(risco_medio))

    print(CIANO + BOLD)
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║              RELATÓRIO FINAL DA MISSÃO               ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(RESET, end="")

    print(f"  Missão                   : {NOME_MISSAO}")
    print(f"  Equipe                   : {NOME_EQUIPE}")
    print(f"  Data de encerramento     : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  Ciclos registrados       : {n}")
    print()
    print(f"  Média de temperatura     : {medias['temperatura']:.2f} °C")
    print(f"  Média de comunicação     : {medias['comunicacao']:.1f}% de disponibilidade")
    print(f"  Média de bateria         : {medias['bateria']:.2f}%")
    print(f"  Média de oxigênio        : {medias['oxigenio']:.2f}%")
    print(f"  Média de estabilidade    : {medias['estabilidade']:.2f}%")
    print()
    print(f"  Ciclo mais crítico       : Ciclo {ciclo_critico}")
    print(f"  Maior pontuação de risco : {maior_risco}")
    print(f"  Risco médio da missão    : {risco_medio:.2f}")
    print(f"  Ciclos em estado crítico : {qtd_criticos}")

    resumo_energia_solar()
    analisar_tendencia()
    identificar_area_mais_afetada()

    print()
    print(cor_nivel(nivel_final, f"  Classificação final : {classificacao_final}"))
    print(CIANO + "══════════════════════════════════════════════════════" + RESET)

# ============================================================
# FUNÇÕES DE MENU
# ============================================================

def inserir_dados():
    global dados_atuais

    print(AMARELO + "\n  ── INSERÇÃO DE DADOS DA MISSÃO ──" + RESET)
    print("  (Painéis solares | Comunicação | Baterias | Oxigênio | Estabilidade)\n")

    try:
        temperatura  = float(input("  Temperatura dos painéis  (°C)           : "))
        comunicacao  = int  (input("  Comunicação              (1=ativa/0=falha): "))
        bateria      = float(input("  Carga das baterias       (%)             : "))
        oxigenio     = float(input("  Oxigênio                 (%)             : "))
        estabilidade = float(input("  Estabilidade operacional (%)             : "))
    except ValueError:
        print(VERMELHO + "\n  [ERRO] Valor inválido. Digite apenas números." + RESET)
        return

    # Validação e limites
    if comunicacao not in (0, 1):
        comunicacao = 0
    bateria      = max(0, min(100, bateria))
    oxigenio     = max(0, min(100, oxigenio))
    estabilidade = max(0, min(100, estabilidade))

    dados_atuais = {
        "temperatura":  temperatura,
        "comunicacao":  comunicacao,
        "bateria":      bateria,
        "oxigenio":     oxigenio,
        "estabilidade": estabilidade,
    }

    # Calcular eficiência solar e registrar
    eficiencia, kwh = calcular_eficiencia_solar(temperatura, bateria)
    energia_gerada_kwh.append(kwh)

    # Salvar histórico e acumular pontos
    if len(historico) < 50:
        res = [
            analisar_temperatura (temperatura),
            analisar_comunicacao (comunicacao),
            analisar_bateria     (bateria),
            analisar_oxigenio    (oxigenio),
            analisar_estabilidade(estabilidade),
        ]
        for i, (_, pts, _) in enumerate(res):
            pontos_acumulados[i] += pts
        historico.append(dict(dados_atuais))

    print(VERDE + f"\n  [OK] Dados registrados com sucesso!" + RESET)
    print(f"  Eficiência solar estimada : {eficiencia:.1f}%")
    print(f"  Energia gerada (est.)     : {kwh:.3f} kWh neste ciclo")

def visualizar_status():
    res = [
        analisar_temperatura (dados_atuais["temperatura"]),
        analisar_comunicacao (dados_atuais["comunicacao"]),
        analisar_bateria     (dados_atuais["bateria"]),
        analisar_oxigenio    (dados_atuais["oxigenio"]),
        analisar_estabilidade(dados_atuais["estabilidade"]),
    ]
    pontuacao = sum(pts for _, pts, _ in res)
    nivel_ciclo, classe_ciclo = classificar_ciclo(pontuacao)

    eficiencia, kwh = calcular_eficiencia_solar(
        dados_atuais["temperatura"], dados_atuais["bateria"]
    )

    print(CIANO + "\n  ── STATUS ATUAL DA MISSÃO ──" + RESET)

    rotulos = [
        "Temp. painéis solares",
        "Comunicação      ",
        "Bateria (íon-lítio)",
        "Oxigênio         ",
        "Estabilidade     ",
    ]
    valores = [
        f"{dados_atuais['temperatura']:.1f} °C",
        "Ativa" if dados_atuais['comunicacao'] == 1 else "Falha",
        barra_progresso(dados_atuais['bateria']),
        barra_progresso(dados_atuais['oxigenio']),
        barra_progresso(dados_atuais['estabilidade']),
    ]

    for i, (nivel, _, desc) in enumerate(res):
        status = cor_nivel(nivel, desc)
        print(f"  {rotulos[i]:<22}: {status}")
        print(f"  {'':22}  {BRANCO}{valores[i]}{RESET}")
        print()

    print(f"  Eficiência fotovoltaica estimada : {eficiencia:.1f}%")
    print(f"  Energia gerada (est.)            : {kwh:.3f} kWh")
    print(f"  Pontuação de risco               : {pontuacao}")
    print(f"  Classificação do ciclo           : {cor_nivel(nivel_ciclo, classe_ciclo)}")
    print(f"  Total de leituras registradas    : {len(historico)}")

def executar_analise():
    res = [
        analisar_temperatura (dados_atuais["temperatura"]),
        analisar_comunicacao (dados_atuais["comunicacao"]),
        analisar_bateria     (dados_atuais["bateria"]),
        analisar_oxigenio    (dados_atuais["oxigenio"]),
        analisar_estabilidade(dados_atuais["estabilidade"]),
    ]
    pontuacao = sum(pts for _, pts, _ in res)
    alertas   = 0

    print(AMARELO + "\n  ── ANÁLISE AUTOMÁTICA DO SISTEMA ──" + RESET)

    for i, (nivel, _, desc) in enumerate(res):
        if nivel == CRITICO:
            print(VERMELHO + BOLD + f"  [CRÍTICO] {areas[i]}: {desc}" + RESET)
            alertas += 1
        elif nivel == ATENCAO:
            print(AMARELO + f"  [ATENÇÃO] {areas[i]}: {desc}" + RESET)
            alertas += 1

    if alertas == 0:
        print(VERDE + "  [OK] Todos os sistemas operando normalmente." + RESET)
    else:
        print(AMARELO + f"\n  {alertas} alerta(s) identificado(s). Verificar imediatamente!" + RESET)

    nivel_ciclo, classe_ciclo = classificar_ciclo(pontuacao)
    print(f"\n  Pontuação de risco : {pontuacao}  |  {cor_nivel(nivel_ciclo, classe_ciclo)}\n")
    gerar_recomendacao(res)

def ver_historico():
    if not historico:
        print(AMARELO + "\n  Nenhuma leitura registrada ainda." + RESET)
        return

    print(CIANO + "\n  ── HISTÓRICO DE LEITURAS ──" + RESET)
    print(f"  {'#':<4} {'Temp°C':<8} {'Com':<5} {'Bat%':<7} {'Oxi%':<7} {'Est%':<7} {'Solar%':<8} {'Classificação'}")
    print("  " + "─" * 68)

    for i, h in enumerate(historico):
        res = [
            analisar_temperatura (h["temperatura"]),
            analisar_comunicacao (h["comunicacao"]),
            analisar_bateria     (h["bateria"]),
            analisar_oxigenio    (h["oxigenio"]),
            analisar_estabilidade(h["estabilidade"]),
        ]
        pts = sum(p for _, p, _ in res)
        _, classe = classificar_ciclo(pts)
        ef, _ = calcular_eficiencia_solar(h["temperatura"], h["bateria"])
        com_str = "Ativa" if h["comunicacao"] == 1 else "Falha"
        print(f"  {i+1:<4} {h['temperatura']:<8.1f} {com_str:<5} {h['bateria']:<7.1f} {h['oxigenio']:<7.1f} {h['estabilidade']:<7.1f} {ef:<8.1f} {classe}")

# ============================================================
# MENU PRINCIPAL
# ============================================================

def main():
    while True:
        limpar_tela()
        cabecalho()

        print(BRANCO)
        print("  ┌─ MENU PRINCIPAL ──────────────────────────────┐")
        print("  │  1. Inserir dados de telemetria               │")
        print("  │  2. Visualizar status atual                   │")
        print("  │  3. Executar análise automática               │")
        print("  │  4. Ver histórico de leituras                 │")
        print("  │  5. Analisar tendência de risco               │")
        print("  │  6. Área mais afetada                         │")
        print("  │  7. Resumo de energia solar captada           │")
        print("  │  8. Relatório final da missão                 │")
        print("  │  0. Encerrar sistema                          │")
        print("  └───────────────────────────────────────────────┘")
        print()
        opcao = input("  Opção: " + RESET).strip()
        print()

        if   opcao == "1": inserir_dados()
        elif opcao == "2": visualizar_status()
        elif opcao == "3": executar_analise()
        elif opcao == "4": ver_historico()
        elif opcao == "5": analisar_tendencia()
        elif opcao == "6": identificar_area_mais_afetada()
        elif opcao == "7": resumo_energia_solar()
        elif opcao == "8": gerar_relatorio_final()
        elif opcao == "0":
            print(CIANO + "  Sistema encerrado. Fim da missão." + RESET)
            sys.exit(0)
        else:
            print(VERMELHO + "  Opção inválida. Tente novamente." + RESET)

        input("\n  Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()