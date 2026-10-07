from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector


# Aqui eu crio o meu aplicativo usando o Flask
app = Flask(__name__)

# Aqui eu permito que o meu JavaScript consiga conversar com o Flask
CORS(app)


# Aqui eu crio uma função para fazer a conexão com o meu banco de dados
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="urna_academica",
        use_pure=True
    )

# Aqui eu crio uma rota para buscar todos os eleitores cadastrados
@app.get('/eleitores')
def eleitores():

    # Aqui eu faço a conexão com o banco
    c = conectar()

    # Aqui eu crio o cursor para poder fazer comandos SQL
    cur = c.cursor(dictionary=True)

    # Aqui eu busco os eleitores no banco e organizo pelo nome
    cur.execute(
        'SELECT id, nome, matricula, votou '
        'FROM eleitor '
        'ORDER BY nome'
    )

    # Aqui eu guardo todos os resultados encontrados
    d = cur.fetchall()

    # Aqui eu fecho o cursor e a conexão com o banco
    cur.close()
    c.close()

    # Aqui eu mando os dados de volta para o JavaScript
    return jsonify(d)


# Aqui eu crio a rota para cadastrar um novo eleitor
@app.post('/eleitores')
def add_eleitor():

    # Aqui eu pego os dados enviados pelo JavaScript
    d = request.get_json()

    # Aqui eu pego o nome e a matrícula que foram enviados
    nome = d.get('nome', '').strip()
    matricula = d.get('matricula', '').strip()

    # Aqui eu faço a conexão com o banco
    c = conectar()

    # Aqui eu crio o cursor para fazer os comandos SQL
    cur = c.cursor(dictionary=True)

    # Aqui eu conto quantos eleitores já existem
    cur.execute('SELECT COUNT(*) total FROM eleitor')

    # Aqui eu verifico se já chegou no limite de 10 eleitores
    if cur.fetchone()['total'] >= 10:
        cur.close()
        c.close()

        return jsonify({
            'erro': 'Limite de 10 eleitores atingido.'
        }), 400

    try:

        # Aqui eu salvo o novo eleitor no banco
        cur.execute(
            'INSERT INTO eleitor (nome, matricula) '
            'VALUES (%s, %s)',
            (nome, matricula)
        )

        # Aqui eu confirmo a alteração no banco
        c.commit()

    except mysql.connector.IntegrityError:

        # Se a matrícula já existir, eu mostro uma mensagem de erro
        cur.close()
        c.close()

        return jsonify({
            'erro': 'Matrícula já cadastrada.'
        }), 400

    # Depois de terminar, eu fecho o cursor e a conexão
    cur.close()
    c.close()

    # Aqui eu aviso que o cadastro foi realizado
    return jsonify({
        'mensagem': 'Eleitor cadastrado.'
    }), 201


# Aqui eu crio uma rota para mostrar os representantes
@app.get('/representantes')
def representantes():

    # Eu faço a conexão com o banco
    c = conectar()

    # Eu crio o cursor para executar o SQL
    cur = c.cursor(dictionary=True)

    # Aqui eu busco todos os representantes e organizo pelo número
    cur.execute(
        'SELECT id, nome, numero '
        'FROM representante '
        'ORDER BY numero'
    )

    # Aqui eu guardo os resultados encontrados
    d = cur.fetchall()

    # Eu fecho o cursor e a conexão
    cur.close()
    c.close()

    # Eu envio os representantes para o JavaScript
    return jsonify(d)


# Aqui eu crio a rota para cadastrar um representante
@app.post('/representantes')
def add_rep():

    # Eu pego os dados enviados pelo JavaScript
    d = request.get_json()

    # Eu faço a conexão com o banco
    c = conectar()

    # Eu crio o cursor
    cur = c.cursor(dictionary=True)

    # Aqui eu conto quantos representantes já existem
    cur.execute(
        'SELECT COUNT(*) total FROM representante'
    )

    # Aqui eu verifico se já existem 5 representantes
    if cur.fetchone()['total'] >= 5:
        cur.close()
        c.close()

        return jsonify({
            'erro': 'Limite de 5 representantes atingido.'
        }), 400

    try:

        # Aqui eu cadastro o representante no banco
        cur.execute(
            'INSERT INTO representante (nome, numero) '
            'VALUES (%s, %s)',
            (d['nome'], d['numero'])
        )

        # Eu confirmo a alteração
        c.commit()

    except mysql.connector.IntegrityError:

        # Se o número já existir, eu mostro uma mensagem
        cur.close()
        c.close()

        return jsonify({
            'erro': 'Número já cadastrado.'
        }), 400

    # Eu fecho o cursor e a conexão
    cur.close()
    c.close()

    # Eu aviso que o cadastro foi realizado
    return jsonify({
        'mensagem': 'Representante cadastrado.'
    }), 201

# Aqui eu crio uma rota para buscar os vice-representantes
@app.get('/vices')
def vices():

    # Eu faço a conexão com o banco
    c = conectar()

    # Eu crio o cursor
    cur = c.cursor(dictionary=True)

    # Aqui eu busco os vice-representantes pelo número
    cur.execute(
        'SELECT id, nome, numero '
        'FROM vice_representante '
        'ORDER BY numero'
    )

    # Eu guardo os resultados
    d = cur.fetchall()

    # Eu fecho o cursor e a conexão
    cur.close()
    c.close()

    # Eu envio os dados para o JavaScript
    return jsonify(d)


# Aqui eu crio a rota para cadastrar um vice-representante
@app.post('/vices')
def add_vice():

    # Eu pego os dados enviados pelo JavaScript
    d = request.get_json()

    # Eu faço a conexão com o banco
    c = conectar()

    # Eu crio o cursor
    cur = c.cursor(dictionary=True)

    # Aqui eu conto quantos vice-representantes existem
    cur.execute(
        'SELECT COUNT(*) total FROM vice_representante'
    )

    # Aqui eu verifico se já existem 5 vice-representantes
    if cur.fetchone()['total'] >= 5:
        cur.close()
        c.close()

        return jsonify({
            'erro': 'Limite de 5 vice-representantes atingido.'
        }), 400

    try:

        # Aqui eu cadastro o vice-representante
        cur.execute(
            'INSERT INTO vice_representante (nome, numero) '
            'VALUES (%s, %s)',
            (d['nome'], d['numero'])
        )

        # Eu confirmo a alteração no banco
        c.commit()

    except mysql.connector.IntegrityError:

        # Se o número já estiver cadastrado, eu mostro o erro
        cur.close()
        c.close()

        return jsonify({
            'erro': 'Número já cadastrado.'
        }), 400

    # Eu fecho o cursor e a conexão
    cur.close()
    c.close()

    # Eu aviso que o cadastro foi realizado
    return jsonify({
        'mensagem': 'Vice cadastrado.'
    }), 201



# Aqui eu crio a rota responsável por registrar o voto
@app.post('/votar')
def votar():

    # Eu pego os dados enviados pelo JavaScript
    d = request.get_json()

    # Eu faço a conexão com o banco
    c = conectar()

    # Eu crio o cursor
    cur = c.cursor(dictionary=True)

    try:

        # Aqui eu começo uma transação para garantir que tudo seja salvo corretamente
        c.start_transaction()

        # Aqui eu procuro o eleitor pela matrícula
        cur.execute(
            'SELECT id, votou '
            'FROM eleitor '
            'WHERE matricula = %s '
            'FOR UPDATE',
            (d['matricula'],)
        )

        # Eu guardo o eleitor encontrado
        e = cur.fetchone()

        # Se eu não encontrar o eleitor, mostro um erro
        if not e:
            c.rollback()

            return jsonify({
                'erro': 'Eleitor não cadastrado.'
            }), 404

        # Aqui eu verifico se esse eleitor já votou
        if e['votou']:
            c.rollback()

            return jsonify({
                'erro': 'Este eleitor já votou.'
            }), 400

        # Aqui eu verifico se o representante escolhido existe
        cur.execute(
            'SELECT id '
            'FROM representante '
            'WHERE id = %s',
            (d['representante_id'],)
        )

        # Se não encontrar o representante, eu cancelo a votação
        if not cur.fetchone():
            c.rollback()

            return jsonify({
                'erro': 'Representante inválido.'
            }), 400

        # Aqui eu verifico se o vice escolhido existe
        cur.execute(
            'SELECT id '
            'FROM vice_representante '
            'WHERE id = %s',
            (d['vice_id'],)
        )

        # Se não encontrar o vice, eu cancelo a votação
        if not cur.fetchone():
            c.rollback()

            return jsonify({
                'erro': 'Vice inválido.'
            }), 400

        # Aqui eu salvo o voto no banco
        cur.execute(
            'INSERT INTO voto (representante_id, vice_id) '
            'VALUES (%s, %s)',
            (
                d['representante_id'],
                d['vice_id']
            )
        )

        # Aqui eu marco o eleitor como alguém que já votou
        cur.execute(
            'UPDATE eleitor '
            'SET votou = TRUE '
            'WHERE id = %s',
            (e['id'],)
        )

        # Aqui eu confirmo todas as alterações
        c.commit()

        # Eu aviso que o voto foi registrado
        return jsonify({
            'mensagem': 'Voto registrado com sucesso.'
        })

    except Exception as erro:

        # Se acontecer algum erro, eu desfaço as alterações
        c.rollback()

        # Aqui eu mostro o erro no terminal para conseguir descobrir o problema
        print('ERRO AO VOTAR:', erro)

        return jsonify({
            'erro': 'Erro ao registrar voto. Verifique o banco.'
        }), 500

    finally:

        # No final eu fecho o cursor e a conexão
        cur.close()
        c.close()



# Aqui eu crio uma rota para mostrar os resultados da votação
@app.get('/resultados')
def resultados():

    # Eu faço a conexão com o banco
    c = conectar()

    # Eu crio o cursor
    cur = c.cursor(dictionary=True)

    # Aqui eu conto quantos votos cada representante recebeu
    cur.execute('''
        SELECT
            r.id,
            r.nome,
            r.numero,
            COUNT(v.id) AS votos
        FROM representante r
        LEFT JOIN voto v
            ON v.representante_id = r.id
        GROUP BY
            r.id,
            r.nome,
            r.numero
        ORDER BY
            votos DESC,
            r.numero
    ''')

    # Eu guardo os resultados dos representantes
    reps = cur.fetchall()

    # Aqui eu faço a mesma coisa para os vice-representantes
    cur.execute('''
        SELECT
            vr.id,
            vr.nome,
            vr.numero,
            COUNT(v.id) AS votos
        FROM vice_representante vr
        LEFT JOIN voto v
            ON v.vice_id = vr.id
        GROUP BY
            vr.id,
            vr.nome,
            vr.numero
        ORDER BY
            votos DESC,
            vr.numero
    ''')

    # Eu guardo os resultados dos vice-representantes
    vs = cur.fetchall()

    # Eu fecho o cursor e a conexão
    cur.close()
    c.close()

    # Eu envio os dois resultados para o JavaScript
    return jsonify({
        'representantes': reps,
        'vices': vs
    })


# INICIAR O PROGRAMA
# Aqui eu verifico se estou executando este arquivo diretamente
if __name__ == '__main__':

    # Aqui eu inicio o servidor Flask
    app.run(debug=True)