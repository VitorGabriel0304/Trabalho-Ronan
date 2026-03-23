from flask import Flask, render_template, request, redirect, flash, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "segredo"

# -----------------------------
# Decorador de login
# -----------------------------
def login_obrigatorio(f):
    @wraps(f)
    def funcao_protegida(*args, **kwargs):
        if "usuario" not in session:
            flash("Você precisa estar logado!", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return funcao_protegida

# -----------------------------
# "Banco de dados"
# -----------------------------
usuarios = [
    {"nome": "Teste", "email": "teste", "senha": "teste", "idade": 25},
    {"nome": "Vitor", "email": "vitor@email.com", "senha": "123", "idade": 21},
    {"nome": "Rhian", "email": "rhian@email.com", "senha": "123", "idade": 20},
]

generos = [
    {"nome": "Ação"}, {"nome": "Comédia"}, {"nome": "Terror"}, 
    {"nome": "Ficção"}, {"nome": "Drama"}, {"nome": "Documentário"}
]

filmes = [
    {"titulo": "Gladiador", "ano": 2000, "genero": "Ação", "faixa_etaria": 16, "capa": "/static/imgs/Gladiador.jpg"},
    {"titulo": "Interstellar", "ano": 2014, "genero": "Ficção", "faixa_etaria": 10, "capa": "/static/imgs/interstellar.jpg"},
    {"titulo": "Avatar", "ano": 2009, "genero": "Ficção", "faixa_etaria": 12, "capa": "/static/imgs/FilmeAvatar.jpg"},
    {"titulo": "O Lobo de Wall Street", "ano": 2013, "genero": "Comédia", "faixa_etaria": 18, "capa": "/static/imgs/The_Wolf_of_Wall_Street.jpg"},
    {"titulo": "Annabelle", "ano": 2014, "genero": "Terror", "faixa_etaria": 16, "capa": "/static/imgs/Annabelle.jpg"},
    {"titulo": "Forrest Gump", "ano": 1994, "genero": "Drama", "faixa_etaria": 10, "capa": "/static/imgs/forrestgump.jpg"},
    {"titulo": "Homem de Ferro", "ano": 2008, "genero": "Ação", "faixa_etaria": 12, "capa": "/static/imgs/Iron_Man.jpg"}
]

series = [
    {"titulo": "Breaking Bad", "ano": 2008, "genero": "Drama", "faixa_etaria": 16, "temporadas": 5, "capa": "/static/imgs/Breaking_Bad.jpg"},
    {"titulo": "Friends", "ano": 1994, "genero": "Comédia", "faixa_etaria": 10, "temporadas": 10, "capa": "/static/imgs/Friends.jpg"},
    {"titulo": "Stranger Things", "ano": 2016, "genero": "Ficção", "faixa_etaria": 12, "temporadas": 4, "capa": "/static/imgs/Stranger_Things.jpg"},
    {"titulo": "Planet Earth", "ano": 2006, "genero": "Documentário", "faixa_etaria": 0, "temporadas": 1, "capa": "/static/imgs/Planet_Earth.jpg"},
    {"titulo": "The Office", "ano": 2005, "genero": "Comédia", "faixa_etaria": 12, "temporadas": 9, "capa": "/static/imgs/The_Office.jpg"},
    {"titulo": "Chernobyl", "ano": 2019, "genero": "Drama", "faixa_etaria": 16, "temporadas": 1, "capa": "/static/imgs/Chernobyl.jpg"},
    {"titulo": "Our Planet", "ano": 2019, "genero": "Documentário", "faixa_etaria": 0, "temporadas": 1, "capa": "/static/imgs/Our_Planet.jpg"}
]

# -----------------------------
# Páginas públicas
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sobre/equipe")
def sobre_equipe():
    return render_template("sobre_equipe.html")

# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario_encontrado = next((u for u in usuarios if u["email"] == email and u["senha"] == senha), None)
        if usuario_encontrado:
            session["usuario"] = {"nome": usuario_encontrado["nome"], "idade": int(usuario_encontrado["idade"])}
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("listar_usuarios"))
        flash("Email ou senha inválidos!", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")

# -----------------------------
# Cadastro
# -----------------------------
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")
        idade = request.form.get("idade")
        if not nome or not email or not senha or not idade:
            flash("Preencha todos os campos!", "danger")
            return redirect(url_for("cadastro"))
        if senha != confirmar:
            flash("As senhas não coincidem!", "danger")
            return redirect(url_for("cadastro"))
        usuarios.append({"nome": nome, "email": email, "senha": senha, "idade": int(idade)})
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("login"))
    return render_template("cadastro.html")

# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Logout realizado!", "info")
    return redirect(url_for("login"))

# -----------------------------
# Usuários
# -----------------------------
@app.route("/usuarios/listar", endpoint="listar_usuarios")
@login_obrigatorio
def listar_usuarios():
    return render_template("usuarios/listar_usuarios.html", usuarios=usuarios)

@app.route("/usuarios/inserir", methods=["GET", "POST"], endpoint="inserir_usuarios")
@login_obrigatorio
def inserir_usuarios():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        idade = request.form.get("idade")
        if not nome or not email or not idade:
            flash("Preencha todos os campos!", "danger")
            return redirect(url_for("inserir_usuarios"))
        usuarios.append({"nome": nome, "email": email, "senha": "123", "idade": int(idade)})
        flash("Usuário adicionado!", "success")
        return redirect(url_for("listar_usuarios"))
    return render_template("usuarios/inserir_usuario.html")

# -----------------------------
# Filmes
# -----------------------------
@app.route("/filmes/listar", endpoint="listar_filmes")
@login_obrigatorio
def listar_filmes():
    genero_filtro = request.args.get("genero", "todos")
    lista_generos = [g["nome"] for g in generos]
    usuario_logado = session.get("usuario")
    if not isinstance(usuario_logado, dict):
        flash("Erro na sessão. Faça login novamente.", "danger")
        return redirect(url_for("logout"))
    idade_usuario = int(usuario_logado.get("idade", 0))
    filmes_filtrados = [f for f in filmes if genero_filtro == "todos" or f["genero"] == genero_filtro]
    filmes_filtrados = [f for f in filmes_filtrados if idade_usuario >= f["faixa_etaria"]]
    return render_template("entidade2/listar_entidade2.html", filmes=filmes_filtrados, generos=lista_generos, genero_filtro=genero_filtro)

@app.route("/filmes/inserir", methods=["GET", "POST"], endpoint="inserir_filmes")
@login_obrigatorio
def inserir_filmes():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        ano = request.form.get("ano")
        genero = request.form.get("genero")
        faixa_etaria = request.form.get("faixa_etaria")
        capa = request.form.get("capa")
        if not titulo or not ano or not genero or not faixa_etaria:
            flash("Preencha os campos obrigatórios!", "danger")
            return redirect(url_for("inserir_filmes"))
        filmes.append({"titulo": titulo, "ano": int(ano), "genero": genero, "faixa_etaria": int(faixa_etaria), "capa": capa if capa else ""})
        flash("Filme adicionado!", "success")
        return redirect(url_for("listar_filmes"))
    return render_template("entidade2/inserir_entidade2.html", generos=[g["nome"] for g in generos])

# -----------------------------
# Séries
# -----------------------------
@app.route("/series/listar", endpoint="listar_series")
@login_obrigatorio
def listar_series():
    genero_filtro = request.args.get("genero", "todos")
    lista_generos = [g["nome"] for g in generos]
    usuario_logado = session.get("usuario")
    if not isinstance(usuario_logado, dict):
        flash("Erro na sessão. Faça login novamente.", "danger")
        return redirect(url_for("logout"))
    idade_usuario = int(usuario_logado.get("idade", 0))
    series_filtradas = [s for s in series if genero_filtro == "todos" or s["genero"] == genero_filtro]
    series_filtradas = [s for s in series_filtradas if idade_usuario >= s["faixa_etaria"]]
    return render_template("entidade3/listar_entidade3.html", series=series_filtradas, generos=lista_generos, genero_filtro=genero_filtro)

@app.route("/series/inserir", methods=["GET", "POST"], endpoint="inserir_series")
@login_obrigatorio
def inserir_series():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        ano = request.form.get("ano")
        genero = request.form.get("genero")
        faixa_etaria = request.form.get("faixa_etaria")
        temporadas = request.form.get("temporadas")
        capa = request.form.get("capa")
        if not titulo or not ano or not genero or not faixa_etaria or not temporadas:
            flash("Preencha os campos obrigatórios!", "danger")
            return redirect(url_for("inserir_series"))
        series.append({"titulo": titulo, "ano": int(ano), "genero": genero, "faixa_etaria": int(faixa_etaria), "temporadas": int(temporadas), "capa": capa if capa else ""})
        flash("Série/Documentário adicionado!", "success")
        return redirect(url_for("listar_series"))
    return render_template("entidade3/inserir_entidade3.html", generos=[g["nome"] for g in generos])

# -----------------------------
# Rodar servidor
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)