def filtrarProdutos(produtos, filtro):
    if filtro:
        print(f"Filtro recebido: {filtro}")  # Adicione um print para ver o filtro recebido
        if "-" in filtro:
            categoria, tipo = filtro.split("-")
            print(f"Categoria: {categoria}, Tipo: {tipo}")  # Verifique se os valores estão corretos
            produtos = produtos.filter(tipo__slug=tipo, categoria__slug=categoria)
        else:
            produtos = produtos.filter(categoria__slug=filtro)

    return produtos


