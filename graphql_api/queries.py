from ariadne import QueryType


from services.patient_service import (
    get_patient,
    get_patients,
    count_appointments_by_patient
)

from services.address_service import get_address_by_cep

from services.scheduling_service import (
    get_appointments_by_patient_ids
)

from services.scheduling_service import get_appointments
from logger import logger
query = QueryType()


def get_requested_fields(info):
    return {
        field.name.value
        for field in info.field_nodes[0].selection_set.selections
    }


@query.field("patient")
def resolve_patient(_, info, id):
    logger.debug(f"GraphQL: buscando paciente #{id}")
    patient = get_patient(id)

    if not patient:
        return None

    return patient


@query.field("appointments")
def resolve_appointments(_, info, patientId):
    return get_appointments(patientId)


# @query.field("patients")
# def resolve_patients(_, info):
#     fields = get_requested_fields(info)

#     data = get_patients()
#     patients = data.get("patients", [])

#     return enrich_patients(
#         patients,
#         include_appointments="appointments" in fields
#     )

@query.field("patients")
def resolve_patients(_, info):
    data = get_patients()

    patients = data.get("patients", [])

    patient_ids = [
        patient["patient_id"]
        for patient in patients
    ]

    appointments = get_appointments_by_patient_ids(patient_ids)

    counts = count_appointments_by_patient(appointments)

    for patient in patients:
        patient_id = patient["patient_id"]

        patient["total_appointments"] = counts.get(
            patient_id,
            0
        )

    return patients

@query.field("addressByCep")
def resolve_address_by_cep(_, info, cep):
    return get_address_by_cep(cep)