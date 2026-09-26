from ariadne import gql


type_defs = gql("""
    type Patient {
        patient_id: ID!
        name: String!
        birth_date: String
        tax_id: String
        phone: String
        email: String
        cep: String
        logradouro: String
        complemento: String
        bairro: String
        localidade: String
        uf: String
        profession: String
        total_appointments: Int
        appointments: [Appointment!]!
    }

    type Appointment {
        appointment_id: ID!
        patient_id: ID!
        date: String!
        reason: String!
        notes: String
    }

    type Query {
        patient(id: ID!): Patient
        patients: [Patient!]!
        appointments(patientId: ID!): [Appointment!]!
        addressByCep(cep: String!): Address
    }
    
    type Address {
        cep: String
        logradouro: String
        complemento: String
        bairro: String
        localidade: String
        uf: String
    }

    type Mutation {
        addPatient(
            name: String!
            birth_date: String!
            tax_id: String!
            phone: String!
            email: String!
            cep: String!
            logradouro: String!
            complemento: String
            bairro: String!
            localidade: String!
            uf: String!
            profession: String!
        ): Patient

        addAppointment(
            date: String!
            notes: String
            patient_id: ID!
            reason: String!
        ): Appointment

        updatePatient(
            patientId: ID!
            name: String
            birth_date: String
            tax_id: String
            phone: String
            email: String
            cep: String
            logradouro: String
            complemento: String
            bairro: String
            localidade: String
            uf: String
            profession: String
        ): Patient

        deletePatient(patientId: ID!): Boolean!

        deleteAppointment(appointmentId: ID!): Boolean!
    }
""")