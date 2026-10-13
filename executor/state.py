"""Máquina de estados de una orden de HORUS. Toda transición no listada es un
error de programación y se rechaza (nunca se fuerza un estado)."""

RECEIVED, ACCEPTED, REJECTED = "RECEIVED", "ACCEPTED", "REJECTED"
WAITING_ENTRY, ENTERING, OPEN, EXITING, CLOSED = "WAITING_ENTRY", "ENTERING", "OPEN", "EXITING", "CLOSED"
INVALIDATED, EXPIRED, CANCELLED = "INVALIDATED", "EXPIRED", "CANCELLED"
HALTED = "HALTED_NEEDS_INSTRUCTION"

TERMINAL = {REJECTED, INVALIDATED, EXPIRED, CANCELLED, CLOSED}

TRANSITIONS = {
    RECEIVED: {ACCEPTED, REJECTED},
    ACCEPTED: {WAITING_ENTRY, CANCELLED, EXPIRED, HALTED},
    WAITING_ENTRY: {ENTERING, INVALIDATED, EXPIRED, CANCELLED, HALTED},
    # ENTERING: las ejecuciones parciales se informan con filled_qty dentro del estado
    ENTERING: {OPEN, CLOSED, EXPIRED, CANCELLED, HALTED},
    OPEN: {EXITING, CANCELLED, HALTED},
    EXITING: {CLOSED, HALTED},
    HALTED: {CANCELLED, EXITING},
}


def can_transition(a, b):
    return b in TRANSITIONS.get(a, set())


class TransitionError(ValueError):
    pass
