from app.models.enums import EstadoGeneral, TipoProceso

DETALLES_POR_ESTADO = {
    EstadoGeneral.SOURCING: ["Sin responder", "En conversación"],
    
    EstadoGeneral.NO_COMIENZA: [
        "Sin ingles", "Rate mayor", "Faltan skills tecnicas", "No le interesa"
    ],
    
    EstadoGeneral.NO_CONTINUA: [
        "Desiste", "Baja en HR", "Baja en CC", "Baja en SD", 
        "Baja en CF", "Baja en Cliente", "Baja en Psicotecnico", 
        "Baja en Offer", "Baja en Ingreso"
    ],
    
    EstadoGeneral.EN_PROCESO: {
        TipoProceso.RENAISS_SIN_CLIENTE: ["HR", "CC", "SD", "CF", "Psicotecnico", "Offer", "Ingreso"],
        TipoProceso.RENAISS_CON_CLIENTE: ["HR", "CC", "SD", "CF", "Cliente", "Psicotecnico", "Offer", "Ingreso"],
        TipoProceso.STAFFED_CORTO: ["CF", "Cliente", "Offer"],
        TipoProceso.STAFFED_LARGO: ["HR", "CC", "SD", "CF", "Cliente", "Offer", "Ingreso"]
    }
}