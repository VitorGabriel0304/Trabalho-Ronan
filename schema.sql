-- DROP DATABASE IF EXISTS cinelist ;

CREATE DATABASE IF NOT EXISTS cinelist;
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

   

 USE cinelist;

-- DROP DATABASE IF EXISTS funcoes ;
CREATE DATABASE IF NOT EXISTS funcoes(
    id_funcao BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(20) NOT NULL, UNIQUE
    status BOOLEAN DEFAULT 1,
    descricao VARCHAR(255),
    gerenciar_usuario BOOLEAN DEFAULT 0,
    gerenciar_tarefas BOOLEAN DEFAULT 0,
    gerenciar_funcao BOOLEAN DEFAULT 0,
    gerenciar_serie BOOLEAN DEFAULT 0,
    gerenciar_filme BOOLEAN DEFAULT 0,

-- log 
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
        on update CURRENT_TIMESTAMP

);

-- DROP TABLE IF EXISTS CLIENTES;
CREATE TABLE IF NOT EXISTS usuarios(

    funcao_id BIGINT UNSIGNED NOT NULL,

    -- logs

    -- cria o relacionamneto de tabelas
    CONSTRAINT fk_usuario_funcao
    FOREIGN KEY (funcao_id) REFERENCES funcoes (funcao_id)


)

