from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True)
    product = Column(String)
    supplier = Column(String, index=True)
    destination = Column(String)
    order_date = Column(DateTime)
    expected_delivery = Column(DateTime)
    actual_delivery = Column(DateTime, nullable=True)
    lead_time = Column(Integer)
    shipping_mode = Column(String)
    quantity = Column(Integer)
    inventory = Column(Integer)
    demand = Column(Integer)
    shipping_cost = Column(Float)
    delay_days = Column(Integer, nullable=True)
    status = Column(String) # e.g. "Pending", "Delivered", "Delayed"

    predictions = relationship("Prediction", back_populates="shipment")
    prescriptions = relationship("Prescription", back_populates="shipment")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    delay_probability = Column(Float)
    predicted_delay_days = Column(Float)
    model_version = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    shipment = relationship("Shipment", back_populates="predictions")

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    option_name = Column(String) # e.g. "Option A", "Option B"
    action_type = Column(String) # e.g. "Expedited", "Secondary Supplier"
    estimated_cost = Column(Float)
    estimated_delay = Column(Float)
    risk_score = Column(Float)
    expected_savings = Column(Float)
    optimization_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    shipment = relationship("Shipment", back_populates="prescriptions")
    decision = relationship("Decision", back_populates="prescription", uselist=False)

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    selected_action = Column(String)
    decision_date = Column(DateTime(timezone=True), server_default=func.now())
    decision_status = Column(String, default="EXECUTED")

    prescription = relationship("Prescription", back_populates="decision")
    user = relationship("User")
    outcome = relationship("Outcome", back_populates="decision", uselist=False)

class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("decisions.id"))
    actual_cost = Column(Float)
    actual_delay = Column(Float)
    actual_savings = Column(Float)
    success = Column(Boolean)
    evaluated_at = Column(DateTime(timezone=True), server_default=func.now())

    decision = relationship("Decision", back_populates="outcome")
