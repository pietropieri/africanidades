
tam_linhas_sentimentos = range(0, 7)
lista_dividida=[['/Amor', '/Raiva', '/Saudade', '/Paixao', '/Tristeza'], ['/Ansiedade', '/Odio', '/Alegria', '/Felicidade', '/Medo'], ['/Angustia', '/Euforia', '/Desespero', '/Confianca', '/Inseguranca'], ['/Tranquilidade', '/Motivacao', '/Energia', '/Irritacao', '/Solidao'], ['/Otimismo', '/Confianca', '/Melancolia', '/Resignacao', '/Esperanca'], ['/Decepcao', '/Tesao', '/Superacao', '/Empoderamento', '/Confusao'], ['/Cumpricidade', '/Admiracao', '/Indignacao']]
texxto = """
    Olá! Obrigado por utilizar nosso Bot. Estamos aqui para celebrar e promover as Africanidades, uma cultura negra rica e influente que molda o mundo de diversas formas. Se você está interessado em explorar músicas relacionadas a essa cultura, está no lugar certo! 🎶🌍🎵
    Como você está se sentindo hoje? Escolha abaixo o sentimento que mais lhe atrai no momento, e nós recomendaremos músicas incríveis para você! Aproveite ao máximo essa experiência única.
    """ 
for nn in tam_linhas_sentimentos: 
    minha_string = "  ".join(lista_dividida[nn])
    texxto = texxto + "\n "+minha_string 
    print(texxto)