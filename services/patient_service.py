import os
import requests
import time
from logger import logger

from services.scheduling_service import get_appointments

PATIENT_BACKEND_URL = os.getenv(
    "PATIENT_BACKEND_URL",
    "http://127.0.0.1:5000"
)


def get_patient(patient_id):
    response = requests.get(
        f"{PATIENT_BACKEND_URL}/patient/{patient_id}",
        timeout=5
    )

    if response.status_code == 404:
        return None
    
    response.raise_for_status()

    patient = response.json()

    patient["appointments"] = get_appointments(patient_id)

    return patient

def get_patients():
    response = requests.get(
        f"{PATIENT_BACKEND_URL}/patients",
        timeout=5
    )

    response.raise_for_status()

    return response.json()


def group_appointments_by_patient(appointments):
    grouped = {}

    for appointment in appointments:
        patient_id = appointment["patient_id"]

        grouped.setdefault(patient_id, []).append(
            appointment
        )

    return grouped


def count_appointments_by_patient(appointments):
    counts = {}

    for appointment in appointments:
        patient_id = appointment["patient_id"]

        counts[patient_id] = counts.get(patient_id, 0) + 1

    return counts


def add_patient(
    name,
    birth_date,
    tax_id,
    phone,
    email,
    cep,
    logradouro,
    complemento,
    bairro,
    localidade,
    uf,
    profession
):
    response = requests.post(
        f"{PATIENT_BACKEND_URL}/patient",
        json={
            "name": name,
            "birth_date": birth_date,
            "tax_id": tax_id,
            "phone": phone,
            "email": email,
            "cep": cep,
            "logradouro": logradouro,
            "complemento": complemento,
            "bairro": bairro,
            "localidade": localidade,
            "uf": uf,
            "profession": profession,
        },
        timeout=5
    )

    if response.status_code == 409:
        try:
            error_data = response.json()

            if isinstance(error_data, dict):
                message = (
                    error_data.get("message")
                    or error_data.get("error")
                    or "CPF ou e-mail já cadastrado."
                )
            else:
                message = "CPF ou e-mail já cadastrado."

        except ValueError:
            message = "CPF ou e-mail já cadastrado."

        raise Exception(message)

    response.raise_for_status()

    return response.json()


def delete_patient(patient_id):
    response = requests.delete(
        f"{PATIENT_BACKEND_URL}/patient/{patient_id}",
        timeout=5
    )

    if response.status_code == 404:
        return False

    response.raise_for_status()

    return True


def update_patient(
    patient_id,
    name,
    birth_date,
    tax_id,
    phone,
    email,
    cep,
    logradouro,
    complemento,
    bairro,
    localidade,
    uf,
    profession,
):
    response = requests.put(
        f"{PATIENT_BACKEND_URL}/patient/{patient_id}",
        json={
            "name": name,
            "birth_date": birth_date,
            "tax_id": tax_id,
            "phone": phone,
            "email": email,
            "cep": cep,
            "logradouro": logradouro,
            "complemento": complemento,
            "bairro": bairro,
            "localidade": localidade,
            "uf": uf,
            "profession": profession,
        },
        timeout=5,
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()