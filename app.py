from flask import Flask, render_template, request, redirect, flash, url_for, session
from functools import wraps
from db import iniciar_bd, execute_query, execute_one

app = Flask(__name__)
app.secret_key = "segredo"

# Inicia o BD e as tabelas ao subir o app
try:
    iniciar_bd()
except Exception as e:
    print(f"Erro ao iniciar banco de dados: {e}")

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

# --- DADOS EM MEMÓRIA ---
usuarios_memoria = [
  {"id": 1, "nome": "Admin", "email": "admin@", "senha": "admin", "idade": 25, "funcao": "Administrador"},
  {"id": 2, "nome": "Vitor", "email": "vitor@email.com", "senha": "123", "idade": 21, "funcao": "Usuário"},
  {"id": 3, "nome": "Rhian", "email": "rhian@email.com", "senha": "123", "idade": 20, "funcao": "Usuário"},
  {"id": 4, "nome": "Julia", "email": "julia@email.com", "senha": "123", "idade": 22, "funcao": "Usuário"},
  {"id": 5, "nome": "Carlos", "email": "carlos@email.com", "senha": "123", "idade": 28, "funcao": "Gerente"},
  {"id": 6, "nome": "Fernanda", "email": "fernanda@email.com", "senha": "123", "idade": 24, "funcao": "Supervisor"},
  {"id": 7, "nome": "Lucas", "email": "lucas@email.com", "senha": "123", "idade": 19, "funcao": "Suporte"}
]

generos = [
    {"nome": "Ação"}, {"nome": "Comédia"}, {"nome": "Terror"}, 
    {"nome": "Ficção"}, {"nome": "Drama"}, {"nome": "Documentário"}
]

filmes = [
    {"id": 1, "titulo": "Gladiador", "ano": 2000, "genero": "Ação", "faixa_etaria": 16, "capa": "/static/imgs/Gladiador.jpg"},
    {"id": 2, "titulo": "Interstellar", "ano": 2014, "genero": "Ficção", "faixa_etaria": 10, "capa": "/static/imgs/Interstellar.jpg"},
    {"id": 3, "titulo": "Avatar", "ano": 2009, "genero": "Ficção", "faixa_etaria": 12, "capa": "/static/imgs/FilmeAvatar.jpg"},
    {"id": 4, "titulo": "O Lobo de Wall Street", "ano": 2013, "genero": "Comédia", "faixa_etaria": 18, "capa": "/static/imgs/The_Wolf_of_Wall_Street.jpg"},
    {"id": 5, "titulo": "Annabelle", "ano": 2014, "genero": "Terror", "faixa_etaria": 16, "capa": "/static/imgs/Annabelle.jpg"},
    {"id": 6, "titulo": "Forrest Gump", "ano": 1994, "genero": "Drama", "faixa_etaria": 10, "capa": "/static/imgs/forrestgump.jpg"},
    {"id": 7, "titulo": "Homem de Ferro", "ano": 2008, "genero": "Ação", "faixa_etaria": 12, "capa": "/static/imgs/Iron_Man.jpg"}
]

series = [
    {"id": 1, "titulo": "Breaking Bad", "ano": 2008, "genero": "Drama", "faixa_etaria": 16, "temporadas": 5, "capa": "/static/imgs/Breakingbad.jpg"},
    {"id": 2, "titulo": "Friends", "ano": 1994, "genero": "Comédia", "faixa_etaria": 10, "temporadas": 10, "capa": "/static/imgs/Friends.webp"},
    {"id": 3, "titulo": "Stranger Things", "ano": 2016, "genero": "Ficção", "faixa_etaria": 12, "temporadas": 4, "capa": "/static/imgs/StrangerThings.jpg"},
    {"id": 4, "titulo": "Planet Earth", "ano": 2006, "genero": "Documentário", "faixa_etaria": 0, "temporadas": 1, "capa": "/static/imgs/PlanetEarth.jpg"},
    {"id": 5, "titulo": "The Office", "ano": 2005, "genero": "Comédia", "faixa_etaria": 12, "temporadas": 9, "capa": "/static/imgs/TheOffice.jpg"},
    {"id": 6, "titulo": "Chernobyl", "ano": 2019, "genero": "Drama", "faixa_etaria": 16, "temporadas": 1, "capa": "/static/imgs/Chernobyl.jpg"},
    {"id": 7, "titulo": "Our Planet", "ano": 2019, "genero": "Documentário", "faixa_etaria": 0, "temporadas": 1, "capa": "/static/imgs/OurPlanet.webp"}
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
        usuario_encontrado = next((u for u in usuarios_memoria if u["email"] == email and u["senha"] == senha), None)
        if usuario_encontrado:
            session["usuario"] = {"nome": usuario_encontrado["nome"], "idade": int(usuario_encontrado["idade"])}
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("listar_usuarios"))
        flash("Email ou senha inválidos!", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")
        idade = request.form.get("idade")
        funcao = request.form.get("funcao")
        if not nome or not email or not senha or not idade or not funcao:
            flash("Preencha todos os campos!", "danger")
            return redirect(url_for("cadastro"))
        if senha != confirmar:
            flash("As senhas não coincidem!", "danger")
            return redirect(url_for("cadastro"))
        
        novo_id = max([u["id"] for u in usuarios_memoria]) + 1 if usuarios_memoria else 1
        usuarios_memoria.append({"id": novo_id, "nome": nome, "email": email, "senha": senha, "idade": int(idade), "funcao": funcao})
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("login"))
    return render_template("cadastro.html")

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
    return render_template("usuarios/listar_usuarios.html", usuarios=usuarios_memoria)

@app.route("/usuarios/inserir", methods=["GET", "POST"], endpoint="inserir_usuarios")
@login_obrigatorio
def inserir_usuarios():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        idade = request.form.get("idade")
        funcao = request.form.get("funcao")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")

        if not nome or not email or not idade or not funcao or not senha:
            flash("Preencha todos os campos!", "danger")
            return redirect(url_for("inserir_usuarios"))
        
        if senha != confirmar:
            flash("As senhas não coincidem!", "danger")
            return redirect(url_for("inserir_usuarios"))
        
        novo_id = max([u["id"] for u in usuarios_memoria]) + 1 if usuarios_memoria else 1
        usuarios_memoria.append({"id": novo_id, "nome": nome, "email": email, "senha": senha, "idade": int(idade), "funcao": funcao})
        flash("Usuário adicionado!", "success")
        return redirect(url_for("listar_usuarios"))
    return render_template("usuarios/inserir_usuario.html")

@app.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_usuario(id):
    usuario = next((u for u in usuarios_memoria if u["id"] == id), None)
    if not usuario:
        flash("Usuário não encontrado!", "danger")
        return redirect(url_for("listar_usuarios"))
    
    if request.method == "POST":
        usuario["nome"] = request.form.get("nome")
        usuario["email"] = request.form.get("email")
        usuario["idade"] = int(request.form.get("idade"))
        usuario["funcao"] = request.form.get("funcao")
        
        # Se digitar uma nova senha, atualiza
        nova_senha = request.form.get("senha")
        if nova_senha:
            usuario["senha"] = nova_senha
            
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("listar_usuarios"))
    
    return render_template("usuarios/inserir_usuario.html", usuario=usuario)

@app.route("/usuarios/excluir/<int:id>")
@login_obrigatorio
def excluir_usuario(id):
    global usuarios_memoria
    usuarios_memoria = [u for u in usuarios_memoria if u["id"] != id]
    flash("Usuário excluído com sucesso!", "success")
    return redirect(url_for("listar_usuarios"))

# -----------------------------
# Filmes
# -----------------------------
@app.route("/filmes/listar", endpoint="listar_filmes")
@login_obrigatorio
def listar_filmes():
    genero_filtro = request.args.get("genero", "todos")
    lista_generos = [g["nome"] for g in generos]
    usuario_logado = session.get("usuario")
    idade_usuario = int(usuario_logado.get("idade", 0))
    filmes_filtrados = [f for f in filmes if genero_filtro == "todos" or f["genero"] == genero_filtro]
    filmes_filtrados = [f for f in filmes_filtrados if idade_usuario >= f["faixa_etaria"]]
    return render_template("filmes/listar_filme.html", filmes=filmes_filtrados, generos=lista_generos, genero_filtro=genero_filtro)

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
        
        novo_id = max([f["id"] for f in filmes]) + 1 if filmes else 1
        filmes.append({"id": novo_id, "titulo": titulo, "ano": int(ano), "genero": genero, "faixa_etaria": int(faixa_etaria), "capa": capa if capa else ""})
        flash("Filme adicionado!", "success")
        return redirect(url_for("listar_filmes"))
    return render_template("filmes/inserir_filme.html", generos=[g["nome"] for g in generos])

@app.route("/filmes/editar/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_filme(id):
    filme = next((f for f in filmes if f["id"] == id), None)
    if not filme:
        flash("Filme não encontrado!", "danger")
        return redirect(url_for("listar_filmes"))
    
    if request.method == "POST":
        filme["titulo"] = request.form.get("titulo")
        filme["ano"] = int(request.form.get("ano"))
        filme["genero"] = request.form.get("genero")
        filme["faixa_etaria"] = int(request.form.get("faixa_etaria"))
        filme["capa"] = request.form.get("capa")
        flash("Filme atualizado com sucesso!", "success")
        return redirect(url_for("listar_filmes"))
    
    return render_template("filmes/inserir_filme.html", filme=filme, generos=[g["nome"] for g in generos])

@app.route("/filmes/excluir/<int:id>")
@login_obrigatorio
def excluir_filme(id):
    global filmes
    filmes = [f for f in filmes if f["id"] != id]
    flash("Filme excluído com sucesso!", "success")
    return redirect(url_for("listar_filmes"))

# -----------------------------
# Séries
# -----------------------------
@app.route("/series/listar", endpoint="listar_series")
@login_obrigatorio
def listar_series():
    genero_filtro = request.args.get("genero", "todos")
    lista_generos = [g["nome"] for g in generos]
    usuario_logado = session.get("usuario")
    idade_usuario = int(usuario_logado.get("idade", 0))
    series_filtradas = [s for s in series if genero_filtro == "todos" or s["genero"] == genero_filtro]
    series_filtradas = [s for s in series_filtradas if idade_usuario >= s["faixa_etaria"]]
    return render_template("series/listar_serie.html", series=series_filtradas, generos=lista_generos, genero_filtro=genero_filtro)

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
        
        novo_id = max([s["id"] for s in series]) + 1 if series else 1
        series.append({"id": novo_id, "titulo": titulo, "ano": int(ano), "genero": genero, "faixa_etaria": int(faixa_etaria), "temporadas": int(temporadas), "capa": capa if capa else ""})
        flash("Série/Documentário adicionado!", "success")
        return redirect(url_for("listar_series"))
    return render_template("series/inserir_serie.html", generos=[g["nome"] for g in generos])

@app.route("/series/editar/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_serie(id):
    serie = next((s for s in series if s["id"] == id), None)
    if not serie:
        flash("Série não encontrada!", "danger")
        return redirect(url_for("listar_series"))
    
    if request.method == "POST":
        serie["titulo"] = request.form.get("titulo")
        serie["ano"] = int(request.form.get("ano"))
        serie["genero"] = request.form.get("genero")
        serie["faixa_etaria"] = int(request.form.get("faixa_etaria"))
        serie["temporadas"] = int(request.form.get("temporadas"))
        serie["capa"] = request.form.get("capa")
        flash("Série atualizada com sucesso!", "success")
        return redirect(url_for("listar_series"))
    
    return render_template("series/inserir_serie.html", serie=serie, generos=[g["nome"] for g in generos])

@app.route("/series/excluir/<int:id>")
@login_obrigatorio
def excluir_serie(id):
    global series
    series = [s for s in series if s["id"] != id]
    flash("Série excluída com sucesso!", "success")
    return redirect(url_for("listar_series"))

# -----------------------------
# Funções (Banco de Dados)
# -----------------------------
@app.route("/funcoes/listar", endpoint="listar_funcoes")
@login_obrigatorio
def listar_funcoes():
    try:
        sql = "SELECT * FROM funcoes ORDER BY id_funcao DESC"
        lista_dados = execute_query(sql, fetch=True)
        
        for f in lista_dados:
            perms = []
            if f.get('gerenciar_usuario'): perms.append('Gerenciar usuário')
            if f.get('gerenciar_tarefas'): perms.append('Gerenciar tarefa')
            if f.get('gerenciar_funcao'): perms.append('Gerenciar funções')
            if f.get('gerenciar_serie'): perms.append('Séries')
            if f.get('gerenciar_filme'): perms.append('Filmes')
            f['permissoes'] = perms
            f['status'] = 'Ativo' if f.get('status') else 'Inativo'

        return render_template("funcoes/listar_funcoes.html", funcoes=lista_dados)
    except Exception as e:
        flash(f"Erro ao acessar banco de dados: {e}", "danger")
        return render_template("funcoes/listar_funcoes.html", funcoes=[])

@app.route("/funcoes/inserir", methods=["GET", "POST"], endpoint="inserir_funcoes")
@login_obrigatorio
def inserir_funcoes():
    if request.method == "POST":
        nome = request.form.get("nome").strip()
        status = 1 if request.form.get("status") == "Ativo" else 0
        descricao = request.form.get("descricao").strip()
        permissoes = request.form.getlist("permissoes")

        if not nome:
            flash("Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for("inserir_funcoes"))

        try:
            sql = """
                INSERT INTO funcoes (nome, status, descricao, gerenciar_usuario, gerenciar_tarefas, gerenciar_funcao, gerenciar_serie, gerenciar_filme)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                nome, status, descricao,
                1 if 'Gerenciar usuário' in permissoes else 0,
                1 if 'Gerenciar tarefa' in permissoes else 0,
                1 if 'Gerenciar funções' in permissoes else 0,
                1 if 'Séries' in permissoes else 0,
                1 if 'Filmes' in permissoes else 0
            )
            execute_query(sql, params)
            flash("Função cadastrada com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao inserir função: {e}", "danger")
        
        return redirect(url_for("listar_funcoes"))

    return render_template("funcoes/inserir_funcao.html")

@app.route("/funcoes/editar/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_funcao(id):
    try:
        if request.method == "POST":
            nome = request.form.get("nome").strip()
            status = 1 if request.form.get("status") == "Ativo" else 0
            descricao = request.form.get("descricao").strip()
            permissoes = request.form.getlist("permissoes")

            sql = """
                UPDATE funcoes SET nome=%s, status=%s, descricao=%s, 
                gerenciar_usuario=%s, gerenciar_tarefas=%s, gerenciar_funcao=%s, 
                gerenciar_serie=%s, gerenciar_filme=%s 
                WHERE id_funcao=%s
            """
            params = (
                nome, status, descricao,
                1 if 'Gerenciar usuário' in permissoes else 0,
                1 if 'Gerenciar tarefa' in permissoes else 0,
                1 if 'Gerenciar funções' in permissoes else 0,
                1 if 'Séries' in permissoes else 0,
                1 if 'Filmes' in permissoes else 0,
                id
            )
            execute_query(sql, params)
            flash("Função atualizada com sucesso!", "success")
            return redirect(url_for("listar_funcoes"))

        sql = "SELECT * FROM funcoes WHERE id_funcao = %s"
        funcao = execute_one(sql, (id,))
        if not funcao:
            flash("Função não encontrada!", "danger")
            return redirect(url_for("listar_funcoes"))
        
        funcao['status_str'] = 'Ativo' if funcao.get('status') else 'Inativo'
        perms = []
        if funcao.get('gerenciar_usuario'): perms.append('Gerenciar usuário')
        if funcao.get('gerenciar_tarefas'): perms.append('Gerenciar tarefa')
        if funcao.get('gerenciar_funcao'): perms.append('Gerenciar funções')
        if funcao.get('gerenciar_serie'): perms.append('Séries')
        if funcao.get('gerenciar_filme'): perms.append('Filmes')
        funcao['permissoes'] = perms

        return render_template("funcoes/inserir_funcao.html", funcao=funcao)
    except Exception as e:
        flash(f"Erro ao editar função: {e}", "danger")
        return redirect(url_for("listar_funcoes"))

@app.route("/funcoes/excluir/<int:id>")
@login_obrigatorio
def excluir_funcao(id):
    try:
        sql = "DELETE FROM funcoes WHERE id_funcao = %s"
        execute_query(sql, (id,))
        flash("Função excluída com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao excluir função: {e}", "danger")
    return redirect(url_for("listar_funcoes"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
