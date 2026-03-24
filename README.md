# 🌐 Network Configuration Generator

Esta aplicação web, desenvolvida em Python com a framework Streamlit, permite aos administradores de rede gerar rapidamente ficheiros de configuração padronizados e sem erros para equipamentos Cisco (Switches e Routers).

## 🎯 Objetivo do Projeto
O objetivo é simplificar o *provisioning* de equipamentos de rede, substituindo a configuração manual via CLI por uma interface gráfica intuitiva que gera o *script* final pronto a aplicar, poupando tempo e reduzindo erros de digitação (*typos*).

## ✨ Funcionalidades Principais

A interface está dividida em três áreas lógicas de configuração:

* **⚙️ Definições Globais & Segurança:**
  * Configuração de *Hostname* e *Domain Name*.
  * Definição do *MOTD Banner* e geração de chaves criptográficas (SSH v2).
  * Encriptação de palavras-passe nativa (`service password-encryption`).
* **🏗️ VLANs & Interfaces Físicas:**
  * Criação de VLANs (ID e Nome) e respetivas interfaces virtuais (SVI) com endereçamento IP.
  * Configuração de portas físicas em modo `access` (atribuição de VLAN) ou `trunk` (dot1q).
* **🌐 Encaminhamento (Routing):**
  * Geração de rotas estáticas (*Static Routes* / *Default Gateway*).
* **🛡️ Auditoria de Segurança Integrada:**
  * Validação em tempo real da existência e força da palavra-passe `enable secret`, alertando o utilizador para más práticas.
* **💾 Exportação:**
  * Geração instantânea do código final em sintaxe Cisco IOS e opção de *download* do ficheiro `.txt`.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3
* **Interface Web:** Streamlit
* **Validação:** Expressões Regulares (`re`)
* **Domínio:** Redes Cisco (IOS)

## 🚀 Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone [https://github.com/teu-utilizador/teu-repositorio.git](https://github.com/teu-utilizador/teu-repositorio.git)
