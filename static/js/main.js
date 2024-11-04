var itens = document.getElementsByClassName("itemOrdenar");

for (var i = 0; i < itens.length; i++) {
    let url = new URL(document.URL);  
    url.searchParams.set("ordem", itens[i].name);
    itens[i].href = url.href;
}
