
from .models import doctor


SYMPTOM_RULES = {
    "chest pain": ["Cardiologist", "Heart Specialist"],
    "heart problem": ["Cardiologist", "Heart Specialist"],
    "skin rash": ["Dermatologist", "Skin Specialist"],
    "itching": ["Dermatologist", "Skin Specialist"],
    "headache": ["Neurologist", "Brain Specialist", "Nuro"],
    "migraine": ["Neurologist", "Brain Specialist", "Nuro"],
    "bone pain": [
        "Orthopedic Surgeon",
        "Orthopedic Specialist",
        "Bone Specialist",
    ],
    "joint pain": [
        "Orthopedic Surgeon",
        "Orthopedic Specialist",
        "Bone Specialist",
    ],
    "child fever": ["Pediatrician", "Child Specialist"],
    "ear pain": ["ENT Specialist", "ENT Surgeon"],
    "sore throat": ["ENT Specialist", "ENT Surgeon"],
    "eye pain": ["Ophthalmologist", "Eye Specialist"],
    "blurred vision": ["Ophthalmologist", "Eye Specialist"],
    "fever": ["General Physician", "Internal Medicine"],
    "cough": ["General Physician", "Internal Medicine"],
}


def find_specializations(symptoms):
    if symptoms is None:
        return []

    normalized_symptoms = " ".join(
        str(symptoms).lower().replace(",", " ").split()
    )

    if not normalized_symptoms:
        return []

    matched_specializations = set()

    for symptom, specializations in SYMPTOM_RULES.items():
        if symptom in normalized_symptoms:
            matched_specializations.update(specializations)

    return sorted(matched_specializations)


def recommend_doctors(symptoms):
    specializations = find_specializations(symptoms)

    if not specializations:
        return doctor.objects.none()

    return (
        doctor.objects.filter(
            doctor_specialisation__in=specializations
        )
        .select_related("dept_name")
        .order_by("doctor_name")
        .distinct()
    )


# Keep the old function name working too.
recommend_doctor = recommend_doctors
