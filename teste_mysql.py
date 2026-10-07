import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    use_pure=True,
    database="urna_academica"
)

print("CONECTOU!")