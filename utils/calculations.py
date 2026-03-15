def calculate_bmi(weight_kg, height_cm):
    """Calculates BMI from weight (kg) and height (cm)."""
    if not height_cm or not weight_kg:
        return 0, "Unknown"
    
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m ** 2)
    
    # Categories
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
        
    return round(bmi, 2), category

def calculate_maintenance_calories(age, gender, height_cm, weight_kg, activity_level):
    """
    Calculates maintenance calories using the Mifflin-St Jeor equation.
    Activity levels: 1.2 (sedentary), 1.375 (light), 1.55 (moderate), 1.725 (active), 1.9 (very active)
    """
    if not age or not height_cm or not weight_kg:
        return 0, 0, 0
        
    # BMR formula
    if gender.lower() == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
    # Activity multipliers
    activity_multiplier = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    
    mult = activity_multiplier.get(activity_level, 1.2)
    maintenance = int(bmr * mult)
    
    fat_loss = maintenance - 500
    muscle_gain = maintenance + 300
    
    return maintenance, fat_loss, muscle_gain
