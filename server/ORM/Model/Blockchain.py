from ORM.Base import Base
from sqlalchemy import Column, TIMESTAMP, BigInteger, text, JSON, String


class Blockchain(Base):
    __tablename__ = "blockchain"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    transaction = Column(JSON)
    current_hash= Column(String)
    previous_hash= Column(String)



    def __repr__(self):
        return f'''
Blockchain(
id: {self.id}
created_at: {self.created_at}
transaction: {self.transaction}
current_hash: {self.current_hash}
previous_hash: {self.previous_hash}
)
'''
