from ariadne import MutationType

from services.patient_service import (
    add_patient,
    delete_patient,
    update_patient
)
from services.scheduling_service import (
    add_appointment,
    delete_appointment
)

mutation = MutationType()

@mutation.field("addPatient")
def resolve_add_patient(
    _,
    info,
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
    return add_patient(
        name=name,
        birth_date=birth_date,
        tax_id=tax_id,
        phone=phone,
        email=email,
        cep=cep,
        logradouro=logradouro,
        complemento=complemento,
        bairro=bairro,
        localidade=localidade,
        uf=uf,
        profession=profession
    )


@mutation.field("addAppointment")
def resolve_add_appointment(
    _,
    info,
    date,
    notes,
    patient_id,
    reason,
):
    data = add_appointment(
        date=date,
        notes=notes,
        patient_id=patient_id,
        reason=reason,
    )

    if not data:
        return None

    return data

@mutation.field("updatePatient")
def resolve_update_patient(
    _,
    info,
    patientId,
    name=None,
    birth_date=None,
    tax_id=None,
    phone=None,
    email=None,
    cep=None,
    logradouro=None,
    complemento=None,
    bairro=None,
    localidade=None,
    uf=None,
    profession=None
):
    return update_patient(
        patient_id=patientId,
        name=name,
        birth_date=birth_date,
        tax_id=tax_id,
        phone=phone,
        email=email,
        cep=cep,
        logradouro=logradouro,
        complemento=complemento,
        bairro=bairro,
        localidade=localidade,
        uf=uf,
        profession=profession
    )


@mutation.field("deletePatient")
def resolve_delete_patient(_, info, patientId):
    return delete_patient(patientId)


@mutation.field("deleteAppointment")
def resolve_delete_appointment(_, info, appointmentId):
    return delete_appointment(appointmentId)