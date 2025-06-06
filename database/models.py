from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Project(Base):
    """Model for storing project information"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    duration_weeks = Column(Integer, nullable=False)
    team_size = Column(String(50), nullable=False)
    project_type = Column(String(100), nullable=False)
    methodology = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SDLCBreakdown(Base):
    """Model for storing SDLC breakdown results"""
    __tablename__ = 'sdlc_breakdowns'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False)  # Reference to Project
    ai_response = Column(Text)  # Raw AI response
    parsed_data = Column(JSON)  # Parsed SDLC data
    total_phases = Column(Integer)
    complexity_assessment = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class SDLCPhase(Base):
    """Model for storing individual SDLC phases"""
    __tablename__ = 'sdlc_phases'
    
    id = Column(Integer, primary_key=True)
    breakdown_id = Column(Integer, nullable=False)  # Reference to SDLCBreakdown
    phase_order = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    duration_weeks = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    deliverables = Column(JSON)  # List of deliverables
    activities = Column(JSON)  # List of activities
    team_focus = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

# Database connection and session management
def get_database_url():
    """Get database URL from environment variables"""
    return os.getenv('DATABASE_URL', 'postgresql://localhost/smartsdlc')

def create_database_engine():
    """Create database engine"""
    database_url = get_database_url()
    return create_engine(database_url, echo=False)

def create_tables():
    """Create all database tables"""
    engine = create_database_engine()
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get database session"""
    engine = create_database_engine()
    Session = sessionmaker(bind=engine)
    return Session()