import re
import requests

print("### SOFTWARE WEB SCRAPPER ###")
#link = requests.get(input("\nInforme o link do Wikipedia que deseja analisar:"))
link = input("\nInforme o link do Wikipedia que deseja analisar:")

def showMenu(titulo,main):
    while True:
        print("\n#### OPÇÕES PARA EXTRAÇÃO DE DADOS DA PÁGINA: " + titulo.upper() + "####\n")
        print("1 - Listar os tópicos do índice do artigo")
        print("2 - Listar todos os nomes de arquivos de imagens presentes no artigo")
        print("3 - Listar todos os links para outros artigos da Wikipedia que são citados no conteúdo do artigo.\n")
        opcao = int(input("Informe a opção desejada:"))

        if opcao == 1:
            listaTopicos(titulo,main)
        elif opcao == 2:
            listaNomesImagens(titulo,main)
        elif opcao == 3:
            listaLinks(titulo,main)
        else:
            print("\n" * 2)
            print("ERRO! Opção inválida! \n Escolha uma das opções exibidas no menu.")
            print("\n" * 2)
            showMenu()

def verificaLink(linkRecebido):
    linkAtivo = False
    linkWikipedia = False
   
    if requests.get(linkRecebido).status_code == 200:
        linkAtivo = True
    
    if re.search(r'(https{0,1}:\/\/)?pt.wikipedia.org',linkRecebido):
        linkWikipedia = True  
    
    if linkAtivo and linkWikipedia:
        link = requests.get(linkRecebido).text.replace('\n', '') #retirando as quebras de linhas do código
        titulo_busca = re.findall(r'<title>(.*)–.*</title>',link)
        titulo = titulo_busca[0]
        main_busca = re.search(r'(<main.*</main>)', link) #selecionando o corpo do artigo
        main= main_busca[0]
        showMenu(titulo,main)
    else:
        print("Link inválido!")

# Listar os topicos do ındice do artigo
def listaTopicos(titulo,main):
    indices = re.findall(r'<span class="tocnumber">(\d+[\.?\d*]*)</span>\s*<span class="toctext">([^\<]+)[</span>\s*</a>]', main)
    print('\nTOPICOS DO INDICE:\n')
    for topico in indices:
        numero = topico[0]
        topico = topico[1]
        for x in numero:
            if x=='.': 
                print('   ',end='')
        print(str(numero) + ' ' + topico)
    retornarMenu(titulo,main)

#Listar todos os links para outros artigos da Wikipedia que sao citados no conteudo do artigo
def listaLinks(titulo,main):
    links = re.findall(r'href="(/wiki[^\"]+)', main)
    i=1
    print('\nLINKS PARA OUTROS ARTIGOS DA WIKIPEDIA:\n')
    for x in links:
        print(i, x)
        i=i+1
    retornarMenu(titulo,main)

#Listar todas as imagens que sao citadas no conteudo do artigo
def listaNomesImagens(titulo,main):
    imagens = re.findall(r'src="//upload.wikimedia.org/wikipedia/commons/thumb/\w*/\w*/([^\/]+)', main)
    i=1
    print('\nNOMES DOS ARQUIVOS DE IMAGEM:\n')
    for x in imagens:
        print(i, x)
        i=i+1
    retornarMenu(titulo,main)

def retornarMenu(titulo,main):
    print('\n-------------------------------------------------------------------')
    continuar = input('Deseja retornar ao menu? (s/n)').upper()
    if continuar =='S':
        print('\n')
        showMenu(titulo,main)
    elif continuar =='N':
        exit()
    else:
        print('Resposta inválida!')
        retornarMenu(titulo,main)
        
verificaLink(link)
