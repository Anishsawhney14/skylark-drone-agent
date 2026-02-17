from sheets import load_sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time


# =====================================================
# DATE OVERLAP CHECK
# =====================================================

def is_date_overlap(start1, end1, start2, end2):

    start1 = datetime.strptime(start1, "%Y-%m-%d")
    end1 = datetime.strptime(end1, "%Y-%m-%d")

    start2 = datetime.strptime(start2, "%Y-%m-%d")
    end2 = datetime.strptime(end2, "%Y-%m-%d")

    return start1 <= end2 and start2 <= end1


# =====================================================
# GOOGLE SHEETS CONNECTION
# =====================================================

def get_client():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )

    client = gspread.authorize(creds)

    return client


# =====================================================
# PILOT CONFLICT DETECTION (FULLY UPDATED)
# =====================================================

def detect_pilot_conflicts(pilot, mission):

    conflicts = []

    # Skill mismatch
    if mission["required_skills"].lower() not in pilot["skills"].lower():
        conflicts.append("Skill mismatch")

    # Certification mismatch
    if mission["required_certs"].lower() not in pilot["certifications"].lower():
        conflicts.append("Certification mismatch")

    # Location mismatch
    if pilot["location"] != mission["location"]:
        conflicts.append("Location mismatch")

    # Budget conflict
    daily_rate = pilot["daily_rate_inr"]

    start_date = datetime.strptime(mission["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(mission["end_date"], "%Y-%m-%d")

    days = (end_date - start_date).days + 1
    total_cost = daily_rate * days

    if total_cost > mission["mission_budget_inr"]:
        conflicts.append("Budget exceeded")

    # ADVANCED DATE OVERLAP DETECTION
    if pilot["current_assignment"] not in ["", "-", None]:

        missions_df = load_sheet("missions")

        assigned_mission_id = pilot["current_assignment"]

        assigned_mission = missions_df[
            missions_df["project_id"] == assigned_mission_id
        ]

        if not assigned_mission.empty:

            assigned_start = assigned_mission.iloc[0]["start_date"]
            assigned_end = assigned_mission.iloc[0]["end_date"]

            new_start = mission["start_date"]
            new_end = mission["end_date"]

            if is_date_overlap(
                assigned_start, assigned_end,
                new_start, new_end
            ):
                conflicts.append(
                    f"Pilot already assigned to overlapping mission ({assigned_mission_id})"
                )

    return conflicts


# =====================================================
# DRONE CONFLICT DETECTION (FULLY UPDATED)
# =====================================================

def detect_drone_conflicts(drone, mission):

    conflicts = []

    # Location mismatch
    if drone["location"] != mission["location"]:
        conflicts.append("Location mismatch")

    # Maintenance conflict
    maintenance_due = datetime.strptime(
        drone["maintenance_due"], "%Y-%m-%d"
    )

    if maintenance_due <= datetime.today():
        conflicts.append("Drone due for maintenance")

    # Weather conflict
    weather = mission["weather_forecast"]
    resistance = drone["weather_resistance"]

    if weather.lower() == "rainy":
        if "IP43" not in resistance:
            conflicts.append("Drone not rain compatible")

    # ADVANCED DATE OVERLAP DETECTION
    if drone["current_assignment"] not in ["", "-", None]:

        missions_df = load_sheet("missions")

        assigned_mission_id = drone["current_assignment"]

        assigned_mission = missions_df[
            missions_df["project_id"] == assigned_mission_id
        ]

        if not assigned_mission.empty:

            assigned_start = assigned_mission.iloc[0]["start_date"]
            assigned_end = assigned_mission.iloc[0]["end_date"]

            new_start = mission["start_date"]
            new_end = mission["end_date"]

            if is_date_overlap(
                assigned_start, assigned_end,
                new_start, new_end
            ):
                conflicts.append(
                    f"Drone already assigned to overlapping mission ({assigned_mission_id})"
                )

    return conflicts


# =====================================================
# PILOT ASSIGNMENT
# =====================================================

def assign_pilot(mission_id):

    missions = load_sheet("missions")
    pilots = load_sheet("pilot_roster")

    mission = missions[
        missions["project_id"] == mission_id
    ].iloc[0]

    valid_pilot = None

    for index, pilot in pilots.iterrows():

        conflicts = detect_pilot_conflicts(pilot, mission)

        if len(conflicts) == 0:
            valid_pilot = pilot
            break

    if valid_pilot is None:
        return "No valid pilot available due to conflicts"

    client = get_client()

    sheet = client.open("pilot_roster").sheet1

    records = sheet.get_all_records()

    for i, row in enumerate(records):

        if row["pilot_id"] == valid_pilot["pilot_id"]:

            sheet.update_cell(i+2, 6, "Assigned")
            sheet.update_cell(i+2, 7, mission_id)

            break

    return f"Pilot {valid_pilot['name']} assigned successfully to {mission_id}"


# =====================================================
# DRONE ASSIGNMENT
# =====================================================

def assign_drone(mission_id):

    missions = load_sheet("missions")
    drones = load_sheet("drone_fleet")

    mission = missions[
        missions["project_id"] == mission_id
    ].iloc[0]

    valid_drone = None

    for index, drone in drones.iterrows():

        conflicts = detect_drone_conflicts(drone, mission)

        if len(conflicts) == 0:
            valid_drone = drone
            break

    if valid_drone is None:
        return "No valid drone available due to conflicts"

    client = get_client()

    sheet = client.open("drone_fleet").sheet1

    records = sheet.get_all_records()

    for i, row in enumerate(records):

        if row["drone_id"] == valid_drone["drone_id"]:

            sheet.update_cell(i+2, 4, "Assigned")
            sheet.update_cell(i+2, 6, mission_id)

            break

    return f"Drone {valid_drone['drone_id']} assigned successfully to {mission_id}"


# =====================================================
# ASSIGN PILOT EXCLUDING SPECIFIC NAME
# =====================================================

def assign_pilot_excluding(mission_id, excluded_name):

    missions = load_sheet("missions")
    pilots = load_sheet("pilot_roster")

    mission = missions[
        missions["project_id"] == mission_id
    ].iloc[0]

    valid_pilot = None

    for index, pilot in pilots.iterrows():

        if pilot["name"] == excluded_name:
            continue

        conflicts = detect_pilot_conflicts(pilot, mission)

        if len(conflicts) == 0:
            valid_pilot = pilot
            break

    if valid_pilot is None:
        return "No alternative pilot available"

    client = get_client()

    sheet = client.open("pilot_roster").sheet1

    records = sheet.get_all_records()

    for i, row in enumerate(records):

        if row["pilot_id"] == valid_pilot["pilot_id"]:

            sheet.update_cell(i+2, 6, "Assigned")
            sheet.update_cell(i+2, 7, mission_id)

            break

    return f"Pilot {valid_pilot['name']} assigned successfully to {mission_id}"


# =====================================================
# URGENT REASSIGNMENT
# =====================================================

def urgent_reassign(mission_id):

    client = get_client()

    pilot_sheet = client.open("pilot_roster").sheet1
    drone_sheet = client.open("drone_fleet").sheet1

    pilot_records = pilot_sheet.get_all_records()
    drone_records = drone_sheet.get_all_records()

    released_pilot = None
    released_drone = None

    # Release pilot
    for i, row in enumerate(pilot_records):

        if row["current_assignment"] == mission_id:

            pilot_sheet.update_cell(i+2, 6, "Available")
            pilot_sheet.update_cell(i+2, 7, "")

            released_pilot = row["name"]

            time.sleep(1)
            break

    # Release drone
    for i, row in enumerate(drone_records):

        if row["current_assignment"] == mission_id:

            drone_sheet.update_cell(i+2, 4, "Available")
            drone_sheet.update_cell(i+2, 6, "")

            released_drone = row["drone_id"]

            time.sleep(1)
            break

    # Assign new ones
    pilot_result = assign_pilot_excluding(mission_id, released_pilot)

    drone_result = assign_drone(mission_id)

    return (
        f"Urgent reassignment completed\n\n"
        f"Released Pilot: {released_pilot}\n"
        f"Released Drone: {released_drone}\n\n"
        f"{pilot_result}\n"
        f"{drone_result}"
    )
