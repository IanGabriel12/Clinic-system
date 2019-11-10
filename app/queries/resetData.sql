use clinic;
ALTER TABLE pacientes
    DROP FOREIGN KEY fk_endPessoa;
ALTER TABLE pacientes
    ADD CONSTRAINT endereco_id
        FOREIGN KEY (endereco_id)
        REFERENCES enderecos(id)
        ON DELETE CASCADE;