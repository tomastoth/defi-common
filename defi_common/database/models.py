from datetime import datetime

import sqlalchemy
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, orm, func, \
    Table, Numeric
from sqlalchemy.orm import relationship

from defi_common.database import db

users_to_addresses = Table(
    "users_to_addresses",
    db.Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("address_id", ForeignKey("addresses.id"), primary_key=True),
)


class Address(db.Base):  # type: ignore
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)  # noqa
    time_created = Column(DateTime(), default=datetime.now())
    time_updated = Column(DateTime(), default=datetime.now())
    address = Column(String)
    blockchain_type = Column(String)
    address_updates = orm.relationship(
        "AggregatedBalanceUpdate", back_populates="address"
    )
    performance_results = orm.relationship(
        "PerformanceRunResult", back_populates="address"
    )
    address_performance_ranks = orm.relationship(
        "AddressPerformanceRank", back_populates="address"
    )
    users = orm.relationship("User", secondary=users_to_addresses, back_populates="addresses")

    def __repr__(self) -> str:
        return f"address: {self.address}, blockchain_type: {self.blockchain_type}"


class AggregatedBalanceUpdate(db.Base):  # type: ignore
    __tablename__ = "address_updates"
    id = Column(Integer, primary_key=True)  # noqa
    time_created = Column(DateTime(), default=datetime.now())
    time_updated = Column(DateTime(), default=datetime.now())
    value_usd = Column(Float, nullable=False)
    timestamp = Column(sqlalchemy.BigInteger, nullable=False)
    time = Column(DateTime, nullable=False)
    symbol = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    value_pct = Column(Float, nullable=False)
    address = orm.relationship(Address, back_populates="address_updates")
    address_id = Column(Integer, ForeignKey("addresses.id"))

    def __repr__(self) -> str:
        return (
            f"symbol: {self.symbol}, value_usd: {self.value_usd}, price: {self.price} "
            f"time: {self.timestamp} address: {self.address}"
        )


class PerformanceRunResult(db.Base):  # type: ignore
    __tablename__ = "performance_run_results"
    id = Column(Integer, primary_key=True)  # noqa
    time_created = Column(DateTime(), default=datetime.now())
    time_updated = Column(DateTime(), default=datetime.now())
    performance = Column(Float, nullable=False)
    start_time = Column(DateTime(), nullable=False)
    end_time = Column(DateTime(), nullable=False)
    address = orm.relationship(Address, back_populates="performance_results")
    address_id = Column(Integer, ForeignKey("addresses.id"))


class AddressPerformanceRank(db.Base):  # type: ignore
    __tablename__ = "address_performance_rank"
    id = Column(Integer, primary_key=True)  # noqa
    time_created = Column(DateTime(), default=datetime.now())
    time_updated = Column(DateTime(), default=datetime.now())
    performance = Column(Float, nullable=False)
    time = Column(DateTime(), nullable=False)
    address = orm.relationship(Address, back_populates="address_performance_ranks")
    address_id = Column(Integer, ForeignKey("addresses.id"))
    ranking_type = Column(String, nullable=False)
    rank = Column(Integer, sqlalchemy.CheckConstraint("rank > 0"))


class CoinChangeRank(db.Base):  # type. ignore
    __tablename__ = "coin_rank"
    id = Column(Integer, primary_key=True)  # noqa
    time_created = Column(DateTime(), default=datetime.now())
    time_updated = Column(DateTime(), default=datetime.now())
    symbol = Column(String, nullable=False)
    rank = Column(Integer, sqlalchemy.CheckConstraint("rank > 0"))
    time = Column(DateTime(), nullable=False)
    pct_change = Column(Float, nullable=False)
    ranking_type = Column(String, nullable=False)


class User(SQLAlchemyBaseUserTableUUID, db.Base):
    __tablename__ = "users"

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    addresses = orm.relationship("Address", secondary=users_to_addresses,
                                 back_populates="users")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.email!r})"


class Blockchain(db.Base):
    __tablename__ = "blockchains"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Token(db.Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    blockchain = orm.relationship("Blockchain")
    blockchain_id = Column(Integer, ForeignKey("blockchains.id"), nullable=False)
    address = Column(String, nullable=False)
    decimals = Column(Integer, nullable=False)


class TokenBalance(db.Base):
    __tablename__ = "token_balances"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime(), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    token_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)
    amount = Column(Float(precision=10), nullable=False)
    price = Column(Float(precision=10), nullable=True)
