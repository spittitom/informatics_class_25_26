from models import Medication, MedicationCreate, Prescription, PrescriptionBase, StockUpdate
from fastapi import FastAPI, HTTPException
from typing import Dict, List, Optional
from uuid import UUID

# Init the in-memory "Database"
# We use Dictionaries to simulate tables
medications_db: Dict[UUID, Medication] = {}
prescriptions_db: Dict[UUID, Prescription] = {}

app = FastAPI(title="HealthCare Medication API", version="0.0.1")

# --- MEDICATION ENDPOINTS ---

@app.post("/medications/", response_model=Medication, status_code=201, tags=["Medications"])
async def create_medication(med: MedicationCreate):
    """Adds a new medication to the inventory."""
    new_med = Medication(
        name=med.name,
        dosage=med.dosage,
        manufacturer=med.manufacturer
        # id and stock_level are automatically set by Pydantic/FieldDefaults
    )
    medications_db[new_med.id] = new_med
    return new_med

@app.get("/medications/{med_id}", response_model=Medication, tags=["Medications"])
async def read_medication(med_id: UUID):    
    """Retrieves the details of a specific medication."""
    if med_id not in medications_db:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medications_db[med_id]

@app.patch("/medications/{med_id}/stock", response_model=Medication, tags=["Medications"])
async def update_medication_stock(med_id: UUID, stock_update: StockUpdate):   
    """Updates the stock level of a medication (inflow/outflow)."""
    if med_id not in medications_db:
        raise HTTPException(status_code=404, detail="Medication not found")

    current_med = medications_db[med_id]
    new_stock = current_med.stock_level + stock_update.stock_change

    # Advanced Validation: Stock must not become negative
    if new_stock < 0:
        raise HTTPException(status_code=400, 
                detail=f"Stock update would lead to a negative stock level: {new_stock}")

    # Updating the object and storing it
    current_med.stock_level = new_stock
    medications_db[med_id] = current_med # Re-assignment for clarity
    
    return current_med


