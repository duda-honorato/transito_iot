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

### 1. Clone ou crie a estrutura do projeto

```bash
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
