from django.db.models import Max, Min

def filtrarProdutos(produtos, filtro):
    if filtro:
        print(f"Filtro recebido: {filtro}")
        if "-" in filtro:
            categoria, tipo = filtro.split("-")
            print(f"Categoria: {categoria}, Tipo: {tipo}")
            produtos = produtos.filter(tipo__slug=tipo, categoria__slug=categoria)
            print(f"Produtos após filtro de categoria e tipo: {produtos}")
        else:
            produtos = produtos.filter(categoria__slug=filtro)
            print(f"Produtos após filtro de categoria: {produtos}")
    return produtos

def precoMaximoMinimo(produtos):
    minimo = 0
    maximo = 0
    if len(produtos) > 0:
        maximo = list(produtos.aggregate(Max("preco")).values())[0]
        maximo = round(maximo, 2)
        minimo = list(produtos.aggregate(Min("preco")).values())[0]
        minimo = round(minimo, 2)
    return minimo, maximo


