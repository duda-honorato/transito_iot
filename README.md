# 🚦 Sistema IoT para Segurança no Trânsito

## 📋 Sobre o Projeto

Este projeto implementa uma solução distribuída de monitoramento de trânsito utilizando conceitos de **IoT (Internet das Coisas)** e **Edge Computing**. O sistema monitora continuamente a velocidade e o fluxo veicular em vias urbanas, detecta infrações em tempo real e notifica motoristas através de atuadores inteligentes.

### 🎯 Objetivos

- Monitorar velocidade e fluxo de veículos em vias urbanas
- Detectar infrações de excesso de velocidade em tempo real
- Notificar motoristas instantaneamente via painéis e displays
- Registrar todas as infrações em nuvem para auditoria
- Demonstrar aplicação prática de diferentes protocolos de rede (UDP, TCP, Multicast)


### Componentes do Sistema

| Componente | Tecnologia | Função |
|------------|------------|--------|
| Sensor Radar | UDP Cliente | Envia leituras de velocidade continuamente |
| Sensor Fluxo | UDP Cliente | Envia dados de fluxo veicular |
| SmartGateway | UDP Servidor + TCP Cliente + Multicast | Processa dados localmente e coordena ações |
| Servidor Nuvem | TCP Servidor Multithread | Armazena infrações e gerencia histórico |
| Atuadores | Multicast Cliente | Exibem alertas e registram ocorrências |

## 📦 Pré-requisitos

- Python 3.8 ou superior
- Bibliotecas padrão (socket, threading, sqlite3, datetime, random, time, struct)

> Nenhuma biblioteca externa é necessária - tudo utiliza apenas a biblioteca padrão do Python!

## 🚀 Como Executar

### Passo 1: Estrutura do Projeto
Primeiro, crie a seguinte estrutura de diretórios e arquivos:

>>>>> INÍCIO
transito_iot/
├── sensor_radar.py
├── sensor_fluxo.py
├── smart_gateway.py
├── servidor_nuvem.py
├── atuador_painel.py
├── atuador_display.py
├── atuador_camera.py
└── shared/
    └── config.py
>>>>> FIM

### Passo 2: Abrir os Terminais

Você precisará de **NO MÍNIMO 5 terminais/janelas** de comando abertas.

| Terminal | Componente | Comando |
|----------|------------|---------|
| Terminal 1 | Servidor Nuvem | `python servidor_nuvem.py` |
| Terminal 2 | SmartGateway | `python smart_gateway.py` |
| Terminal 3 | Atuador Painel | `python atuador_painel.py` |
| Terminal 4 | Atuador Display | `python atuador_display.py` |
| Terminal 5 | Sensor Radar | `python sensor_radar.py` |

### Passo 3: Executar na Ordem Correta (IMPORTANTE!)

> ⚠️ **A ordem de execução é essencial!** Siga exatamente como abaixo:

```bash
# ┌─────────────────────────────────────────────────────────────┐
# │ TERMINAL 1 - PRIMEIRO: Servidor Nuvem                       │
# └─────────────────────────────────────────────────────────────┘
cd transito_iot
python servidor_nuvem.py

# ┌─────────────────────────────────────────────────────────────┐
# │ TERMINAL 2 - SEGUNDO: SmartGateway                          │
# └─────────────────────────────────────────────────────────────┘
cd transito_iot
python smart_gateway.py

# ┌─────────────────────────────────────────────────────────────┐
# │ TERMINAL 3 - TERCEIRO: Atuador Painel                       │
# └─────────────────────────────────────────────────────────────┘
cd transito_iot
python atuador_painel.py

# ┌─────────────────────────────────────────────────────────────┐
# │ TERMINAL 4 - QUARTO: Atuador Display                        │
# └─────────────────────────────────────────────────────────────┘
cd transito_iot
python atuador_display.py

# ┌─────────────────────────────────────────────────────────────┐
# │ TERMINAL 5 - QUINTO: Sensor Radar                           │
# └─────────────────────────────────────────────────────────────┘
cd transito_iot
python sensor_radar.py

**TERMINAL 1 - PRIMEIRO: Servidor Nuvem**

```bash
cd transito_iot
python servidor_nuvem.py
