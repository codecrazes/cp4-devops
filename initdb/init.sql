CREATE DATABASE IF NOT EXISTS appdb;
USE appdb;

CREATE TABLE IF NOT EXISTS transactions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  descricao VARCHAR(255) NOT NULL,
  valor DECIMAL(10,2) NOT NULL,
  data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO transactions (descricao, valor) VALUES ('Compra inicial', 123.45);
