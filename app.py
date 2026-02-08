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
        # Ellenőrizzük, hogy van-e benne perjel (maszk)
        if '/' not in ip_input:
            st.warning("⚠️ Nem adtál meg maszkot (pl. /24), így a rendszert egyetlen gépként (/32) kezelem.")
        
        net = ipaddress.ip_network(ip_input, strict=False)
        
        # 1. Alapadatok kártyákban
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Hálózat", str(net.network_address))
        col2.metric("Maszk", str(net.netmask))
        col3.metric("Broadcast", str(net.broadcast_address))
        col4.metric("Eszközök száma", net.num_addresses - 2 if net.prefixlen < 31 else 0)
        st.write("---")

        # 2. Interaktív maszkolás és Bináris nézet
        st.subheader("🔢 Interaktív bináris vizualizáció")
        
        # EGYETLEN csúszka, egyedi kulccsal
        new_prefix = st.slider("Maszk méretének módosítása (CIDR):", 
                               min_value=0, max_value=32, 
                               value=int(net.prefixlen),
                               key="main_slider")

        def colored_bin(ip, cidr):
            full_bin = "".join([format(int(x), '08b') for x in str(ip).split('.')])
            net_part = full_bin[:cidr]
            host_part = full_bin[cidr:]
            
            def add_dots(s, start_pos):
                res = ""
                for i, bit in enumerate(s):
                    absolute_pos = start_pos + i
                    if absolute_pos > 0 and absolute_pos % 8 == 0:
                        res += "."
                    res += bit
                return res

            net_final = add_dots(net_part, 0)
            host_final = add_dots(host_part, len(net_part))

            return f'<code style="font-family: monospace; font-size: 1.2em; background-color: rgba(0,0,0,0.1); padding: 8px; border-radius: 5px; display: inline-block; width: 100%;">' \
                   f'<span style="color: #3498db; font-weight: bold;">{net_final}</span>' \
                   f'<span style="color: #2ecc71;">{host_final}</span>' \
                   f'</code>'

        # Megjelenítés a csúszka értéke (new_prefix) alapján
        st.markdown(f"{colored_bin(net.network_address, new_prefix)} &nbsp; **Hálózat**", unsafe_allow_html=True)
        
        # Kiszámoljuk az ideiglenes maszkot a csúszka alapján
        temp_mask = ipaddress.IPv4Network(f"0.0.0.0/{new_prefix}").netmask
        st.markdown(f"{colored_bin(temp_mask, new_prefix)} &nbsp; **Maszk**", unsafe_allow_html=True)
        
        st.info(f"💡 Most egy **/{new_prefix}**-es maszk hatását látod a hálózaton. Kék = Hálózati rész, Zöld = Host rész.")

        st.write("---")

        # 3. Alhálózatok listázása (ha a csúszka nagyobb, mint az eredeti maszk)
        st.write("---")

        # 3. Alhálózatok listázása (Kibővített adatokkal és logikával)
        if new_prefix > net.prefixlen:
            st.subheader(f"✂️ Alhálózatok (/{new_prefix})")
            
            # Kiszámoljuk az összes alhálózatot
            subnets = list(net.subnets(new_prefix=new_prefix))
            st.write(f"Ebből a hálózatból **{len(subnets)}** darab alhálózat jön létre:")
            
            # Adatok előkészítése a részletes táblázathoz
            subnet_data = []
            for s in subnets[:16]: # Csak az első 16-ot dolgozzuk fel a sebesség miatt
                hosts = list(s.hosts())
                if hosts:
                    range_text = f"{hosts[0]} - {hosts[-1]}"
                else:
                    range_text = "Nincs kiosztható cím" # /31 vagy /32 esetén
                
                subnet_data.append({
                    "Alhálózat": str(s.network_address),
                    "CIDR": f"/{s.prefixlen}",
                    "Használható IP tartomány": range_text,
                    "Broadcast cím": str(s.broadcast_address)
                })
            
            # Megjelenítés táblázatban
            st.table(subnet_data)
            
            if len(subnets) > 16:
                st.warning(f"⚠️ További {len(subnets) - 16} alhálózat nem került kilistázásra (a böngésződ hálájára).")
        
        elif new_prefix < net.prefixlen:
            # Itt tartottuk meg a számodra fontos szuperhálózat infót
            st.warning(f"☝️ **Szuperhálózat (Supernetting) jelenség:** A választott /{new_prefix} maszk tágabb, mint az eredeti /{net.prefixlen}. Ez több hálózat összevonását jelentené.")
        
        else:
            st.info("💡 A csúszka az eredeti maszk méretén áll, így nem történt alhálózatokra bontás.")

    except ValueError:
        # Ez a rész kapja el, ha valaki betűt ír szám helyett vagy rossz az IP formátum
        st.error("❌ Érvénytelen formátum! Ellenőrizd az IP címet (pl. 192.168.1.1) és a maszkot (pl. /24).")

st.divider()
st.caption("Powered by Docker & Streamlit. Hosted on Contabo VPS. | 2026")