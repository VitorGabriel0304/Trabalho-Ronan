// =========================
// CONFIRMAÇÃO AO EXCLUIR
// =========================
document.addEventListener("DOMContentLoaded", function () {
    
    const botoesExcluir = document.querySelectorAll(".btn-excluir");

    botoesExcluir.forEach(function (botao) {
        botao.addEventListener("click", function (e) {
            const confirmar = confirm("Tem certeza que deseja excluir?");
            if (!confirmar) {
                e.preventDefault(); // cancela ação
            }
        });
    });

});

// =========================
// EFEITO NOS INPUTS (CSS atualizado)
// =========================
const inputs = document.querySelectorAll("input, select");

inputs.forEach(function(input) {

    input.addEventListener("focus", function() {
        // Bordas e sombra conforme CSS
        input.style.border = "1px solid rgba(80,200,255,0.7)";
        input.style.boxShadow = "0 0 12px 5px rgba(80,200,255,0.3)";
        input.style.transition = "all 0.3s ease";
    });

    input.addEventListener("blur", function() {
        // Retorna ao padrão
        input.style.border = "1px solid rgba(255,255,255,0.1)";
        input.style.boxShadow = "none";
    });

    input.addEventListener("mouseover", function() {
        input.style.borderColor = "rgba(80,200,255,0.7)";
        input.style.boxShadow = "0 0 10px 4px rgba(80,200,255,0.3)";
    });

    input.addEventListener("mouseout", function() {
        if(document.activeElement !== input) {
            input.style.borderColor = "rgba(255,255,255,0.1)";
            input.style.boxShadow = "none";
        }
    });

});

// =========================
// CLICK VISUAL NOS BOTÕES (Efeito de clique compatível com CSS)
// =========================
const botoes = document.querySelectorAll("button, .botao-entrar, .botao-criar, .botao-form, .add-usuario, .btn-editar, .btn-sair");

botoes.forEach(function(botao) {

    botao.addEventListener("mousedown", function() {
        botao.style.transform = "scale(0.95)";
    });

    botao.addEventListener("mouseup", function() {
        botao.style.transform = "scale(1)";
    });

    botao.addEventListener("mouseleave", function() {
        botao.style.transform = "scale(1)";
    });

});

// =========================
// COPIAR EMAIL (EQUIPE)
// =========================
const btnCopiarEmails = document.querySelectorAll(".btn-copiar");
btnCopiarEmails.forEach(function(btn) {
    btn.addEventListener("click", function() {
        const emailEl = btn.previousElementSibling; // assume que o texto vem antes do botão
        if(emailEl) {
            const email = emailEl.textContent;
            navigator.clipboard.writeText(email)
                .then(() => {
                    alert("Email copiado para a área de transferência!");
                })
                .catch(err => {
                    alert("Erro ao copiar email: " + err);
                });
        }
    });
});

// =========================
// INDICADOR DE FORÇA DE SENHA (CADASTRO)
// =========================
const senhaInputs = document.querySelectorAll("#senha");
senhaInputs.forEach(function(senhaInput){
    const senhaIndicador = senhaInput.closest("form").querySelector("#forca-senha");
    if(!senhaIndicador) return;

    senhaInput.addEventListener("input", function() {
        const senha = senhaInput.value;
        let forca = 0;

        if(senha.length >= 6) forca++;
        if(/[A-Z]/.test(senha)) forca++;
        if(/[0-9]/.test(senha)) forca++;
        if(/[^A-Za-z0-9]/.test(senha)) forca++;

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