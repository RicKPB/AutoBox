import json

directBase = 'C:/svr-dell/COLABORADORES/Henrique Papeschi/AUTOBOX/JsonsEmpresas'
# ver com o gabriel sobre a permissao da pasta se eu consigo poder habilitar a grava dentro da pasta

def saveFileJson(nameFileJson):

    parts = nameFileJson.split('-')

    nameClient = parts[0]

    clientDirect = os.path.join(directBase, nameClient)

    if not os.path.exists(clientDirect):
        os.makedirs(clientDirect)

    directFileJson = os.path.join(clientDirect)

    return directFileJson


def saveDirectFileJson(pathfilejson, datejson):

    with open(pathfilejson, 'w', encoding='utf-8') as f:
        json.dump(datejson, f, ensure_ascii=False, indent=4)

    print(f'Aquivo salvo em {pathfilejson}')
