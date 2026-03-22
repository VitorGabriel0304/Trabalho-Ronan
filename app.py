from flask import Flask, render_template, request, redirect, flash, url_for, session

from functools import wraps

def login_obrigatorio(f):
    @wraps(f)
    def funcao_protegida(*args, **kwargs):
        if "usuario" not in session:
            flash("Você precisa estar logado!", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return funcao_protegida


app = Flask(__name__)
app.secret_key = "segredo"

# =========================
# "BANCO DE DADOS"
# =========================
usuarios = [
    {"nome": "Teste", "email": "teste", "senha": "teste"},
    {"nome": "Vitor", "email": "vitor@email.com", "senha": "123"},
    {"nome": "Rhian", "email": "rhian@email.com", "senha": "123"},
    {"nome": "Ronan", "email": "ronan@email.com", "senha": "123"},
    {"nome": "Lui", "email": "lui@email.com", "senha": "123"},
    {"nome": "Rian", "email": "rian@email.com", "senha": "123"},
    {"nome": "Arthur", "email": "arthur@email.com", "senha": "123"}
]

generos = [
    {"nome": "Ação"},
    {"nome": "Comédia"},
    {"nome": "Terror"},
    {"nome": "Ficção"},
    {"nome": "Drama"}
]

filmes = [
    {"titulo": "Gladiador", "ano": 2000, "genero": "Ação", "nota": 9, "capa": "/static/imgs/Gladiador.jpg"},
    {"titulo": "Interstellar", "ano": 2014, "genero": "Ficção", "nota": 9, "capa": "/static/imgs/interstellar.jpg"},
    {"titulo": "Avatar", "ano": 2009, "genero": "Ficção", "nota": 8, "capa": "/static/imgs/FilmeAvatar.jpg"},
    {"titulo": "O Lobo de Wall Street", "ano": 2013, "genero": "Comédia", "nota": 8, "capa": "/static/imgs/The_Wolf_of_Wall_Street.jpg"},
    {"titulo": "Annabelle", "ano": 2014, "genero": "Terror", "nota": 7, "capa": "/static/imgs/Annabelle.jpg"},
    {"titulo": "Forrest Gump", "ano": 1994, "genero": "Drama", "nota": 9, "capa": "/static/imgs/forrestgump.jpg"},
    {"titulo": "Homem de Ferro", "ano": 2008, "genero": "Ação", "nota": 8, "capa": "/static/imgs/Iron_Man.jpg"}
]

# =========================
# PÁGINAS PÚBLICAS
# =========================

@app.route("/")
def index():
    return render_template("index.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        for usuario in usuarios:
            if usuario["email"] == email and usuario["senha"] == senha:
                
                # 🔥 SALVA NA SESSÃO
                session["usuario"] = usuario["nome"]

                flash("Login realizado com sucesso!", "success")
                return redirect(url_for('listar_usuarios'))

        flash("Email ou senha inválidos!", "danger")
        return redirect(url_for('login'))

    return render_template("login.html")


# =========================
# CADASTRO
# =========================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")

        if not nome or not email or not senha:
            flash("Preencha todos os campos!", "danger")
            return redirect(url_for('cadastro'))

        if senha != confirmar:
            flash("As senhas não coincidem!", "danger")
            return redirect(url_for('cadastro'))

        usuarios.append({
            "nome": nome,
            "email": email,
            "senha": senha
        })

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('login'))

    return render_template("cadastro.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():
    session.pop("usuario", None)  
    flash("Logout realizado!", "info")
    return redirect(url_for('login'))


# =========================
# USUÁRIOS
# =========================

@app.route("/usuarios/listar")
def listar_usuarios():
    return render_template("usuarios/listar_usuarios.html", usuarios=usuarios)


@app.route("/usuarios/inserir", methods=["GET", "POST"])
@login_obrigatorio
def inserir_usuarios():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        if not nome or not email:
            flash("Preencha todos os campos!", "danger")
            return redirect(url_for('inserir_usuarios'))

        usuarios.append({
            "nome": nome,
            "email": email,
            "senha": "123"
        })

        flash("Usuário adicionado!", "success")
        return redirect(url_for('listar_usuarios'))

    return render_template("usuarios/inserir_usuario.html")


# =========================
# FILMES
# =========================

@app.route("/filmes/listar")
@login_obrigatorio
def listar_filmes():
    return render_template("entidade2/listar_entidade2.html", filmes=filmes)


@app.route("/filmes/inserir", methods=["GET", "POST"])
@login_obrigatorio
def inserir_filmes():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        ano = request.form.get("ano")
        genero = request.form.get("genero")
        nota = request.form.get("nota")
        capa = request.form.get("capa")

        if not titulo or not ano or not genero:
            flash("Preencha os campos obrigatórios!", "danger")
            return redirect(url_for('inserir_filmes'))

        filmes.append({
            "titulo": titulo,
            "ano": ano,
            "genero": genero,
            "nota": nota,
            "capa": capa if capa else ""
        })

        flash("Filme adicionado!", "success")
        return redirect(url_for('listar_filmes'))

    return render_template("entidade2/inserir_entidade2.html", generos=generos)


# =========================
# GÊNEROS
# =========================

@app.route("/generos/listar")
@login_obrigatorio
def listar_generos():
    return render_template("entidade3/listar_entidade3.html", generos=generos)


@app.route("/generos/inserir", methods=["GET", "POST"])
@login_obrigatorio
def inserir_generos():
    if request.method == "POST":
        nome = request.form.get("nome")

        if not nome:
            flash("Digite o nome do gênero!", "danger")
            return redirect(url_for('inserir_generos'))

        generos.append({"nome": nome})
        flash("Gênero adicionado!", "success")
        return redirect(url_for('listar_generos'))

    return render_template("entidade3/inserir_entidade3.html")


# =========================
# EQUIPE
# =========================

@app.route("/equipe")
@login_obrigatorio
def equipe():
    return render_template("sobre_equipe.html")


# =========================
# RODAR SERVIDOR
# =========================

if __name__ == "__main__":
    app.run(debug=True)