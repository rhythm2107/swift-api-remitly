from sqlalchemy import Column, String, Boolean, Integer, CheckConstraint, text
from app.core.database import Base

class SwiftCode(Base):
    __tablename__ = "swift_codes"

    id = Column(Integer, primary_key=True, index=True)
    swift_code = Column(String(11), unique=True, nullable=False)
    bank_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    country_iso2 = Column(String(2), nullable=False)
    country_name = Column(String(100), nullable=False)
    is_headquarter = Column(Boolean, nullable=False, server_default=text('false'))

    # Ensure that ISO2 is always of length 2
    __table_args__ = (
        CheckConstraint("char_length(country_iso2) = 2", name="check_country_iso2_len"),
    )