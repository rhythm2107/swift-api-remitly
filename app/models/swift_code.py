from sqlalchemy import Column, String, Boolean, Integer, CheckConstraint, text
from app.core.database import Base

class SwiftCode(Base):
    __tablename__ = "swift_codes"

    id = Column(Integer, primary_key=True, index=True)
    swift_code = Column(String(11), unique=True, nullable=False)
    bank_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    country_iso2 = Column(String(2), nullable=False, index=True)
    country_name = Column(String(100), nullable=False)
    is_headquarter = Column(Boolean, nullable=False, server_default=text('false'))

    __table_args__ = (
        CheckConstraint("char_length(country_iso2) = 2", name="check_country_iso2_len"),
        CheckConstraint("char_length(swift_code) >= 8 AND char_length(swift_code) <= 11", name="check_swift_code_len"),
        CheckConstraint("char_length(trim(bank_name)) > 0", name="check_bank_name_not_empty"),
        CheckConstraint("char_length(trim(country_name)) > 0", name="check_country_name_not_empty"),
    )