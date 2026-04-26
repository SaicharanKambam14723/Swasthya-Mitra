from app.db.database import SessionLocal
from app.models.disease import Disease
from app.models.medicine import Medicine

db = SessionLocal()

# =========================
# 🧠 DISEASES
# =========================
diseases_data = [
    {"name": "Common Cold", "description": "Viral infection affecting nose and throat", "severity": "low", "category": "viral"},
    {"name": "Flu", "description": "Influenza virus infection", "severity": "medium", "category": "viral"},
    {"name": "Fever", "description": "Elevated body temperature", "severity": "low", "category": "general"},
    {"name": "Migraine", "description": "Severe headache", "severity": "medium", "category": "neurological"},
    {"name": "Diabetes", "description": "High blood sugar levels", "severity": "high", "category": "chronic"},
    {"name": "Hypertension", "description": "High blood pressure", "severity": "high", "category": "cardiac"},
    {"name": "Asthma", "description": "Airway inflammation", "severity": "medium", "category": "respiratory"},
    {"name": "COVID-19", "description": "Respiratory viral infection", "severity": "high", "category": "viral"},
    {"name": "Allergy", "description": "Immune response to allergens", "severity": "low", "category": "immune"},
    {"name": "Gastritis", "description": "Stomach inflammation", "severity": "medium", "category": "digestive"},
    {"name": "Diarrhea", "description": "Loose stools", "severity": "low", "category": "digestive"},
    {"name": "Constipation", "description": "Difficulty passing stool", "severity": "low", "category": "digestive"},
    {"name": "Bronchitis", "description": "Inflammation of bronchial tubes", "severity": "medium", "category": "respiratory"},
    {"name": "Sinusitis", "description": "Sinus infection", "severity": "medium", "category": "respiratory"},
    {"name": "Skin Infection", "description": "Bacterial skin infection", "severity": "low", "category": "dermatology"},
    {"name": "Anemia", "description": "Low hemoglobin levels", "severity": "medium", "category": "blood"},
    {"name": "Arthritis", "description": "Joint inflammation", "severity": "medium", "category": "orthopedic"},
    {"name": "Depression", "description": "Mental health disorder", "severity": "high", "category": "mental"},
    {"name": "Anxiety", "description": "Excessive worry", "severity": "medium", "category": "mental"},
    {"name": "Insomnia", "description": "Sleep disorder", "severity": "low", "category": "neurological"},
    {"name": "Urinary Infection", "description": "Urinary tract infection", "severity": "medium", "category": "infection"},
    {"name": "Thyroid Disorder", "description": "Hormonal imbalance", "severity": "medium", "category": "endocrine"},
    {"name": "Obesity", "description": "Excess body fat", "severity": "medium", "category": "chronic"},
    {"name": "Heart Disease", "description": "Cardiac condition", "severity": "high", "category": "cardiac"},
    {"name": "Food Poisoning", "description": "Contaminated food illness", "severity": "medium", "category": "digestive"},
]

# =========================
# 💊 MEDICINES
# =========================
medicines_data = [
    # Allopathic
    {"name": "Paracetamol", "type": "allopathic", "description": "Reduces fever and pain", "dosage": "500mg twice daily"},
    {"name": "Ibuprofen", "type": "allopathic", "description": "Anti-inflammatory pain reliever", "dosage": "400mg after meals"},
    {"name": "Cetirizine", "type": "allopathic", "description": "Antihistamine", "dosage": "10mg once daily"},
    {"name": "Azithromycin", "type": "allopathic", "description": "Antibiotic", "dosage": "500mg once daily"},
    {"name": "Metformin", "type": "allopathic", "description": "Controls blood sugar", "dosage": "500mg twice daily"},
    {"name": "Amlodipine", "type": "allopathic", "description": "Blood pressure control", "dosage": "5mg daily"},
    {"name": "Salbutamol", "type": "allopathic", "description": "Asthma inhaler", "dosage": "As prescribed"},
    {"name": "Omeprazole", "type": "allopathic", "description": "Reduces stomach acid", "dosage": "20mg daily"},
    {"name": "ORS", "type": "allopathic", "description": "Rehydration solution", "dosage": "As needed"},

    # Ayurvedic
    {"name": "Tulsi Extract", "type": "ayurvedic", "description": "Boosts immunity", "dosage": "Twice daily"},
    {"name": "Ashwagandha", "type": "ayurvedic", "description": "Stress relief", "dosage": "Once daily"},
    {"name": "Ginger Extract", "type": "ayurvedic", "description": "Improves digestion", "dosage": "After meals"},
    {"name": "Triphala", "type": "ayurvedic", "description": "Digestive support", "dosage": "Before sleep"},
    {"name": "Giloy", "type": "ayurvedic", "description": "Immunity booster", "dosage": "Twice daily"},
    {"name": "Neem Extract", "type": "ayurvedic", "description": "Blood purifier", "dosage": "Once daily"},
]

# =========================
# INSERT DATA
# =========================
disease_objs = {}
for d in diseases_data:
    obj = Disease(**d)
    db.add(obj)
    db.flush()
    disease_objs[d["name"]] = obj

medicine_objs = {}
for m in medicines_data:
    obj = Medicine(**m)
    db.add(obj)
    db.flush()
    medicine_objs[m["name"]] = obj

db.commit()

# =========================
# 🔗 MAPPING
# =========================
mapping = {
    "Common Cold": ["Paracetamol", "Tulsi Extract", "Giloy"],
    "Flu": ["Paracetamol", "Ibuprofen", "Tulsi Extract"],
    "Fever": ["Paracetamol", "Giloy"],
    "Migraine": ["Ibuprofen", "Ashwagandha"],
    "Diabetes": ["Metformin", "Neem Extract"],
    "Hypertension": ["Amlodipine", "Ashwagandha"],
    "Asthma": ["Salbutamol", "Tulsi Extract"],
    "COVID-19": ["Paracetamol", "Azithromycin", "Giloy"],
    "Allergy": ["Cetirizine", "Neem Extract"],
    "Gastritis": ["Omeprazole", "Ginger Extract", "Triphala"],
    "Diarrhea": ["ORS", "Ginger Extract"],
    "Constipation": ["Triphala"],
    "Bronchitis": ["Azithromycin", "Tulsi Extract"],
    "Sinusitis": ["Cetirizine", "Steam Therapy"],
    "Anemia": ["Ashwagandha"],
    "Arthritis": ["Ibuprofen", "Ashwagandha"],
    "Depression": ["Ashwagandha"],
    "Anxiety": ["Ashwagandha"],
    "Insomnia": ["Ashwagandha"],
    "Food Poisoning": ["ORS", "Ginger Extract"],
}

for disease_name, meds in mapping.items():
    disease = disease_objs.get(disease_name)
    for med_name in meds:
        med = medicine_objs.get(med_name)
        if disease and med:
            disease.medicines.append(med)

db.commit()

print("✅ Seed data inserted successfully!")