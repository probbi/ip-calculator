# 🌐 IP Kalkulátor és alhálózat tervező

Ez egy Streamlit alapú, interaktív hálózati segédeszköz, amit azért hoztam létre, hogy vizuálisan is érthetővé tegyem az IPv4 címzést és az alhálózatok (subnetting) világát.

## Két felhasználási mód:

- **Tanulás és szemléltetés:** A bináris nézet és a színes bit-felosztás segít megérteni, mi történik a számok mögött.
- **Napi munka:** Gyors számítások, tartományok meghatározása és alhálózatok kiosztására.

## Funkciók

**Interaktív Bináris Nézet:** A csúszka mozgatásával azonnal látod a bitek szintjén, mi a hálózati (kék) és mi a host (zöld) rész.

**Intelligens Kalkuláció:** Kiszámolja a hálózati címet, a broadcast címet és a kiosztható IP-k számát.

**Alhálózat Tervező:** Ha szűkíted a maszkot, az app automatikusan generál egy táblázatot a lehetséges alhálózatokról, feltüntetve az első és utolsó használható IP címet is.

**Hibaellenőrzés:** Szól, ha elfelejtettél maszkot megadni, vagy ha épp egy "szuperhálózatot" készítesz.

## Technológiai Stack

- **Nyelv**: Python 3.11+
- **Keretrendszer:** Streamlit
- **Környezet:** Docker & Docker Compose
- **Webszerver:** Nginx Proxy Manager (HTTPS támogatással)

## Telepítés és futtatás:

Helyi futtatás (venv használatával):

### Klónozd a tárolót:

```
git clone https://github.com/probbi/ip-calculator.git
cd ip-calculator
```


### Hozz létre virtuális környezetet és telepítsd a függőségeket:

```
python3 -m venv venv
source venv/bin/activate.fish  # Vagy .sh, ha nem Fish-t használsz
pip install -r requirements.txt 
```

### Indítsd el az appot:

```
streamlit run app.py
```


### Futtatás Dockerrel:

```
docker compose up -d --build
```
