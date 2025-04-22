import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Paths
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "health_data.csv")

# Ensure directory and file
def ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Date", "Steps", "SleepHours", "Calories", "WaterLiters", "Weight", "Height", "BMI"
        ])
        df.to_csv(DATA_FILE, index=False)

# Load data
def load_data():
    return pd.read_csv(DATA_FILE, parse_dates=["Date"])

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Calculate BMI
def calculate_bmi(weight, height):
    if height == 0:
        return 0
    return round(weight / (height ** 2), 2)

# Log today's metrics
def log_daily_metrics(df):
    print("\n--- Log Today's Metrics ---")
    today = pd.to_datetime(datetime.today().date())
    try:
        steps = int(input("Steps walked: "))
        sleep = float(input("Sleep hours: "))
        calories = int(input("Calories consumed: "))
        water = float(input("Water intake (liters): "))
        weight = float(input("Weight (kg): "))
        height = float(input("Height (m): "))
    except ValueError:
        print("Invalid input.")
        return df

    bmi = calculate_bmi(weight, height)
    new_entry = pd.DataFrame([[today, steps, sleep, calories, water, weight, height, bmi]], columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)
    print(f"Data logged. Your BMI is {bmi}")
    return df

# View weekly report
def weekly_report(df):
    print("\n--- Weekly Health Report ---")
    today = pd.to_datetime(datetime.today())
    week_ago = today - timedelta(days=7)
    weekly_data = df[df["Date"] >= week_ago]
    if weekly_data.empty:
        print("No data for the past week.")
        return

    print("\nAverages (last 7 days):")
    print(weekly_data[["Steps", "SleepHours", "Calories", "WaterLiters", "BMI"]].mean().round(2))

    weekly_data.set_index("Date")[["Steps", "SleepHours", "Calories", "WaterLiters"]].plot(subplots=True, figsize=(10, 8), title="Weekly Health Stats")
    plt.tight_layout()
    plt.show()

# Calorie calculator (based on BMR estimation)
def calorie_calculator():
    print("\n--- Calorie Calculator ---")
    try:
        gender = input("Gender (M/F): ").strip().upper()
        weight = float(input("Weight (kg): "))
        height_cm = float(input("Height (cm): "))
        age = int(input("Age: "))
        activity = input("Activity Level (Sedentary, Light, Moderate, Active): ").strip().lower()
    except ValueError:
        print("Invalid input.")
        return

    if gender == "M":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    elif gender == "F":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
    else:
        print("Invalid gender.")
        return

    multiplier = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725
    }.get(activity, 1.2)

    calories = round(bmr * multiplier)
    print(f" Estimated daily calories to maintain weight: {calories} kcal")

# Hydration alert
def hydration_alert(df):
    today = pd.to_datetime(datetime.today().date())
    today_data = df[df["Date"] == today]
    if not today_data.empty and today_data["WaterLiters"].values[0] < 2:
        print(" Reminder: You're below 2L water intake today. Stay hydrated!")

# Main menu
def main():
    ensure_data_file()
    df = load_data()

    while True:
        print("\n Health & Fitness Tracker")
        print("1. Log Daily Metrics")
        print("2. View Weekly Report")
        print("3. BMI & Calorie Calculator")
        print("4. Hydration Reminder")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            df = log_daily_metrics(df)
            save_data(df)
        elif choice == "2":
            weekly_report(df)
        elif choice == "3":
            calorie_calculator()
        elif choice == "4":
            hydration_alert(df)
        elif choice == "5":
            save_data(df)
            print("Exited the program.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
