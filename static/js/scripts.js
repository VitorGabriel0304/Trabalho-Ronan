// =========================
// CONFIRMAÇÃO AO EXCLUIR
// =========================

// toda vez que clicar em algo com classe "btn-excluir"
document.addEventListener("DOMContentLoaded", function () {
    
    const botoesExcluir = document.querySelectorAll(".btn-excluir");

    botoesExcluir.forEach(function (botao) {
        botao.addEventListener("click", function (e) {
            
            // pergunta antes de "excluir"
            const confirmar = confirm("Tem certeza que deseja excluir?");

            if (!confirmar) {
                e.preventDefault(); // cancela ação
            }
        });
    });

});


// =========================
// EFEITO NOS INPUTS
// =========================

// quando clica no input, muda a borda
const inputs = document.querySelectorAll("input, select");

inputs.forEach(function(input) {

    input.addEventListener("focus", function() {
        input.style.border = "2px solid red";
    });

    input.addEventListener("blur", function() {
        input.style.border = "";
    });

});


// =========================
// CLICK VISUAL NOS BOTÕES
// =========================

// efeito rápido quando clica em botão
const botoes = document.querySelectorAll("button");

botoes.forEach(function(botao) {

    botao.addEventListener("click", function() {
        botao.style.transform = "scale(0.95)";

        setTimeout(() => {
            botao.style.transform = "scale(1)";
        }, 100);
    });

});