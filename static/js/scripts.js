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
// EFEITO NOS INPUTS
// =========================
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
const botoes = document.querySelectorAll("button");

botoes.forEach(function(botao) {

    botao.addEventListener("click", function() {
        botao.style.transform = "scale(0.95)";
        setTimeout(() => {
            botao.style.transform = "scale(1)";
        }, 100);
    });

});

// =========================
// COPIAR EMAIL (EQUIPE)
// =========================
const btnCopiarEmail = document.querySelector("#btn-copiar-email");
if (btnCopiarEmail) {
    btnCopiarEmail.addEventListener("click", function() {
        const email = document.querySelector("#email-equipe").textContent;
        navigator.clipboard.writeText(email)
            .then(() => {
                alert("Email copiado para a área de transferência!");
            })
            .catch(err => {
                alert("Erro ao copiar email: " + err);
            });
    });
}

// =========================
// INDICADOR DE FORÇA DE SENHA (CADASTRO)
// =========================
const senhaInput = document.querySelector("#senha");
const senhaIndicador = document.querySelector("#forca-senha");

if(senhaInput && senhaIndicador){
    senhaInput.addEventListener("input", function() {
        const senha = senhaInput.value;
        let forca = 0;

        if(senha.length >= 6) forca++;
        if(/[A-Z]/.test(senha)) forca++;
        if(/[0-9]/.test(senha)) forca++;
        if(/[^A-Za-z0-9]/.test(senha)) forca++;

        switch(forca){
            case 0: senhaIndicador.textContent = ""; break;
            case 1: senhaIndicador.textContent = "Fraca"; senhaIndicador.style.color = "red"; break;
            case 2: senhaIndicador.textContent = "Média"; senhaIndicador.style.color = "orange"; break;
            case 3: senhaIndicador.textContent = "Forte"; senhaIndicador.style.color = "blue"; break;
            case 4: senhaIndicador.textContent = "Muito Forte"; senhaIndicador.style.color = "green"; break;
        }
    });
}