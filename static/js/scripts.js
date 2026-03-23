// =========================
// CONFIRMAÇÃO AO EXCLUIR
// =========================

// DOMContentLoaded garante que o JS só roda depois que o HTML inteiro carregou
document.addEventListener("DOMContentLoaded", function () {
    
    // pega todos os botões de excluir da página de uma vez
    const botoesExcluir = document.querySelectorAll(".btn-excluir");

    botoesExcluir.forEach(function (botao) {
        botao.addEventListener("click", function (e) {
            const confirmar = confirm("Tem certeza que deseja excluir?"); // abre popup nativo do navegador
            if (!confirmar) {
                e.preventDefault(); // cancela ação — impede o clique de continuar
            }
        });
    });

});

// =========================
// EFEITO NOS INPUTS (CSS atualizado)
// =========================

// duplica via JS o mesmo efeito que o CSS já faz — serve de fallback
const inputs = document.querySelectorAll("input, select");

inputs.forEach(function(input) {

    // focus: usuário clicou no campo
    input.addEventListener("focus", function() {
        input.style.border = "1px solid rgba(80,200,255,0.7)";
        input.style.boxShadow = "0 0 12px 5px rgba(80,200,255,0.3)";
        input.style.transition = "all 0.3s ease";
    });

    // blur: usuário saiu do campo
    input.addEventListener("blur", function() {
        input.style.border = "1px solid rgba(255,255,255,0.1)";
        input.style.boxShadow = "none";
    });

    input.addEventListener("mouseover", function() {
        input.style.borderColor = "rgba(80,200,255,0.7)";
        input.style.boxShadow = "0 0 10px 4px rgba(80,200,255,0.3)";
    });

    // mouseout: só reseta se o campo não estiver em foco ainda
    input.addEventListener("mouseout", function() {
        if(document.activeElement !== input) { // evita resetar o estilo enquanto o usuário está digitando
            input.style.borderColor = "rgba(255,255,255,0.1)";
            input.style.boxShadow = "none";
        }
    });

});

// =========================
// CLICK VISUAL NOS BOTÕES (Efeito de clique compatível com CSS)
// =========================

// seleciona todos os tipos de botão do sistema
const botoes = document.querySelectorAll("button, .botao-entrar, .botao-criar, .botao-form, .add-usuario, .btn-editar, .btn-sair");

botoes.forEach(function(botao) {

    botao.addEventListener("mousedown", function() {
        botao.style.transform = "scale(0.95)"; // encolhe levemente ao pressionar
    });

    botao.addEventListener("mouseup", function() {
        botao.style.transform = "scale(1)"; // volta ao normal ao soltar
    });

    botao.addEventListener("mouseleave", function() {
        botao.style.transform = "scale(1)"; // garante reset se o mouse sair sem soltar o clique
    });

});

// =========================
// COPIAR EMAIL (EQUIPE)
// =========================

// alternativa JS ao onclick inline do sobre_equipe.html
const btnCopiarEmails = document.querySelectorAll(".btn-copiar");
btnCopiarEmails.forEach(function(btn) {
    btn.addEventListener("click", function() {
        const emailEl = btn.previousElementSibling; // pega o <span> com o email que vem antes do botão
        if(emailEl) {
            const email = emailEl.textContent;
            navigator.clipboard.writeText(email)
                .then(() => {
                    alert("Email copiado para a área de transferência!");
                })
                .catch(err => {
                    alert("Erro ao copiar email: " + err); // ex: navegador sem permissão de clipboard
                });
        }
    });
});

// =========================
// INDICADOR DE FORÇA DE SENHA (CADASTRO)
// =========================

const senhaInputs = document.querySelectorAll("#senha");
senhaInputs.forEach(function(senhaInput){
    // procura o #forca-senha dentro do mesmo form — funciona com múltiplos forms na página
    const senhaIndicador = senhaInput.closest("form").querySelector("#forca-senha");
    if(!senhaIndicador) return; // sai se não tiver o indicador na página (ex: login não tem)

    senhaInput.addEventListener("input", function() {
        const senha = senhaInput.value;
        let forca = 0;

        // cada critério atendido soma 1 ponto
        if(senha.length >= 6) forca++;          // mínimo de 6 caracteres
        if(/[A-Z]/.test(senha)) forca++;        // tem letra maiúscula
        if(/[0-9]/.test(senha)) forca++;        // tem número
        if(/[^A-Za-z0-9]/.test(senha)) forca++; // tem caractere especial

        // exibe o resultado baseado na pontuação
        switch(forca){
            case 0: 
                senhaIndicador.textContent = ""; 
                break;
            case 1: 
                senhaIndicador.textContent = "Fraca"; 
                senhaIndicador.style.color = "red"; 
                break;
            case 2: 
                senhaIndicador.textContent = "Média"; 
                senhaIndicador.style.color = "orange"; 
                break;
            case 3: 
                senhaIndicador.textContent = "Forte"; 
                senhaIndicador.style.color = "blue"; 
                break;
            case 4: 
                senhaIndicador.textContent = "Muito Forte"; 
                senhaIndicador.style.color = "green"; 
                break;
        }
    });
});

// versão 1 do toggleSenha — recebe o id do input e o elemento do olho separados
// usada no cadastro.html: onclick="toggleSenha('senha', this)"
function toggleSenha(idInput, elementoOlho) {
    const input = document.getElementById(idInput);
    if (input.type === "password") {
        input.type = "text"; 
        elementoOlho.textContent = "🙈"; 
    } else {
        input.type = "password"; 
        elementoOlho.textContent = "👁️"; 
    }
}

// versão 2 do toggleSenha — recebe só o elemento do olho (this) e navega até o input pelo D
// usada no login.html: onclick="toggleSenha(this)"
// atenção: essa declaração sobrescreve a função acima — as duas têm o mesmo nome!
function toggleSenha(el) {
    const inputSenha = el.previousElementSibling; // pega o input de senha que vem antes do span no HTML
    if (inputSenha.type === "password") {
        inputSenha.type = "text";  // mostra a senha
        el.textContent = "🙈";     // troca o ícone
    } else {
        inputSenha.type = "password"; // esconde a senha
        el.textContent = "👁️";       // volta o ícone
    }
}