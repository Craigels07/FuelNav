# FuelNav 🚗⛽  
**Optimized Fuel Route Planner**

FuelNav is a Django-based API service that helps drivers find the most cost-effective fueling strategy for long trips. Given a starting point, destination, and fuel price data along the route, FuelNav calculates where to stop for fuel to minimize total fuel cost, considering vehicle range constraints (e.g., 500 miles per tank).

---

## 🌍 Features

- 🔄 **Dynamic Route Chunking** – Splits long routes based on vehicle fuel range.
- ⛽ **Optimal Fuel Stops** – Chooses the cheapest city to refuel in each chunk.
- 📊 **Detailed Cost Summary** – Returns total cost and suggested fueling locations.
- 🚘 **Vehicle-Aware Planning** – Considers maximum range of a user's vehicle.

---

## 🛠️ Tech Stack

- **Backend:** Django 3.2.23 (Python)
- **API Framework:** Django REST Framework
- **Database:** PostgreSQL (or SQLite for local dev)
- **Geolocation:** Uses coordinates (lat/lng) to determine route & fuel stops
- **Deployment Ready:** Containerized setup with support for Railway

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Craigels07/FuelNav.git
cd FuelNav

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
