import pandas as pd

# -----------------------------------
# EMISSION FACTORS
# -----------------------------------
EMISSION_FACTORS = {
    "diesel": 2.68,
    "petrol": 2.31,
    "electricity": 0.82,
    "flight": 0.15,
    "train": 0.05,
    "taxi": 0.12
}

# -----------------------------------
# UNIT NORMALIZATION
# -----------------------------------
def normalize_unit(value, unit):
    if pd.isna(value):
        return 0

    unit = str(unit).lower()

    if unit in ["l", "litre", "liters"]:
        return float(value)

    if unit in ["gallon", "gallons"]:
        return float(value) * 3.785

    if unit in ["kwh"]:
        return float(value)

    return float(value)


# -----------------------------------
# SAP NORMALIZATION
# -----------------------------------
def normalize_sap(row):
    try:
        fuel_type = str(row.get("fuel_type", "")).lower()
        quantity = normalize_unit(row.get("quantity", 0), row.get("unit", ""))

        factor = EMISSION_FACTORS.get(fuel_type, 2.5)

        emissions = quantity * factor

        suspicious = False
        if quantity < 0 or quantity > 100000:
            suspicious = True

        return {
            "activity_value": quantity,
            "emissions": emissions,
            "suspicious": suspicious
        }

    except:
        return {
            "activity_value": 0,
            "emissions": 0,
            "suspicious": True
        }


# -----------------------------------
# UTILITY NORMALIZATION
# -----------------------------------
def normalize_utility(row):
    try:
        kwh = float(row.get("usage_kwh", 0))
        emissions = kwh * EMISSION_FACTORS["electricity"]

        suspicious = kwh < 0 or kwh > 100000

        return {
            "activity_value": kwh,
            "emissions": emissions,
            "suspicious": suspicious
        }

    except:
        return {
            "activity_value": 0,
            "emissions": 0,
            "suspicious": True
        }


# -----------------------------------
# TRAVEL NORMALIZATION
# -----------------------------------
def normalize_travel(row):
    try:
        travel_type = str(row.get("travel_type", "")).lower()
        distance = float(row.get("distance_km", 0))

        factor = EMISSION_FACTORS.get(travel_type, 0.1)

        emissions = distance * factor

        suspicious = distance < 0 or distance > 50000

        return {
            "activity_value": distance,
            "emissions": emissions,
            "suspicious": suspicious
        }

    except:
        return {
            "activity_value": 0,
            "emissions": 0,
            "suspicious": True
        }


# -----------------------------------
# MAIN UNIFIED NORMALIZER (IMPORTANT)
# -----------------------------------
def normalize_record(row, source_type):

    source_type = str(source_type).upper()

    if source_type == "SAP":
        result = normalize_sap(row)

    elif source_type == "UTILITY":
        result = normalize_utility(row)

    elif source_type == "TRAVEL":
        result = normalize_travel(row)

    else:
        result = {
            "activity_value": 0,
            "emissions": 0,
            "suspicious": True
        }

    # FINAL STANDARD OUTPUT FORMAT
    return {
        "activity_value": result["activity_value"],
        "emissions_kg_co2e": result["emissions"],
        "suspicious": result["suspicious"]
    }