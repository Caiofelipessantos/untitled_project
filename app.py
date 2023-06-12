from flask import Flask, url_for, redirect, render_template, request
import psycopg2 as pg

# conectando com o banco de dados
try:
    con = pg.connect(
        database = "hfcebkzm",
        user = "hfcebkzm",
        password = "Pnmx4ymiv3XCgPHDgBN5qhpBDpcWhpgI",
        host = "silly.db.elephantsql.com",
        port = "5432"
    )
    print("Banco de dados conectado!")
except Exception as erro:
    print(erro) 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def about():
    return render_template('about.html')

# Cadastro
@app.route('/cadastrar')
def show_signup_form():
    return render_template('signup/signup.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        if request.form['senha'] != request.form['confirma-senha']:
            error = 'Senhas não coincidem'
        else:
            cur = con.cursor()

            sql = 'INSERT INTO tb_usuario(NOME, SOBRENOME, EMAIL, SENHA) VALUES (%s, %s, %s, %s) RETURNING ID_USUARIO;'
            cur.execute(cur.mogrify(sql, (request.form['nome'], request.form['sobrenome'], request.form['email'], request.form['senha'])))

            # Retornar o ID inserido
            id = cur.fetchone()[0]
            print(f"ID = {id}")
            print("Operação realizada com sucesso!")
            con.commit()
            return redirect(url_for('login'))
    return render_template('signup/signup.html', error=error)

# Login
@app.route('/login')
def show_login_form():
    return render_template('login/login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = con.cursor()

        sql = 'SELECT EMAIL, SENHA FROM tb_usuario WHERE EMAIL=%s AND SENHA=%s;'
        cur.execute(cur.mogrify(sql, (request.form['email'], request.form['senha'])))

        # Retornar ID do usuário requisitado
        id = cur.fetchone()
        print(f"ID = {id}")
        print("Operação realizada com sucesso!")
        con.commit()

        # Se ID não for encontrado
        if id == None:
            error = "Nome de usuário e senha incorretos"
        else:
            return redirect(url_for('home'))

    return render_template('login/login.html', error=error)

# Página inicial
@app.route('/home')
def home():
    return render_template('home.html')