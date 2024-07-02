from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, text

# Criar a conexão com o banco de dados SQLite em memória
engine = create_engine('sqlite:///:memory:')

# Definir o objeto MetaData com o esquema 'teste'
metadata_obj = MetaData()

# Definir a tabela 'user'
user = Table(
    'user',
    metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), nullable=False),
    Column('email_address', String(60)),
    Column('nickname', String(50), nullable=False),
)

# Definir a tabela 'user_prefs'
user_prefs = Table(
    'user_prefs', metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False),
    Column('pref_name', String(60), nullable=False),
    Column('pref_value', String(60), nullable=False),
)

# Imprimir as tabelas definidas
for table in metadata_obj.sorted_tables:
    print(table)

# Criar as tabelas no banco de dados
metadata_obj.create_all(engine)

# Definir outra MetaData para a tabela 'financial_info'
metadata_bd_obj = MetaData()

# Definir a tabela 'financial_info'
financial_info = Table(
    'financial_info',
    metadata_bd_obj,
    Column('id', Integer, primary_key=True),
    Column('value', String(60), nullable=False),
)

# Criar a tabela 'financial_info' no banco de dados
metadata_bd_obj.create_all(engine)

# Imprimir as chaves primárias e restrições da tabela 'financial_info'
print(financial_info.primary_key)
print(financial_info.constraints)

# Tentar executar uma consulta SQL
try:
    with engine.connect() as connection:
        # Inserir dados na tabela 'user' para a consulta
        connection.execute(
            user.insert().values(user_id=1, user_name="User1", email_address="user1@example.com", nickname="User1Nick"))
        connection.execute(
            user.insert().values(user_id=2, user_name="User2", email_address="user2@example.com", nickname="User2Nick"))

        # Executar a consulta SQL para selecionar todos os dados da tabela 'user'
        sql = text('SELECT * FROM user')
        result = connection.execute(sql)

        for row in result:
            print(row)
except Exception as e:
    print(f"An error occurred: {e}")
