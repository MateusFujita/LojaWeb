import mercadopago

publicKey = "APP_USR-7b3e79f1-ac3e-457c-86ee-63274eb0d38b"
token = "APP_USR-1447703668097327-121610-c00b2dce2bb6bdbdaef99181ed713b93-2159381799"

def criarPagamento(itemPedido, link):
    sdk = mercadopago.SDK(token)

    itens = []
    for item in itemPedido:
        quantidade = int(item.quantidade)
        produto = item.itemEstoque.produto.nome
        preco = float(item.itemEstoque.produto.preco)

        itens.append({
            "title": produto,
            "quantity": quantidade,
            "unit_price": preco
        })

    preference_data = {
        "items": itens,
        "auto_return": "all",
        "back_urls": {
            "success": link,
            "pending": link,
            "failure": link
        }
    }

    # Apenas uma única chamada ao MercadoPago
    resposta = sdk.preference().create(preference_data)
    link_pagamento = resposta["response"]["init_point"]
    id_pagamento = resposta["response"]["id"]

    print(f"ID do Pagamento: {id_pagamento}")
    print(f"Link de Pagamento: {link_pagamento}")

    return link_pagamento, id_pagamento

