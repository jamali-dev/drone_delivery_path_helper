# src/energy.py
import numpy as np

def leg_energy_kJ(dist_m, payload_kg, battery_kg, alpha=0.12, beta=0.04):
    """
    Estimate energy use for one flight leg.
    Formula from Dorling et al. (2016):
    E ≈ α * distance + β * distance * (payload + battery)
    Returns energy in kilojoules (kJ).
    """
    mass_term = (payload_kg + battery_kg)
    return (alpha * dist_m + beta * dist_m * mass_term)

def check_battery(energy_kJ, battery_capacity_kJ):
    """
    Check if this flight fits within available battery capacity.
    """
    return energy_kJ <= 0.9 * battery_capacity_kJ
