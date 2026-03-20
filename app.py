from flask import Flask, render_template, request, redirect, flash

# aqui a gente cria o app do Flask (tipo iniciar o sistema)
app = Flask(__name__)

# isso aqui é necessário pro flash funcionar (mensagens tipo "deu certo")
app.secret_key = "segredo"


# =========================
# "BANCO DE DADOS" FAKE
# =========================

# aqui são os usuários já cadastrados (simulando um banco)
usuarios = [
    {"nome": "Vitor", "email": "vitor@email.com"},
    {"nome": "Ana", "email": "ana@email.com"},
    {"nome": "Carlos", "email": "carlos@email.com"},
    {"nome": "Julia", "email": "julia@email.com"},
    {"nome": "Marcos", "email": "marcos@email.com"}
]

# lista de gêneros de filme
generos = [
    {"nome": "Ação"},
    {"nome": "Comédia"},
    {"nome": "Terror"},
    {"nome": "Ficção"},
    {"nome": "Drama"}
]

# lista de filmes já cadastrados
filmes = [
    {"titulo": "Interestelar", "ano": 2014, "genero": "Ficção", "nota": 9},
    {"titulo": "Vingadores", "ano": 2012, "genero": "Ação", "nota": 8},
    {"titulo": "Titanic", "ano": 1997, "genero": "Drama", "nota": 9},
    {"titulo": "It", "ano": 2017, "genero": "Terror", "nota": 7},
    {"titulo": "Se Beber Não Case", "ano": 2009, "genero": "Comédia", "nota": 8}
]


# =========================
# PÁGINAS PÚBLICAS
# =========================

# página inicial (tipo "home" do sistema)
@app.route("/")
def index():
    return render_template("index.html")


# login (mostra a tela e "finge" o login)
@app.route("/login", methods=["GET", "POST"])
def login():

    # se o cara clicou em entrar
    if request.method == "POST":
        flash("Login realizado com sucesso!", "success")

        # joga direto pra listagem de usuários
        return redirect("/usuarios/listar")

    # só mostra a página
    return render_template("login.html")


# cadastro de usuário
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    # se enviou o formulário
    if request.method == "POST":

        # pega tudo que o cara digitou
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")

        # checa se deixou algo vazio
        if not nome or not email or not senha:
            flash("Preencha todos os campos!", "danger")
            return redirect("/cadastro")

        # confere se as senhas batem
        if senha != confirmar:
            flash("As senhas não coincidem!", "danger")
            return redirect("/cadastro")

        # adiciona o usuário na lista
        usuarios.append({"nome": nome, "email": email})

        flash("Cadastro realizado com sucesso!", "success")

        # manda pro login
        return redirect("/login")

    return render_template("cadastro.html")


# logout (basicamente só volta pro login)
@app.route("/logout")
def logout():
    flash("Logout realizado!", "info")
    return redirect("/login")


# =========================
# USUÁRIOS
# =========================

# mostra todos os usuários
@app.route("/usuarios/listar")
def listar_usuarios():

    # manda a lista pro HTML
    return render_template("usuarios/listar_usuarios.html", usuarios=usuarios)


# adicionar usuário
@app.route("/usuarios/inserir", methods=["GET", "POST"])
def inserir_usuarios():

    if request.method == "POST":

        nome = request.form.get("nome")
        email = request.form.get("email")

        # se não preencher, já bloqueia
        if not nome or not email:
            flash("Preencha todos os campos!", "danger")
            return redirect("/usuarios/inserir")

        # adiciona na lista
        usuarios.append({"nome": nome, "email": email})

        flash("Usuário adicionado!", "success")

        # volta pra listagem
        return redirect("/usuarios/listar")

    return render_template("usuarios/inserir_usuario.html")


# =========================
# FILMES
# =========================

# lista os filmes
@app.route("/filmes/listar")
def listar_filmes():
    return render_template("filmes/listar_filmes.html", filmes=filmes)


# adicionar filme
@app.route("/filmes/inserir", methods=["GET", "POST"])
def inserir_filmes():

    if request.method == "POST":

        titulo = request.form.get("titulo")
        ano = request.form.get("ano")
        genero = request.form.get("genero")
        nota = request.form.get("nota")

        # valida o básico
        if not titulo or not ano or not genero:
            flash("Preencha os campos obrigatórios!", "danger")
            return redirect("/filmes/inserir")

        # adiciona o filme
        filmes.append({
            "titulo": titulo,
            "ano": ano,
            "genero": genero,
            "nota": nota
        })

        flash("Filme adicionado!", "success")

        return redirect("/filmes/listar")

    # aqui manda também os gêneros pro select
    return render_template("filmes/inserir_filme.html", generos=generos)


# =========================
# GÊNEROS
# =========================

# lista os gêneros
@app.route("/generos/listar")
def listar_generos():
    return render_template("generos/listar_generos.html", generos=generos)


# adicionar gênero
@app.route("/generos/inserir", methods=["GET", "POST"])
def inserir_generos():

    if request.method == "POST":

        nome = request.form.get("nome")

        if not nome:
            flash("Digite o nome do gênero!", "danger")
            return redirect("/generos/inserir")

        # adiciona na lista
        generos.append({"nome": nome})

        flash("Gênero adicionado!", "success")

        return redirect("/generos/listar")

    return render_template("generos/inserir_genero.html")


# =========================
# EQUIPE
# =========================

# página da equipe (sobre quem fez o sistema)
@app.route("/equipe")
def equipe():
    return render_template("sobre_equipe.html")


# =========================
# RODAR O SERVIDOR
# =========================

if __name__ == "__main__":
    # debug=True → atualiza sozinho quando você salva
    app.run(debug=True)