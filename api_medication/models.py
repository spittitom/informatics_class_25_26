from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class MedicationBase(BaseModel):
    name: str = Field(..., example="Amoxicillin 500mg")
    dosage: str = Field(..., example="500mg")
    manufacturer: str = Field(..., example="PharmaCorp")
    
class MedicationCreate(MedicationBase):
    pass # Only base fields are needed for creation

class Medication(MedicationBase):
    id: UUID = Field(default_factory=uuid4)
    stock_level: int = Field(default=0, ge=0) # Stock level must be >= 0
    
    class Config:
        # Allows Pydantic to synchronize with non-dict types (like our 'database' dictionary)
        from_attributes = True

class StockUpdate(BaseModel):
    stock_change: int = Field(..., description="+ or - change in stock.", example=50)

class PrescriptionBase(BaseModel):
    patient_id: int = Field(..., example=101)
    medication_id: UUID
    quantity: int = Field(..., gt=0)
    instructions: str = Field(..., example="Take one capsule every 8 hours.")
    
class Prescription(PrescriptionBase):
    id: UUID = Field(default_factory=uuid4)
    status: str = Field(default="Active") # e.g., Active, Filled, Cancelled
    
    class Config:
        from_attributes = True



