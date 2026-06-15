# 🎬 CineDesk — Movie Booking System

A movie ticket booking application with a command-line backend (`Main.py`) and a dark-themed Streamlit web interface (`UI.PY`). Movie data is persisted in a local `movies.json` file.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Streamlit

### Install Dependencies

```bash
pip install streamlit
```

### Run the Web UI

```bash
streamlit run UI.PY
```

### Run the CLI Version

```bash
python Main.py
```

---

## 📁 Project Structure

```
project/
│
├── Main.py         # Command-line interface (CRUD logic)
├── UI.PY           # Streamlit web interface
├── movies.json     # Persistent data store (auto-created on first run)
└── README.md       # Project documentation
```

---

## 🖥️ Web UI Features (UI.PY)

The Streamlit interface is organized into four tabs:

| Tab | Description |
|-----|-------------|
| **Now Showing** | Lists all movies with color-coded seat availability badges |
| **Add Movie** | Register a new movie with a name and seat count |
| **Book Tickets** | Select a movie and reserve seats |
| **Cancel Tickets** | Release previously booked seats back to a movie |

### Seat Badge Colors

| Badge | Meaning |
|-------|---------|
| 🟡 Yellow | Seats available |
| 🔴 Red | 5 or fewer seats left |
| ⚫ Grey | Sold out |

---

## 💻 CLI Features (Main.py)

```
1. Add Movie      — Add a new movie with a name and seat count
2. Book Ticket    — Book one or more seats for a movie
3. Cancel Ticket  — Return seats for a movie
4. Show Movies    — List all movies and available seats
```

---

## 🗄️ Data Storage

All data is stored in `movies.json` in the same directory. Example structure:

```json
[
  {
    "movie_name": "Sholay",
    "available_seats": 101
  }
]
```

Both `Main.py` and `UI.PY` read from and write to the same file, so changes made in one are reflected in the other.

---

## ⚙️ How It Works

- **`MovieBooking` class** (`Main.py`) manages all booking logic using class-level state loaded from `movies.json` at startup.
- **Streamlit session state** (`UI.PY`) keeps movie data in memory during a session and syncs it to `movies.json` after every change.
- Both interfaces use `pathlib.Path` to safely check for file existence before reading.

---

## ⚠️ Notes

- Booking validation prevents reserving more seats than are available.
- Duplicate movie names are blocked in the web UI.
- The CLI does not validate duplicate movie names — avoid adding the same movie twice.
- Cancelling tickets does **not** validate against originally booked seats; it simply adds the given number back.

---

## 🛠️ Future Improvements

- Add user authentication for admin vs. customer roles.
- Track individual bookings with booking IDs.
- Add a delete-movie option in the web UI.
- Deploy to Streamlit Cloud for public access.
