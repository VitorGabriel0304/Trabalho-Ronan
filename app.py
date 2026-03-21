from flask import Flask, render_template, request, redirect, flash, url_for

# aqui a gente cria o app do Flask
app = Flask(__name__)

# necessário pro flash funcionar
app.secret_key = "segredo"

# =========================
# "BANCO DE DADOS" 
# =========================
usuarios = [
    {"nome": "Vitor", "email": "vitor@email.com"},
    {"nome": "Rhian", "email": "rhian@email.com"},
    {"nome": "Ronan", "email": "ronan@email.com"},
    {"nome": "Lui", "email": "lui@email.com"},
    {"nome": "Rian", "email": "rian@email.com"},
    {"nome": "Arthur", "email": "arthur@email.com"}
]


generos = [
    {"nome": "Ação"},
    {"nome": "Comédia"},
    {"nome": "Terror"},
    {"nome": "Ficção"},
    {"nome": "Drama"}
]

filmes = [
    {"titulo": "Gladiador", "ano": 2000, "genero": "Ação", "nota": 9},
    {"titulo": "O Rei Leão", "ano": 1994, "genero": "Animação", "nota": 9},
    {"titulo": "Doutor Estranho no Multiverso da Loucura", "ano": 2022, "genero": "Ação", "nota": 8},
    {"titulo": "A Rede Social", "ano": 2010, "genero": "Drama", "nota": 8},
    {"titulo": "Annabelle", "ano": 2014, "genero": "Terror", "nota": 7},
    {"titulo": "O Lobo de Wall Street", "ano": 2013, "genero": "Comédia", "nota": 8},
    {"titulo": "Interestelar", "ano": 2014, "genero": "Ficção", "nota": 9},
    {"titulo": "Homem de Ferro", "ano": 2008, "genero": "Ação", "nota": 8},
    {"titulo": "La La Land", "ano": 2016, "genero": "Drama", "nota": 9},
    {"titulo": "It: A Coisa", "ano": 2017, "genero": "Terror", "nota": 7},
    {"titulo": "Curtindo a Vida Adoidado", "ano": 1986, "genero": "Comédia", "nota": 8},
    {"titulo": "Avatar", "ano": 2009, "genero": "Ficção", "nota": 8},
    {"titulo": "Capitão América: Guerra Civil", "ano": 2016, "genero": "Ação", "nota": 8},
    {"titulo": "Forrest Gump", "ano": 1994, "genero": "Drama", "nota": 9},
    {"titulo": "Annabelle 2: A Criação do Mal", "ano": 2017, "genero": "Terror", "nota": 7}
]


# =========================
# PÁGINAS PÚBLICAS
# =========================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for('listar_usuarios'))
    return render_template("login.html")

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

        usuarios.append({"nome": nome, "email": email})
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('login'))

    return render_template("cadastro.html")

@app.route("/logout")
def logout():
    flash("Logout realizado!", "info")
    return redirect(url_for('login'))

# =========================
# USUÁRIOS
# =========================
@app.route("/usuarios/listar")
def listar_usuarios():
    return render_template("usuarios/listar_usuarios.html", usuarios=usuarios)

@app.route("/usuarios/inserir", methods=["GET", "POST"])
def inserir_usuarios():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        if not nome or not email:
            flash("Preencha todos os campos!", "danger")
            return redirect(url_for('inserir_usuarios'))

        usuarios.append({"nome": nome, "email": email})
        flash("Usuário adicionado!", "success")
        return redirect(url_for('listar_usuarios'))

    return render_template("usuarios/inserir_usuario.html")

# =========================
# FILMES
# =========================
@app.route("/filmes/listar")
def listar_filmes():
    return render_template("entidade2/listar_entidade2.html", filmes=filmes)

@app.route("/filmes/inserir", methods=["GET", "POST"])
def inserir_filmes():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        ano = request.form.get("ano")
        genero = request.form.get("genero")
        nota = request.form.get("nota")

        if not titulo or not ano or not genero:
            flash("Preencha os campos obrigatórios!", "danger")
            return redirect(url_for('inserir_filmes'))

        filmes.append({
            "titulo": titulo,
            "ano": ano,
            "genero": genero,
            "nota": nota
        })
        flash("Filme adicionado!", "success")
        return redirect(url_for('listar_filmes'))

    return render_template("entidade2/inserir_entidade2.html", generos=generos)

# =========================
# GÊNEROS
# =========================
@app.route("/generos/listar")
def listar_generos():
    return render_template("entidade3/listar_entidade3.html", generos=generos)

@app.route("/generos/inserir", methods=["GET", "POST"])
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
def equipe():
    return render_template("sobre_equipe.html")

# =========================
# RODAR O SERVIDOR
# =========================
if __name__ == "__main__":
    app.run(debug=True)