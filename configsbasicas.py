import streamlit as st
import re

# Configuração da página
st.set_page_config(page_title="Network Config Generator", page_icon="🌐", layout="wide")

def validate_ip(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip)

st.title("🌐 Network Configuration Generator")
st.markdown("---")

# --- SIDEBAR: CONFIGURAÇÕES GERAIS ---
with st.sidebar:
    st.header("⚙️ Definições Globais")
    hostname = st.text_input("Hostname do Equipamento", "SW-CORE-01")
    enable_secret = st.text_input("Enable Secret", type="password")
    domain_name = st.text_input("Domain Name", "empresa.local")
    
    st.subheader("🛡️ Segurança de Acesso")
    banner = st.text_area("MOTD Banner", "************************************************ACESSO RESTRITO!*******************************************")
    ssh_version = st.selectbox("Versão SSH", ["2", "1.99"])

# --- ÁREA PRINCIPAL: ABAS POR CATEGORIA ---
tab1, tab2, tab3 = st.tabs(["🏗️ VLANs & Interfaces", "🌐 Encaminhamento (Static)", "💾 Gerar Configuração"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("VLANs")
        vlan_id = st.number_input("ID da VLAN", min_value=1, max_value=4094, value=10)
        vlan_name = st.text_input("Nome da VLAN", "ADMIN_MGMT")
        
        st.subheader("Interface SVI (VLAN Interface)")
        vlan_ip = st.text_input("IP da Interface VLAN", "192.168.10.1")
        vlan_mask = st.text_input("Máscara (ex: 255.255.255.0)", "255.255.255.0")

    with col2:
        st.subheader("Interfaces Físicas")
        int_name = st.text_input("Nome da Interface (ex: Gi0/1)", "GigabitEthernet0/1")
        int_desc = st.text_input("Descrição", "UPLINK_TO_ROUTER")
        int_mode = st.selectbox("Modo", ["access", "trunk"])
        int_vlan = st.number_input("VLAN Atribuída (Access)", 1, 4094, value=10)

with tab2:
    st.subheader("Rotas Estáticas")
    static_net = st.text_input("Rede de Destino", "0.0.0.0")
    static_mask = st.text_input("Máscara de Destino", "0.0.0.0")
    static_gw = st.text_input("Next-Hop (Gateway)", "192.168.10.254")

with tab3:
    st.subheader("📄 Script Gerado")
    
    # Lógica de Construção da Configuração
    config_script = f"""! --- CONFIGURAÇÃO GERADA PARA {hostname} ---
hostname {hostname}
!
ip domain-name {domain_name}
!
enable secret {enable_secret if enable_secret else "Cisco123"}
!
service password-encryption
no ip domain-lookup
!
banner motd ^C
{banner}
^C
!
vlan {vlan_id}
 name {vlan_name}
!
interface Vlan {vlan_id}
 description Management SVI
 ip address {vlan_ip} {vlan_mask}
 no shutdown
!
interface {int_name}
 description {int_desc}
 switchport mode {int_mode}
 """
    
    if int_mode == "access":
        config_script += f"switchport access vlan {int_vlan}\n"
    else:
        config_script += "switchport trunk encapsulation dot1q\n switchport mode trunk\n"
        
    config_script += f"""!
ip route {static_net} {static_mask} {static_gw}
!
line vty 0 4
 transport input ssh
 login local
!
ip ssh version {ssh_version}
crypto key generate rsa modulus 2048
!
end
write memory
"""

    st.code(config_script, language="bash")
    st.download_button("Baixar Configuração (.txt)", config_script, file_name=f"{hostname}_config.txt")

# --- AUDITORIA DE SEGURANÇA ---
st.divider()
st.subheader("🛡️ Verificação de Segurança (Audit)")
if not enable_secret:
    st.error("❌ Erro: Definir um 'Enable Secret' é obrigatório para um ambiente profissional.")
elif len(enable_secret) < 8:
    st.warning("⚠️ Aviso: A password de enable deve ter pelo menos 8 caracteres.")
else:
    st.success("✅ Segurança Base: OK.")
