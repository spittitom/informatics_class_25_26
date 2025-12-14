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




# # --- PRESCRIPTION ENDPOINTS ---

# @app.post("/prescriptions/", response_model=Prescription, status_code=201, tags=["Prescriptions"])
# async def create_prescription(p: PrescriptionBase):
#     """Creates a new prescription and deducts the quantity from stock (simulated)."""
#     if p.medication_id not in medications_db:
#         raise HTTPException(status_code=404, detail="Referenced medication not found")

#     # Simulation Step: Automatically adjust stock upon prescription creation
#     stock_change = -p.quantity # Deduction of quantity
    
#     # Ideally, we would encapsulate the PATCH logic here or start a transaction.
#     # For this task, we call the logic directly (Caution: Use transactions in real life!)
#     try:
#         med_update = StockUpdate(stock_change=stock_change)
#         updated_med = await update_medication_stock(p.medication_id, med_update)
#     except HTTPException as e:
#         # We pass on the error from the stock adjustment directly
#         raise HTTPException(status_code=400, detail=f"Stock deduction failed: {e.detail}")

#     # Creation of the prescription after stock was successfully adjusted
#     new_prescription = Prescription(
#         patient_id=p.patient_id,
#         medication_id=p.medication_id,
#         quantity=p.quantity,
#         instructions=p.instructions
#     )
#     prescriptions_db[new_prescription.id] = new_prescription
    
#     return new_prescription

# @app.get("/prescriptions/search", response_model=List[Prescription], tags=["Prescriptions"])
# async def search_prescriptions(
#     patient_id: Optional[int] = None, 
#     medication_id: Optional[UUID] = None
# ):
#     """Searches for prescriptions based on Patient ID or Medication ID."""
    
#     # Asynchronous filtering of data (Simulation of a DB query)
#     def filter_logic():
#         results = []
#         for p in prescriptions_db.values():
#             match_patient = patient_id is None or p.patient_id == patient_id
#             match_medication = medication_id is None or p.medication_id == medication_id
            
#             if match_patient and match_medication:
#                 results.append(p)
#         return results

#     # In a real application, you would use 'await' for the DB query here.
#     # Since our DB is an in-memory Dict, we can call the function synchronously.
#     return filter_logic()