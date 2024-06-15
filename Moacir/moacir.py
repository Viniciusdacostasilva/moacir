import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import pytz 
import sqlite3
import random

intents = discord.Intents.default()
intents.messages = True  # Habilita a intenção de receber mensagens
intents.guilds = True  # Habilita a intenção de receber informações sobre servidores (guilds)
pala= ['né moacir', 'né moacir?', 'ne moacir', 'ne, moacir', 'né, moacir?', 'né, moacir?', 'ne, moacir?']
# Lista para armazenar as notícias

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

TOKEN = 'MTI0NTcyNzYwMTg3NjUzNzQwOQ.G8uL25.v_R2fysr3Rk4OCbzE39Wv6Ic5FvGEsXNx8SY9c'

# Substitua 'specific_user_id' pelo ID do usuário específico
SPECIFIC_USER_ID = '1162898741498482778'
 
# Define o fuso horário do Brasil
fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

# Data de destino
target_date = datetime(2024, 6, 1, 9, 0, 0, tzinfo=fuso_horario_brasil)

# Variável para controlar se a contagem regressiva já foi enviada
contagem_enviada = False

#////////////////////////////////////////////////////////////////////////

conn_resultados = sqlite3.connect('jogodobicho.db')
c_resultados = conn_resultados.cursor()

# Cria a tabela de porcentagem de sorte se ela ainda não existir


#////////////////////////////////////////////////////////////////////////

# Conectando ao banco de dados SQLite (ele será criado se não existir)
conn = sqlite3.connect('noticias.db')
c = conn.cursor()

# Criando a tabela de notícias se ela não existir


#////////////////////////////////////////////////////////////////////////

# Banco de dados para biscoito da sorte
conn_biscoito = sqlite3.connect('jogodobicho.db')
c_biscoito = conn_biscoito.cursor()


#/////////////////////////////////////////////////////////////////////

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    global contagem_enviada
    
    # Verifica se a mensagem foi enviada pelo usuário específico
    if message.author.id == int(SPECIFIC_USER_ID):
        await message.channel.send('Teste fora')

    # Processa o comando apenas se a mensagem não for do próprio bot
    if message.author == bot.user:
        return

    # Executa o código para 'né moacir' ou 'ne moacir'
    if 'né moacir' in message.content.lower() or 'ne moacir' in message.content.lower():
        await process_ne_moacir_command(message)

    # Verifica se a palavra-chave foi detectada e se a contagem regressiva já foi enviada
    if message.content == 'moacir' and not contagem_enviada:
        print("Palavra 'moacir' detectada!")  # Mensagem de debug
        await process_moacir_command(message)
        
        # Marca a contagem regressiva como enviada
        contagem_enviada = False
        
        # Inicia a contagem regressiva após a detecção da palavra-chave
        await contagem_regressiva(message.channel)

    # Verifica se a mensagem começa com o prefixo do bot antes de processar comandos
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)


async def process_ne_moacir_command(message):
    verifyIfWordExist = False
    content = message.content.lower()

    for keyword in pala:
        if keyword in content:
            # Se a mensagem contém uma das palavras
            conteudo_anterior = content.split(keyword)[0].strip()
            if conteudo_anterior:
                # Pega as duas últimas palavras do que o usuário disse antes da palavra
                palavras_anteriores = conteudo_anterior.split()[-2:]
                if len(palavras_anteriores) >= 2:
                    nova_frase = 'É ' + ' '.join(palavras_anteriores) + ' né'
                    verifyIfWordExist = True
                    await message.channel.send(nova_frase)
                    await message.channel.send("https://cdn.discordapp.com/attachments/1026944137129369603/1245739837705683076/image.png?ex=66646522&is=666313a2&hm=02fe1f53c9b87befd0dec8746a43449145aced0763c37b839022cbcddfe44dbf&")
                else:
                    await message.channel.send("Você não disse o suficiente para repetir.")
            break

    # Aguarda a próxima mensagem apenas se a palavra-chave for detectada
    if verifyIfWordExist:
        def check(m):
            return m.author == message.author and m.channel == message.channel
        response = await bot.wait_for('message', check=check)

        if response.content.lower() == 'é':
            await response.add_reaction('🕰️')

    return verifyIfWordExist

async def process_moacir_command(message):
    await message.channel.send("Contagem regressiva para comer o Moacir:")
    # Envia a foto
    await message.channel.send("https://cdn.discordapp.com/attachments/1026944137129369603/1245730085017882675/image.png?ex=6659d00c&is=66587e8c&hm=752f5e3d53b52e222d8d09b87b7a0f16a5e86be798adae33df0078325f0c20dc")

# Função assíncrona para realizar a contagem regressiva
async def contagem_regressiva(channel):
    # Obtém a data e hora atual no fuso horário do Brasil
    now = datetime.now(fuso_horario_brasil)

    # Calcula a diferença entre a data atual e a data alvo
    remaining_time = target_date - now

    # Formata a diferença de tempo em dias, horas, minutos e segundos
    days, remainder = divmod(remaining_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Envia a contagem regressiva para o canal
    await channel.send(f"Moacir já foi queijado com sucesso")

@bot.command(name='mamanews')
async def news(ctx, mes: str = None):
    if mes:
        # Filtra as notícias pelo mês fornecido
        try:
            mes = mes.lower()
            # Mapear o nome do mês para o número do mês
            meses = {
                "janeiro": "01",
                "fevereiro": "02",
                "março": "03",
                "abril": "04",
                "maio": "05",
                "junho": "06",
                "julho": "07",
                "agosto": "08",
                "setembro": "09",
                "outubro": "10",
                "novembro": "11",
                "dezembro": "12"
            }
            mes_numero = meses.get(mes)
            if not mes_numero:
                await ctx.send("Mês inválido. Por favor, forneça um mês válido.")
                return
            c.execute('SELECT id, data, texto FROM noticias WHERE strftime("%m", data) = ?', (mes_numero,))
        except Exception as e:
            await ctx.send("Ocorreu um erro ao processar seu pedido.")
            return
    else:
        # Obter o mês atual
        mes_atual = datetime.now(fuso_horario_brasil).strftime('%m')
        c.execute('SELECT id, data, texto FROM noticias WHERE strftime("%m", data) = ?', (mes_atual,))
    
    rows = c.fetchall()
    if rows:
        resposta = "\n".join([f"Notícia {row[0]} - Data: {row[1]}: {row[2]}" for row in rows])
        await ctx.send(resposta)
    else:
        await ctx.send('Não há notícias disponíveis para este mês.')

#Comando para adicionar noticias
@bot.command(name='add_news')
async def add_news(ctx, *, nova_noticia: str):
    data_atual = datetime.now(fuso_horario_brasil).strftime('%Y-%m-%d')
    c.execute('INSERT INTO noticias (texto, data) VALUES (?, ?)', (nova_noticia, data_atual))
    conn.commit()
    await ctx.send(f'Notícia adicionada em {data_atual}: {nova_noticia}')

#Comando para Remover
@bot.command(name='remove_news')
async def remove_news(ctx, noticia_id: int):
    c.execute('DELETE FROM noticias WHERE id = ?', (noticia_id,))
    conn.commit()
    if c.rowcount > 0:
        await ctx.send(f'Notícia com ID {noticia_id} removida com sucesso.')
    else:
        await ctx.send(f'Não foi encontrada nenhuma notícia com ID {noticia_id}.')

#Comando para editar
@bot.command(name='edit_news')
async def edit_news(ctx, noticia_id: int, *, novo_texto: str):
    c.execute('UPDATE noticias SET texto = ? WHERE id = ?', (novo_texto, noticia_id))
    conn.commit()
    if c.rowcount > 0:
        await ctx.send(f'Notícia com ID {noticia_id} editada com sucesso.')
    else:
        await ctx.send(f'Não foi encontrada nenhuma notícia com ID {noticia_id}.')

#comando para sorte
@bot.command(name='sorte')
async def sorte(ctx):
    try:
        # Extract user's name and message from the command
        user_name = ctx.author.nick
        if user_name is None:
            user_name = ctx.author.name
        user_message = ctx.message.content[len("#comando para sorte") + 1:]

        # Connect to the database
        conn_resultados = sqlite3.connect('jogodobicho.db')
        c_resultados = conn_resultados.cursor()

        # Get user's ID and current date
        user_id = ctx.author.id
        data_atual = datetime.now(fuso_horario_brasil).strftime('%Y-%m-%d')

        # Check if the user's luck percentage has already been calculated for the current day
        c_resultados.execute('SELECT porcentagem_sorte FROM sorte WHERE user_id = ? AND data = ?', (user_id, data_atual))
        resultado = c_resultados.fetchone()

        if resultado:
            porcentagem_sorte = resultado[0]
        else:
            porcentagem_sorte = random.randint(0, 100)

        # Store the luck percentage for the user
        c_resultados.execute('INSERT INTO sorte (user_id, data, porcentagem_sorte) VALUES (?, ?, ?)', (user_id, data_atual, porcentagem_sorte))
        conn_resultados.commit()

        # Personalize the response with user's name and message
        personalized_response = f"É **{user_name},** parece que a chance de você pisar numa bosta de cigano hoje é de {porcentagem_sorte}%"

        await ctx.send(personalized_response)

    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao processar o comando: {e}")

    finally:
        c_resultados.close()
        conn_resultados.close()
    
#///////////////////////////////////////////////////////////////////////////////////////////////////
#Comando para biscoito ele vai sortear uma frase dita no discord
@bot.command(name='biscoito')
async def biscoito(ctx):
    try:
        conn_resultados = sqlite3.connect('jogodobicho.db')
        c_resultados = conn_resultados.cursor()
        
        # Cria a tabela 'megasena' se ela ainda não existir
        c_resultados.execute('''
            CREATE TABLE IF NOT EXISTS megasena (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numeros TEXT NOT NULL,
                data TEXT NOT NULL,
                user_id INTEGER NOT NULL
            )
        ''')
        conn_resultados.commit()

        # Cria a tabela 'frases_atribuidas' se ela ainda não existir
        c_resultados.execute('''
            CREATE TABLE IF NOT EXISTS frases_atribuidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                frase TEXT NOT NULL,
                data TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                biscoito_id INTEGER NOT NULL,
                FOREIGN KEY(biscoito_id) REFERENCES biscoito(id)
            )
        ''')
        conn_resultados.commit()

        c_biscoito = conn_resultados.cursor()
        
        user_id = ctx.author.id
        data_atual = datetime.now(fuso_horario_brasil).strftime('%Y-%m-%d')
        
        # Verifica se o usuário já recebeu uma frase no dia atual
        c_biscoito.execute('SELECT id, frase FROM frases_atribuidas WHERE user_id = ? AND data = ?', (user_id, data_atual))
        result = c_biscoito.fetchone()
        
        if result:
            mensagem_id = result[0]
            mensagem = result[1]
        else:
            c_biscoito.execute('SELECT id, frase FROM biscoito ORDER BY RANDOM() LIMIT 1')
            result = c_biscoito.fetchone()
            mensagem_id = result[0]
            mensagem = result[1]
            
            # Armazena a frase sorteada para o usuário no dia atual
            biscoito_id = mensagem_id
            c_biscoito.execute('INSERT INTO frases_atribuidas (frase, data, user_id, biscoito_id) VALUES (?, ?, ?, ?)', (mensagem, data_atual, user_id, biscoito_id))
            conn_resultados.commit()

        # Agora, obtenha ou gere os números da sorte como antes
        c_resultados.execute('SELECT numeros FROM megasena WHERE user_id = ? AND data = ?', (user_id, data_atual))
        resultado = c_resultados.fetchone()

        if resultado:
            numeros_text = resultado[0]
        else:
            numeros = [random.randint(0, 99) for _ in range(6)]
            numeros_text = ', '.join(map(str, numeros))

            # Armazena os números sorteados para o usuário
            c_resultados.execute('INSERT INTO megasena (numeros, data, user_id) VALUES (?, ?, ?)', (numeros_text, data_atual, user_id))
            conn_resultados.commit()

        await ctx.send(f'{mensagem} \n:fortune_cookie: Números da sorte: {numeros_text}')
    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao processar o comando: {e}")
    finally:
        c_biscoito.close()
        c_resultados.close()
        conn_resultados.close()

@bot.command(name='add_biscoito')
async def add_biscoito(ctx, *, frase: str):
    c_biscoito.execute('INSERT INTO biscoito (frase) VALUES (?)', (frase,))
    conn_biscoito.commit()
    c_biscoito.execute('SELECT id FROM biscoito WHERE frase = ?', (frase,))
    frase_id = c_biscoito.fetchone()[0]
    await ctx.send(f'Frase adicionada ao biscoito da sorte: {frase} (ID: {frase_id})')

@bot.command(name='rem_biscoito')
async def rem_biscoito(ctx, id: int):
    c_biscoito.execute('DELETE FROM biscoito WHERE id = ?', (id,))
    conn_biscoito.commit()
    await ctx.send(f'Frase removida do biscoito da sorte: ID {id}')

@bot.command(name='edit_biscoito')
async def edit_biscoito(ctx, id: int, *, nova_frase: str):
    c_biscoito.execute('UPDATE biscoito SET frase = ? WHERE id = ?', (nova_frase, id))
    conn_biscoito.commit()
    await ctx.send(f'Frase editada no biscoito da sorte: {nova_frase} (ID: {id})')

@bot.command(name='frases')
async def frases(ctx):
    try:
        c_biscoito.execute('SELECT id, frase FROM biscoito')
        frases = c_biscoito.fetchall()
        
        if frases:
            mensagem = "\n".join([f"ID: {frase[0]}, Frase: {frase[1]}" for frase in frases])
            await ctx.send("Frases disponíveis:\n" + mensagem)
        else:
            await ctx.send("Desculpe, não há frases disponíveis.")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao processar o comando: {e}")

    
@bot.command(name='mamahelp')
async def mamahelp(ctx):
    help_text = """
    Aqui estão os comandos disponíveis:
    - !sorte: Mostra a probabilidade de ter pisado numa bosta de cigano.
    - !frases: Exibe as frases disponíveis para os biscoitos.
    - !biscoito: Exibe uma frase aleatória do biscoito da sorte.
    - !add_biscoito <frase>: Adiciona uma nova frase ao biscoito da sorte.
    - !rem_biscoito <id>: Remove a frase do biscoito da sorte pelo ID.
    - !edit_biscoito <id> <nova_frase>: Edita a frase do biscoito da sorte pelo ID.
    - !add_news <texto>: Adiciona uma notícia com o texto fornecido.
    - !mamanews [mes]: Mostra notícias do mês atual ou do mês especificado.
    - !remove_news <id>: Remove a notícia pelo ID.
    - !edit_news <id> <novo_texto>: Edita a notícia pelo ID.
    - !mamahelp: Mostra esta mensagem de ajuda.
    """
    await ctx.send(help_text)
    
    
bot.run(TOKEN)