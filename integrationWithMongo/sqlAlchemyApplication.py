import sqlalchemy as sqlA
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, inspect, select
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "cliente"
    # attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)
    endereco = Column(String)

    contas = relationship("Conta", back_populates="cliente", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"<Cliente(id={self.id}, name={self.name})>"


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))

    cliente = relationship("Cliente", back_populates="contas")

    def __repr__(self):
        return f"<Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, id_cliente={self.id_cliente})>"


print(Cliente.__tablename__)
print(Conta.__tablename__)

# conexão com o bd
engine = create_engine('sqlite://')

# criando as classes como tabelas no bd
Base.metadata.create_all(engine)

# investiga o esquema de banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("cliente"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

# adicionando um usuário e suas contas ao banco de dados
with Session(engine) as session:
    juliana = Cliente(
        name="Juliana",
        cpf="12345678900",
        endereco="Rua A, 123"
    )
    marcio = Cliente(
        name="Marcio",
        cpf="98765432100",
        endereco="Rua B, 456"
    )
    patrick = Cliente(
        name="Patrick",
        cpf="11122233344",
        endereco="Rua C, 789"
    )

    conta_juliana = Conta(
        tipo="Corrente",
        agencia="1234",
        num=567890,
        cliente=juliana
    )
    conta_marcio = Conta(
        tipo="Poupança",
        agencia="4321",
        num=123456,
        cliente=marcio
    )

    session.add(juliana)
    session.add(marcio)
    session.add(patrick)
    session.add(conta_juliana)
    session.add(conta_marcio)
    session.commit()

stmt = select(Cliente).where(Cliente.name.in_(["Juliana", "Marcio", "Patrick"]))
with Session(engine) as session:
    for cliente in session.scalars(stmt):
        print(cliente)

order = select(Cliente).order_by(Cliente.name.asc())
with Session(engine) as session:
    for cliente in session.scalars(order):
        print(cliente)
