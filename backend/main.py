"""
EcoSeal Insulation Takeoff System - FastAPI Backend
Real data, real API, real database
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
import json
import os

# ============================================================================
# DATABASE SETUP
# ============================================================================

DATABASE_URL = "sqlite:///./takeoff.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================================================
# DATABASE MODELS
# ============================================================================

class ProjectDB(Base):
    """Project database model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    status = Column(String, default="draft")  # draft, in_progress, complete
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TakeoffDB(Base):
    """Takeoff results database model"""
    __tablename__ = "takeoffs"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    level = Column(String)
    wall_type = Column(String)
    material_type = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    assembly = Column(String)
    r_value = Column(String)
    perimeter_ft = Column(Float)
    height_ft = Column(Float)
    confidence = Column(String, default="GREEN")
    created_at = Column(DateTime, default=datetime.utcnow)

class SettingsDB(Base):
    """System settings"""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# ============================================================================
# PYDANTIC MODELS (API request/response)
# ============================================================================

class ProjectCreate(BaseModel):
    name: str
    notes: str = None
    date: str = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    date: datetime
    notes: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TakeoffItem(BaseModel):
    level: str
    wall_type: str
    material_type: str
    quantity: float
    unit: str
    assembly: str
    r_value: str
    perimeter_ft: float
    height_ft: float
    confidence: str = "GREEN"

class TakeoffResponse(BaseModel):
    id: int
    project_id: int
    level: str
    wall_type: str
    material_type: str
    quantity: float
    unit: str
    assembly: str
    r_value: str
    perimeter_ft: float
    height_ft: float
    confidence: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SettingUpdate(BaseModel):
    key: str
    value: str

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="EcoSeal Takeoff API",
    description="Real insulation takeoff system with persistent data",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATABASE DEPENDENCY
# ============================================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# PROJECT ENDPOINTS
# ============================================================================

@app.post("/api/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = next(get_db())):
    """Create a new project"""
    db_project = ProjectDB(
        name=project.name,
        notes=project.notes,
        date=datetime.fromisoformat(project.date) if project.date else datetime.utcnow(),
        status="draft"
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/api/projects", response_model=list[ProjectResponse])
def list_projects(db: Session = next(get_db())):
    """List all projects"""
    projects = db.query(ProjectDB).order_by(ProjectDB.created_at.desc()).all()
    return projects

@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = next(get_db())):
    """Get a specific project"""
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/api/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectCreate, db: Session = next(get_db())):
    """Update a project"""
    db_project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db_project.name = project.name
    db_project.notes = project.notes
    if project.date:
        db_project.date = datetime.fromisoformat(project.date)
    db_project.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_project)
    return db_project

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, db: Session = next(get_db())):
    """Delete a project"""
    db_project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return {"status": "deleted"}

# ============================================================================
# TAKEOFF ENDPOINTS
# ============================================================================

@app.post("/api/projects/{project_id}/takeoffs", response_model=TakeoffResponse)
def create_takeoff(project_id: int, takeoff: TakeoffItem, db: Session = next(get_db())):
    """Create a takeoff item for a project"""
    # Verify project exists
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db_takeoff = TakeoffDB(
        project_id=project_id,
        level=takeoff.level,
        wall_type=takeoff.wall_type,
        material_type=takeoff.material_type,
        quantity=takeoff.quantity,
        unit=takeoff.unit,
        assembly=takeoff.assembly,
        r_value=takeoff.r_value,
        perimeter_ft=takeoff.perimeter_ft,
        height_ft=takeoff.height_ft,
        confidence=takeoff.confidence
    )
    db.add(db_takeoff)
    db.commit()
    db.refresh(db_takeoff)
    return db_takeoff

@app.get("/api/projects/{project_id}/takeoffs", response_model=list[TakeoffResponse])
def list_takeoffs(project_id: int, db: Session = next(get_db())):
    """List all takeoff items for a project"""
    takeoffs = db.query(TakeoffDB).filter(TakeoffDB.project_id == project_id).all()
    return takeoffs

@app.delete("/api/projects/{project_id}/takeoffs/{takeoff_id}")
def delete_takeoff(project_id: int, takeoff_id: int, db: Session = next(get_db())):
    """Delete a takeoff item"""
    db_takeoff = db.query(TakeoffDB).filter(
        TakeoffDB.id == takeoff_id,
        TakeoffDB.project_id == project_id
    ).first()
    if not db_takeoff:
        raise HTTPException(status_code=404, detail="Takeoff not found")
    
    db.delete(db_takeoff)
    db.commit()
    return {"status": "deleted"}

# ============================================================================
# SETTINGS ENDPOINTS
# ============================================================================

@app.post("/api/settings")
def update_setting(setting: SettingUpdate, db: Session = next(get_db())):
    """Update a setting"""
    db_setting = db.query(SettingsDB).filter(SettingsDB.key == setting.key).first()
    
    if db_setting:
        db_setting.value = setting.value
        db_setting.updated_at = datetime.utcnow()
    else:
        db_setting = SettingsDB(key=setting.key, value=setting.value)
        db.add(db_setting)
    
    db.commit()
    return {"key": setting.key, "value": setting.value}

@app.get("/api/settings/{key}")
def get_setting(key: str, db: Session = next(get_db())):
    """Get a setting"""
    setting = db.query(SettingsDB).filter(SettingsDB.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": setting.key, "value": setting.value}

# ============================================================================
# STATS ENDPOINTS (Real data from database)
# ============================================================================

@app.get("/api/stats")
def get_stats(db: Session = next(get_db())):
    """Get real system statistics"""
    total_projects = db.query(ProjectDB).count()
    complete_projects = db.query(ProjectDB).filter(ProjectDB.status == "complete").count()
    total_takeoffs = db.query(TakeoffDB).count()
    
    # Calculate total ccSPF
    total_ccspf = db.query(TakeoffDB).filter(TakeoffDB.material_type == "ccSPF").count()
    
    return {
        "total_projects": total_projects,
        "complete_projects": complete_projects,
        "total_takeoffs": total_takeoffs,
        "total_ccspf_items": total_ccspf,
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "EcoSeal Takeoff API"
    }

# ============================================================================
# ROOT
# ============================================================================

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "name": "EcoSeal Insulation Takeoff System",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
