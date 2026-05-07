import requests
import time

# 1. Configurações
# Usamos a API pública do Mercado Livre (substitua o ID se quiser outro produto)
PRODUCT_ID = "MLB3532356555" 
API_ML_URL = f"https://api.mercadolivre.com/items/{PRODUCT_ID}"
API_RENDER_URL = "https://sentinela-de-mercado.onrender.com/precos/"

def raspar_via_api():
    print(f"🕵️ Acessando API oficial do Mercado Livre para o item {PRODUCT_ID}...")
    
    try:
        # A API oficial raramente bloqueia, pois é feita para desenvolvedores
        resposta = requests.get(API_ML_URL, timeout=15)
        
        if resposta.status_code != 200:
            print(f"❌ Erro na API do ML: {resposta.status_code}")
            return

        dados = resposta.json()
        
        # Extraindo os dados puros do JSON
        nome = dados.get('title', 'Produto sem título')
        preco = dados.get('price', 0.0)
        link = dados.get('permalink', '')

        if preco > 0:
            print(f"✅ DADOS CAPTURADOS!")
            print(f"📦 Produto: {nome}")
            print(f"💰 Preço: R$ {preco}")
            
            # 2. Enviando para a sua API na Render
            payload = {
                "nome": nome,
                "preco": preco,
                "loja": "Mercado Livre (API)",
                "url": link
            }
            
            print(f"🚀 Enviando para a Render...")
            res_render = requests.post(API_RENDER_URL, params=payload)
            
            if res_render.status_code == 200:
                print("🏆 SUCESSO ABSOLUTO! Dados gravados no banco de dados na nuvem.")
                print(res_render.json())
            else:
                print(f"🤔 Erro ao salvar na Render: {res_render.status_code}")
        else:
            print("❌ Preço não encontrado nos dados da API.")

    except Exception as e:
        print(f"💥 Erro crítico: {e}")

if __name__ == "__main__":
    raspar_via_api()