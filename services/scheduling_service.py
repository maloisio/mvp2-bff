import os
import requests


SCHEDULING_BACKEND_URL = os.getenv(
    "SCHEDULING_BACKEND_URL",
    "http://127.0.0.1:5001"
)


def get_appointments(patient_id):
    response = requests.get(
        f"{SCHEDULING_BACKEND_URL}/appointments/patient/{patient_id}",
        timeout=5
    )

    response.raise_for_status()

    return response.json()["appointments"]

def get_appointments_by_patient_ids(patient_ids):
    if not patient_ids:
        return []

    response = requests.get(
        f"{SCHEDULING_BACKEND_URL}/appointments/batch",
        params={
            "patient_ids": ",".join(map(str, patient_ids))
        },
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    return data.get("appointments", [])


def add_appointment(
    date,
    notes,
    patient_id,
    reason
):
    response = requests.post(
        f"{SCHEDULING_BACKEND_URL}/appointment",
        json={
            "date": date,
            "notes": notes,
            "patient_id": patient_id,
            "reason": reason
        },
        timeout=5
    )

    if response.status_code == 404:
        return None
    response.raise_for_status()

    return response.json()


def delete_appointment(appointment_id):
    response = requests.delete(
        f"{SCHEDULING_BACKEND_URL}/appointment/{appointment_id}",
        timeout=5
    )

    if response.status_code == 404:
        return False

    response.raise_for_status()

    return True