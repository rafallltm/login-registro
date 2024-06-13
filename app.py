import os
from flask import Flask, render_template, request, redirect, session
import redis

app = Flask(__name__)

# Gerar uma chave secreta aleatória
def generate_secret_key():
    return os.urandom(24)

# Verificar se a chave secreta está definida na variável de ambiente
if 'SECRET_KEY' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']
else:
    # Se não estiver definida, gerar uma chave secreta e definir como padrão
    app.secret_key = generate_secret_key()
    # Exibir a chave secreta no terminal para ser configurada como variável de ambiente
    print("Chave secreta gerada:", app.secret_key)
    print("Configure-a como variável de ambiente usando: export SECRET_KEY='sua_chave_secreta_aqui'")



# Conexão com Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Funções de registro e login
def registrar_usuario(email, senha):
    if r.hexists('usuarios', email):
        return False  # Usuário já registrado
    else:
        r.hset('usuarios', email, senha)
        return True

def fazer_login(email, senha):
    if r.hexists('usuarios', email):
        if r.hget('usuarios', email) == senha:
            return True
    return False  # Usuário não encontrado ou senha incorreta



# Rotas da aplicação
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if registrar_usuario(email, senha):
            session['email'] = email
            return redirect('/perfil')
        else:
            return "Usuário já registrado!"
    return render_template('registrar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if fazer_login(email, senha):
            session['email'] = email
            return redirect('/perfil')
        else:
            return "Email ou senha incorretos."
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    if 'email' in session:
        return f"Bem-vindo, {session['email']}!"
    else:
        return "Faça login para acessar seu perfil."

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

