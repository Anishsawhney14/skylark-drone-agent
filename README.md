# Skylark Drone Operations Coordinator AI Agent

## Overview

This project implements an AI agent that simulates the role of a Drone Operations Coordinator. The agent helps manage pilot assignments, drone assignments, inventory tracking, and conflict detection. It reads mission, pilot, and drone data from Google Sheets, validates assignment conditions, and updates assignments automatically.

The main objective of this system is to reduce manual coordination effort and ensure that pilots and drones are assigned correctly based on mission requirements.

The agent is deployed using Streamlit and can be accessed online.

---

## Live Application

Hosted application link:

https://skylark-drone-agent.streamlit.app

---

## GitHub Repository

Source code available at:

https://github.com/Anishsawhney14/skylark-drone-agent

---

## Features

### Pilot Management

- View pilot roster
- Check pilot availability
- Assign pilots to missions
- Prevent assignment if skill, certification, budget, or date conflict exists
- Update pilot assignment in Google Sheets automatically

### Drone Management

- View drone fleet
- Assign drones to missions
- Check maintenance status
- Check weather compatibility
- Update drone assignment in Google Sheets automatically

### Conflict Detection

The agent detects and prevents invalid assignments by checking:

- Skill mismatch
- Certification mismatch
- Budget exceeded
- Location mismatch
- Drone maintenance conflicts
- Weather incompatibility
- Date overlap conflicts (prevents double booking)

### Urgent Reassignment

The agent can handle urgent situations by:

- Releasing the currently assigned pilot and drone
- Finding alternative pilot and drone
- Assigning replacements automatically
- Updating Google Sheets in real time

---

## Architecture Overview

The system consists of three main components:

### 1. User Interface (app.py)

This file contains the Streamlit interface. It allows the user to enter commands and interact with the agent.

### 2. Agent Logic (agent.py)

This file contains the core logic of the system, including:

- Pilot assignment
- Drone assignment
- Conflict detection
- Date overlap validation
- Urgent reassignment

### 3. Google Sheets Integration (sheets.py)

This file handles the connection to Google Sheets and performs:

- Reading pilot, drone, and mission data
- Updating assignment status
- Synchronizing data in real time

---

## Data Source

The agent uses three Google Sheets:

- pilot_roster – contains pilot details and assignment status
- drone_fleet – contains drone availability and maintenance information
- missions – contains mission requirements and schedules

---

## Technologies Used

- Python
- Streamlit
- Google Sheets API
- gspread
- pandas

---

## Example Commands

The following commands can be used in the application:

show pilots

show drones

show missions

assign pilot PRJ001

assign drone PRJ001

urgent reassign PRJ001

---
## How It Works

1. User enters a command in the Streamlit interface
2. Agent reads data from Google Sheets
3. Agent checks conflicts and constraints
4. Agent assigns pilot and drone if valid
5. Agent updates Google Sheets

---

## Learning Outcomes

Through this project, I learned how to:

- Build an automation system for real-world coordination tasks
- Integrate Python with Google Sheets
- Implement conflict detection and scheduling logic
- Design assignment workflows
- Deploy applications using Streamlit Cloud

---

## Conclusion

This project successfully implements an AI agent that can manage pilot and drone assignments, detect conflicts, and automate coordination using Google Sheets. The system ensures that assignments are valid and helps reduce manual coordination effort.
