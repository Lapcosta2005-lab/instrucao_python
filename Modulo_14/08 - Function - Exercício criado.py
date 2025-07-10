
formatacao = input("Qual a formatação você deseja, letra maiúscula (M) ou minúscula (m)? ")
def padrao_codigo(lista, padrao = formatacao):
    for i, item in enumerate(lista):
        item = item.strip()
        if padrao == "m":
            item = item.casefold()
        elif padrao == "M":
            item = item.upper()
        lista[i] = item
    return lista


produtos = [' cachorro   ', 'Gato ', '   COBRA']
print(padrao_codigo(produtos))