from playwright.sync_api import sync_playwright
import gspread
from google.oauth2.service_account import Credentials
import json
import os

# 🟢 CONFIGURACIÓN
GOOGLE_SHEET_ID = "18V_MXVZRW31n1AJXLTnc3U775GVSI1LMTOMXoobtdsg"
NOMBRE_HOJA = "1"
CELDA_OBJETIVO = "B1"

USUARIO = "antonioolea84@gmail.com"
CONTRASENA = "antolegar1997"

def obtener_url_del_indicador():
    with sync_playwright() as p:
        print("🟢 Lanzando navegador Playwright...")
        navegador = p.chromium.launch(headless=True)
        contexto = navegador.new_context()
        pagina = contexto.new_page()

        url_objetivo = None

        def interceptar_respuesta(response):
            url = response.url
            if "trendindicator.php" in url and "token=" in url:
                nonlocal url_objetivo
                url_objetivo = url
                print("🔗 URL interceptada:", url)

        pagina.on("response", interceptar_respuesta)

        print("🔐 Accediendo al login...")
        pagina.goto("https://tradingdifferent.com/login")
        pagina.fill('input[name="email"]', USUARIO)
        pagina.fill('input[name="password"]', CONTRASENA)
        pagina.click('button[type="submit"]')

        print("⏳ Esperando después del login (120s)...")
        pagina.wait_for_timeout(120000)

        print("📊 Cargando gráfico...")
        pagina.goto("https://tradingdifferent.com/pools/binance-btcusdt")
        pagina.wait_for_timeout(120000)

        navegador.close()
        return url_objetivo

def pegar_url_en_hoja(url):
    if not url or "token=" not in url:
        print("❌ No se pudo obtener la URL del indicador.")
        return

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    if "RENDER" in os.environ:
        print("🌐 Ejecutando en Render")
        json_keyfile_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
        creds = Credentials.from_service_account_info(json_keyfile_dict, scopes=scope)
    else:
        print("💻 Ejecutando en local")
        creds = Credentials.from_service_account_file("credenciales.json", scopes=scope)

    client = gspread.authorize(creds)
    hoja = client.open_by_key(GOOGLE_SHEET_ID).worksheet(NOMBRE_HOJA)
    hoja.update_acell(CELDA_OBJETIVO, url)
    print("✅ URL del indicador pegada en la hoja:", url)

if __name__ == "__main__":
    url = obtener_url_del_indicador()
    if url:
        print("✅ URL capturada correctamente:", url)
    pegar_url_en_hoja(url)
