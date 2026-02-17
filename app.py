import streamlit as st
from agent import assign_pilot, assign_drone, urgent_reassign
from sheets import load_sheet

# App title
st.title("Skylark Drone Operations AI Agent")

st.write("Enter command:")

# Input box
command = st.text_input("Command")

if command:

    cmd = command.lower().strip()

    # Assign pilot
    if cmd.startswith("assign pilot"):

        mission_id = command.split()[-1].upper()

        result = assign_pilot(mission_id)

        st.success(result)

    # Assign drone
    elif cmd.startswith("assign drone"):

        mission_id = command.split()[-1].upper()

        result = assign_drone(mission_id)

        st.success(result)

    # Urgent reassignment (NEW FEATURE)
    elif cmd.startswith("urgent reassign"):

        mission_id = command.split()[-1].upper()

        result = urgent_reassign(mission_id)

        st.success(result)

    # Show pilots
    elif cmd == "show pilots":

        pilots = load_sheet("pilot_roster")

        st.subheader("Pilot Roster")
        st.dataframe(pilots)

    # Show drones
    elif cmd == "show drones":

        drones = load_sheet("drone_fleet")

        st.subheader("Drone Fleet")
        st.dataframe(drones)

    # Show missions
    elif cmd == "show missions":

        missions = load_sheet("missions")

        st.subheader("Missions")
        st.dataframe(missions)

    # Unknown command
    else:

        st.error("Command not recognized")
