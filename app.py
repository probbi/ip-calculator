import streamlit as st
import ipaddress

st.set_page_config(page_title="IP kalkulátor", page_icon="🌐", layout="wide")

st.title("🌐 IP kalkulátor")

# Oldalsáv a beállításoknak
with st.sidebar:
    st.header("Beállítások")
    ip_input = st.text_input("IP cím / CIDR", "192.168.1.0/24")
    st.info("Példa: 10.0.0.0/8, 172.16.0.0/12, 192.168.1.0/24")

if ip_input:
    try:
        net = ipaddress.ip_network(ip_input, strict=False)
        
        # 1. Alapadatok kártyákban
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Hálózat", str(net.network_address))
        col2.metric("Maszk", str(net.netmask))
        col3.metric("Broadcast", str(net.broadcast_address))
        col4.metric("Eszközök száma", net.num_addresses - 2 if net.prefixlen < 31 else 0)

        st.write("") # Egy kis helyköz
        specific_ip = ipaddress.ip_address(ip_input.split('/')[0])
        if specific_ip == net.network_address:
            st.info(f"📍 A megadott cím a **Hálózati cím**.")
        elif specific_ip == net.broadcast_address:
            st.warning(f"📍 A megadott cím a **Broadcast cím**.")
        else:
            st.success(f"📍 A megadott IP ({specific_ip}) egy **kiosztható host** ebben a hálózatban.")

        # 2. Bináris nézet
        st.subheader("🔢 Bináris megjelenítés")
        
        def to_bin(ip):
            return " . ".join([format(int(x), '08b') for x in str(ip).split('.')])

        st.code(f"{to_bin(net.network_address)}  (Hálózat)\n"
                f"{to_bin(net.netmask)}  (Maszk)\n"
                f"{to_bin(net.broadcast_address)}  (Broadcast)", language="text")

        # 3. Alhálózat generáló (Subnetting)
        st.subheader("✂️ Alhálózatokra bontás")
        new_prefix = st.slider("Új maszk mérete", net.prefixlen + 1, 32 if net.prefixlen < 32 else 32)
        
        if new_prefix > net.prefixlen:
            subnets = list(net.subnets(new_prefix=new_prefix))
            st.write(f"Ebből a hálózatból **{len(subnets)}** darab `/{new_prefix}`-es alhálózat hozható létre:")
            
            # Csak az első 16-ot írjuk ki, hogy ne fagyassza le az oldalt óriási range-nél
            display_subnets = [str(s) for s in subnets[:16]]
            st.table({"Alhálózatok": display_subnets})
            if len(subnets) > 16:
                st.warning(f"További {len(subnets) - 16} alhálózat nem került kilistázásra.")

    except ValueError:
        st.error("Érvénytelen formátum! Ellenőrizd az IP címet és a maszkot.")

st.divider()
st.caption("Powered by Docker & Streamlit. Hosted on Contabo VPS.")
