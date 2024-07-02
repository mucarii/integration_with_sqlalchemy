from pymongo import MongoClient

# Conectar ao MongoDB Atlas
client = MongoClient('mongodb+srv://adm:<senha>@viagens.wotekhq.mongodb.net/?retryWrites=true&w=majority&appName=viagens')

# Crie um banco de dados chamado 'mydatabase'
db = client['mydatabase']

# Crie uma coleção chamada 'bank'
collection = db['bank']

# Exemplo de documentos de clientes
clientes = [
    {
        "name": "Juliana",
        "cpf": "12345678900",
        "endereco": "Rua A, 123",
        "contas": [
            {
                "tipo": "Corrente",
                "agencia": "1234",
                "num": 567890
            }
        ]
    },
    {
        "name": "Marcio",
        "cpf": "98765432100",
        "endereco": "Rua B, 456",
        "contas": [
            {
                "tipo": "Poupança",
                "agencia": "4321",
                "num": 123456
            }
        ]
    },
    {
        "name": "Patrick",
        "cpf": "11122233344",
        "endereco": "Rua C, 789",
        "contas": []
    }
]

# Inserir documentos na coleção
collection.insert_many(clientes)

#recuperar todos elementos
for cliente in collection.find():
    print(cliente)

#recuperar cliente pelo nome
cliente = collection.find_one({"name": "Juliana"})
print(cliente)

#recuperar cliente pelo tipo de conta
clientes_com_conta_corrente = collection.find({"contas.tipo": "Corrente"})
for cliente in clientes_com_conta_corrente:
    print(cliente)

#recuperar cliente por agencia
clientes_agencia = collection.find({"contas.agencia": "1234"})
for cliente in clientes_agencia:
    print(cliente)

#recuperar todos clientes por nome ordenado
clientes_ordenados = collection.find().sort("name")
for cliente in clientes_ordenados:
    print(cliente)
