# Nessa primeira etapa é necessário fazer a integração com o Google SHeets para coseguir pegar alguns dados 
#Inicialmente é importado algumas bibliotecas do google

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Bibliotecas para manipulação de tabelas
import pandas as pd
import numpy as np
# Biblioteca do BOT do Telegram
import telebot
import time

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1SmcZDALBahecfYrYXpIcQBAfPz6Ia9gF6lpkNPd_gPA"
SAMPLE_RANGE_NAME_01 = "config!B1:AK2"

# Processo de autentificação e obtenção dos dados do Google Sheets 
def main(SAMPLE_RANGE_NAME,Adicionar_valores,Valores_p_adicionar):

  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    if Adicionar_valores == "SIM":
      valor_obtido = Valores_p_adicionar
      Valores_adicionar =[[valor_obtido.replace("/","")]]
      # print(Valores_adicionar)
      adicionando = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="config!B4",valueInputOption="USER_ENTERED",
                                          body={'values': Valores_adicionar}).execute()

    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute())
    
    #Extraindo as as possibilidades de sentimentos e estilos musicais
    Valores = result['values']
    #Verificação de Erro
    
  except HttpError as err:
    print(err)
  return (Valores)



if __name__ == "__main__":
  x = main(SAMPLE_RANGE_NAME_01,"NÃO","")
  # print(x)
  sentimento_x = x[0] 
  # print(sentimento_x)
  estilos_x = x[1]
  # Teste topico estou adicionando "/" em cada sentimento para conseguir utilizar como comando no telegram
  tam_sentimento = range(len(sentimento_x))
  # print(tam_sentimento)
  tam_estilos = range(len(estilos_x))
  sentimentos = []
  estilos = []
  for n in tam_sentimento:
   sentimentos.insert(n,'/'+sentimento_x[n])
  for m in tam_estilos:
   estilos.insert(n,'/'+ estilos_x[m])
  # print(sentimentos)
  # print(estilos)
  def listaMenores_sentimento(lista,n):
    for i in range(0,len(sentimentos),n):
      yield lista[i:i + n]
  coluns_sentiemntos = 3
  linhas_sentimentos = round(len(tam_sentimento)/coluns_sentiemntos)
  # print((linhas_sentimentos))
  lista_dividida = list(listaMenores_sentimento(sentimentos,coluns_sentiemntos))
  # print(lista_dividida)
  tam_linhas_sentimentos = range((linhas_sentimentos))
  # print(tam_linhas_sentimentos)


######### INICIANDO A INTERAÇÃO COM O TELEGRAM
CHAVE_API = "6587636358:AAHwtoYJATb87gOrbHvJ16oZkuC8Vawk-8M"
bot = telebot.TeleBot(CHAVE_API)

for i in range(0,len(sentimentos)):
  
  sentimentos_sem_barra = sentimentos[i].replace("/","")
  # print(sentimentos_sem_barra)
  @bot.message_handler(commands=[sentimentos_sem_barra])
  def escolha(mensagem):
    # print(mensagem.text)
    # if mensagem == sentimentos[i]:
    SAMPLE_RANGE_NAME_02="config!J6:O10"
    if __name__ == "__main__":
        y = main(SAMPLE_RANGE_NAME_02,"SIM",mensagem.text)
        print(y)
        if y[0][0] == '#N/A':
          bot.send_message(mensagem.chat.id,"Foi mal ainda não temos musicas para esse sentimento\
          para nos ajudar voce pode preencher esse forms: https://docs.google.com/forms/d/e/1FAIpQLSf0aYQ7TZSojoeX_Zd8_NnG3r09Tid6Ge6SC2VJzm9tEvm7LQ/viewform")
        else:        
          bot.send_message(mensagem.chat.id,"Selecionei algumas músicas que se relacionam com esse sentimento. Curta e aproveite essa experiência!")
          for n in range(0,5):
            if y[n][0] == '#N/A':
              break
            xy = y[n]
            print(xy)
            texto_1 = "Nome da Música: "
            texto_2 = "Artista: "
            texto_3 = "Um trecho pra você conhecer: "
            texto_4 = "Gênero Musical:  "
            # if xy[4] == "":
            texto_4_1 = " / "
            if len(xy) < 6 or xy[-1] == 'adicionar':
              link = 'Ainda não temos link para essa musica'
            else:
              link = str(xy[-1])

            bot.send_message(mensagem.chat.id,texto_1 +xy[0]+'\n'+ texto_2 + xy[1]+'\n'+ texto_3 +'\n'+xy[2]+'\n'+texto_4+xy[3]+'\n'+link)
        time.sleep(1)
        bot.send_message(mensagem.chat.id, "Deseja explorar mais algum sentimento?   /Clique_aqui")
        
        time.sleep(1)
        bot.send_message(mensagem.chat.id, "Agradecemos imensamente sua participação! Se você quiser compartilhar sua opinião, sugerir músicas ou falar sobre outros sentimentos, ficaríamos muito felizes em ouvir suas ideias. /Clique_Aqui ")
@bot.message_handler(commands=["Clique_Aqui"])
def escolha_01(mensagem): 
  bot.reply_to(mensagem, "Você pode preencher este formulário: "+'\n'+"https://docs.google.com/forms/d/e/1FAIpQLSf0aYQ7TZSojoeX_Zd8_NnG3r09Tid6Ge6SC2VJzm9tEvm7LQ/viewform "+'\n'+" Sua contribuição é muito valiosa para nós! ")
        # time.sleep(1)
            # bot.send_message(mensagem.chat.id,link)
            # else:
              # bot.send_message(mensagem.chat.id,texto_1 + str(n+1) + texto_1_1 +xy[0]+'\n'+ texto_2 + xy[1]+'\n'+ texto_3 +'\n'+xy[2]+'\n'+texto_4+xy[3]+'\n'+xy[5])
            # print("como"+ str(teste) +"opção")
          # bot.send_message(mensagem.chat.id,"Agora conta pra gente, quais das opções mais te agradou (clique na Opção a seguir:) \n /Opcao_1\n /Opcao_2\n /Opcao_3\n /Opcao_4\n /Opcao_5")
    



def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def reponder(mensagem):
   texxto_1 = """
    Saaaalve! Se você está cansade de ouvir músicas que não te representam ou, simplesmente, quer conhecer novas músicas e artistas negres, você está no lugar certo! 🎶🌍🎵
    """
   texxto_2 = """
    Meu nome é Marron, eu sou um BOT criado para celebrar e promover as africanidades brasileiras através da música. A ideia é: você escolhe um sentimento e eu te entrego músicas relacionadas a ele.
    """ 
   texxto_3 = """Qual sentimento você gostaria de explorar?"""
   for nn in tam_linhas_sentimentos: 
    minha_string = "  ".join(lista_dividida[nn])
    texxto_3 = texxto_3 + "\n "+minha_string 
  #  print(texxto)
          # bot.send_message(mensagem,texxto)
  
   bot.reply_to(mensagem,texxto_1)
   bot.send_message(mensagem.chat.id,texxto_2+texxto_3)
  #  bot.send_message(mensagem.chat.id,texxto_3)
   respostas_usuario = mensagem.text
  #  print(respostas_usuario)## PEGA A ESCOLHA DO USUARIO

    # print(y)
  
  #ATÉ AQUI ESTÁ FUNCIONANDO

bot.polling()



