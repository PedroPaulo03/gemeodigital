import streamlit as st
from openai import OpenAI
import os
import re

# Configurações de API 
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

# Avatares para o usuário e assistente
avatar_user = 'arquivos/avatar.png'

# Configurações de modelo e carregamento de instruções do assistente
modelo = 'gpt-4o-mini'

#instrucoes = 'arquivos/assistente-python.txt'
#with open(instrucoes, 'r', encoding='utf-8') as file:
#    instrucoes_gpt = file.read()

#botoes
usuario = st.sidebar.selectbox('Escolha uma pessoa', ['Átila', 'Danilo Lima', 'Pedro'],
                        on_change = lambda: st.session_state.clear())
#usuario = st.sidebar.selectbox('Escolha uma pessoa', ['Danilo Lima'])
#st.write(f'Você escolheu: {usuario}')

if usuario == 'Átila': 
    avatar_assistent = '😃'
    estilo = """
    - ESCREVA SEMPRE EM CAPS LOCK
    """

if usuario == 'Pedro': 
    avatar_assistent = '😎'
    estilo = """
    - ESCREVA SEMPRE USANDO O MAXIMO DE EMOJIS QUE PUDER. TIPO, MUITOO EMOJI. 
    """

if usuario == 'Danilo Lima': 
    avatar_assistent = '🥶'
    estilo = """
    - Utilize letras maiusculas no inicio de toda frase.
    - NUNCA USE EXCLAMAÇÔES E TROQUE POR ".".
    - Nunca faça perguntas retoricas no meio da frase.
    - Use girias a vontade, quanto mais, melhor.
    - Quando for responder uma pergunta foque no que você acha e não o que o outro acha,
    - Nunca utilize "Mn" e "mano" na mesma mensagem.
    - Dê muita preferencia a girias baianas do que girias de outros estados. Nunca utilize giras como "rapá", "meu rei" "praw".
    - Para demonstrar desentendimento utilize frases com "Rpz, eu n to ligado n".
    - Para perguntar se o usuario entendeu pergunte "tlgd?" no final da frase, mas só utilize isso quando estiver explicando ou contando algo.
    - Raramente utilize exclamações nas mensagens.
    - Nunca faça perguntas no meio da frase.
    - Nunca separe a mensagem da risada com um ponto.
    - Raramente coloque ponto final nas mensagens.
    - Na maioria das vezes em contextos informais você começará a frase com "rpz,", mas em começos de conversas evitará o uso.
    - Use variações de "dboa" ao inves de "suave" ou sinonimos.
    - Em situações engraçadas você deverá rir com "KKKKK",  "kakakaka", "kkkkk",  e "ashusduwahsud", sequencia aleatoria de letras. Para demonstrar coisas muito engraçadas sempre dê enfase aumentando a quantidade de letras independente do jeito de rir.
    - palavras como "oxe", "oxente" devem ser frequentemente usadas para representar duvida, desentendimento ou absurdo na fala do usuario.
    - use "uskara" como sinonimo de voces, porem só utlize essa palavra quando quiser chamar a atenção de todos na conversa e sempre no inicio da mensagem.
    - Use "Mano," no inicio da frase para chamar atenção do usuario. Utilize variações como "Mn" também.
    - Nunca ria fora de contexto. Você deverá rir somente quando alguem rir ou quando contarem uma piada.
    - Sempre repita a ultima letra das palavras quando quiser demonstrar afetividade (exemplo: 'manooooooo').

    """


n = st.sidebar.slider('Escolha o tamanho do historico', 
                        min_value= 10, max_value=2000,  
                        step=10, value=10,
                        on_change = lambda: st.session_state.clear())
#st.write(f'Você escolheu: {n}')


#st.write(estilo)

# Mensagem inicial do assistente no chat
frase_inicial = f'Sou o Gemeo Digital de {usuario}, fala ai que eu te respondo!'


def ler_whatsapp_txt(arquivo, n=None):
    mensagens = []

    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            # Expressão regular para capturar as mensagens no formato correto
            padrao = r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.+?): (.+)"
            match = re.match(padrao, linha)

            if match:
                _, nome, mensagem = match.groups()
                mensagens.append(f"{nome}: {mensagem}")

    if n is not None:
        mensagens = mensagens[-n:]

    return "\n\n".join(mensagens)


def ler_multiplas_conversas(diretorio, n=None):
    # Lista para armazenar todas as mensagens coletadas
    todas_mensagens = []

    # Itera sobre todos os arquivos dentro do diretório
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".txt"):  # Considera apenas arquivos .txt
            caminho_arquivo = os.path.join(diretorio, arquivo)
            todas_mensagens.append(ler_whatsapp_txt(caminho_arquivo, n))  # Adiciona as mensagens de cada conversa

    return "\n\n".join(todas_mensagens)

 

historico = ler_multiplas_conversas('arquivos/conversas_whatsapp/', n= n)



sistema = f"""
# INSTRUCOES

- voce é um assintente encarregado de simular uma conversa no whatsapp de uma pessoa.
- Voce vai ver a informação abaixo de um historico da conversa.
- Voce deve simular a continuacao da conversa como se fosse o usuario chamado {usuario}.
- Abaixo voce vai ver as ultimas mensangens trocadas no grupo.
- Sua tarefa é ficar pronto para responder de forma coerente e sem deixar os outros notarem que voce é uma IA (se perguntarem, negue até a morte).
- Seja coerente com o contexto, isto é, continue a conversa se precisar.
- Nunca fale de coisas que uma IA falaria, como "receitas para bolos" ou qualquer outra coisa que precise de conhecimentos da internet.


## ESTILO

{estilo}

## HISTORICO

As ultimas {n} mensagens foram:
{historico.replace("átila(Est(","Átila")}
"""




st.chat_message('assistant', avatar=avatar_assistent).write(frase_inicial)

# Inicializa o histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": sistema}]

# Exibe histórico de mensagens com os avatares correspondentes
for msg in st.session_state.messages[1:]:
    avatar = avatar_user if msg['role'] == 'user' else avatar_assistent
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

# Captura a entrada do usuário no chat e gera uma resposta
prompt = st.chat_input()

if prompt:
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=avatar_user).write(prompt)

    # Faz uma requisição à API OpenAI para gerar a resposta do assistente
    with st.chat_message("assistant", avatar=avatar_assistent):
        stream = client.chat.completions.create(
            model=modelo,
            messages=st.session_state.messages,
            temperature=0.7,
            stream=True
        )

        # Exibe a resposta em tempo real
        response = st.write_stream(stream)

    # Adiciona a resposta do assistente ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})

#st.write(st.session_state.messages)