from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from app.database.db import Base

class Roteiro(Base):
    __tablename__ = "roteiros"
    id = Column(Integer, primary_key=True, index=True)
    pais = Column(String)
    cidade = Column(String)
    data_chegada = Column(Date)
    data_saida = Column(Date)
    transporte = Column(String)
    custo_estimado = Column(Float)
    observacoes = Column(String)

class Despesa(Base):
    __tablename__ = "despesas"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date)
    categoria = Column(String)
    descricao = Column(String)
    valor = Column(Float)
    cidade = Column(String)

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    data = Column(Date)
    valor = Column(Float)
    status = Column(String)
    arquivo = Column(String)

