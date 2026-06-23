# GS-SERS

# 🛰️ Mission Control — Sistema de Monitoramento de Energia Solar Espacial

> **GS2026.1 · Soluções em Energias Renováveis e Sustentáveis**  

---

## 📋 Sobre o Projeto

O **Mission Control** é um sistema de monitoramento inteligente para missões espaciais experimentais, com foco em **energia solar fotovoltaica** como fonte renovável principal. O sistema recebe dados simulados de telemetria, analisa as condições operacionais em tempo real, gera alertas automáticos e produz recomendações baseadas em lógica de decisão.

A missão monitorada é a **Missão Hélio-1**, cujo sistema energético depende inteiramente de painéis solares e baterias de íon-lítio — reforçando a aplicação de conceitos de sustentabilidade e eficiência energética no contexto espacial.

---

## 🌱 Conexão com Energias Renováveis

| Elemento | Aplicação no sistema |
|---|---|
| **Painéis solares fotovoltaicos** | A temperatura monitorada reflete diretamente a eficiência dos painéis. O sistema aplica o coeficiente de temperatura real de painéis solares: **-0,45% por °C acima de 25°C** |
| **Baterias de íon-lítio** | Representam o armazenamento da energia captada pelos painéis solares |
| **Cálculo de energia gerada** | A cada ciclo, o sistema estima os kWh produzidos com base na eficiência fotovoltaica e no nível de bateria |
| **CO₂ evitado** | O relatório final calcula a emissão de CO₂ evitada usando o fator médio do IPCC: **0,233 kg por kWh** |

---

## ⚙️ Funcionalidades

- **Monitoramento de 5 sistemas** em tempo real:
  - Temperatura dos painéis solares
  - Comunicação com a base
  - Carga das baterias de íon-lítio
  - Suporte de oxigênio
  - Estabilidade operacional

- **Geração automática de alertas** com 3 níveis: `NORMAL`, `ATENÇÃO` e `CRÍTICO`

- **Tomada de decisão automatizada**: recomendações específicas por sistema afetado

- **Análise de tendência**: compara o risco do primeiro ciclo com o atual

- **Eficiência fotovoltaica**: calculada a cada leitura com base na temperatura

- **Resumo de energia solar captada**: total de kWh gerado e CO₂ evitado estimado

- **Relatório final completo**: médias, ciclo mais crítico, área mais afetada e classificação geral

---

## 🗂️ Estrutura do Projeto

```
mission-control/
│
├── mission_control.py   # Sistema principal
└── README.md            # Este arquivo
```

---

## ▶️ Como Executar

**Requisitos:** Python 3.8 ou superior. Nenhuma biblioteca externa necessária.

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/mission-control.git

# Entre na pasta
cd mission-control

# Execute o sistema
python mission_control.py
```

---

## 🖥️ Menu do Sistema

```
┌─ MENU PRINCIPAL ──────────────────────────────┐
│  1. Inserir dados de telemetria               │
│  2. Visualizar status atual                   │
│  3. Executar análise automática               │
│  4. Ver histórico de leituras                 │
│  5. Analisar tendência de risco               │
│  6. Área mais afetada                         │
│  7. Resumo de energia solar captada           │
│  8. Relatório final da missão                 │
│  0. Encerrar sistema                          │
└───────────────────────────────────────────────┘
```

---

## 📊 Parâmetros de Análise

| Sistema | Normal | Atenção | Crítico |
|---|---|---|---|
| Temperatura painéis | 10°C – 35°C | < 10°C ou 35°C – 45°C | > 45°C |
| Comunicação | Ativa (1) | — | Falha (0) |
| Bateria | ≥ 50% | 20% – 49% | < 20% |
| Oxigênio | ≥ 90% | 80% – 89% | < 80% |
| Estabilidade | ≥ 70% | 40% – 69% | < 40% |

---

## 🤖 Inteligência e Tomada de Decisão

O sistema utiliza **tomada de decisão baseada em regras** (*rule-based decision making*), uma forma introdutória de inteligência artificial aplicada a sistemas de controle. Cada condição monitorada é classificada por um conjunto de regras que produzem respostas automatizadas proporcionais à gravidade do problema.

Quando 3 ou mais sistemas estão em estado crítico simultaneamente, o sistema aciona automaticamente o **modo de segurança máxima**, priorizando suporte à vida e desligamento de consumidores não essenciais.

---

## 👥 Equipe

| Nome completo | RM |
| Olavo Dadario Vianna Barreto |RM: 569272|
| Paulo Henrique Lira Bilac de Araujo | 569496 |
| Pedro Soares de Souza | 571285 |

**Turma:** 1CCPF · FIAP · 2026  
