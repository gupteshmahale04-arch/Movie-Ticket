import json
import streamlit as st
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineDesk",
    page_icon="🎬",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark cinematic background */
.stApp {
    background-color: #0d0d0f;
    color: #e8e4dc;
}

/* Masthead */
.masthead {
    text-align: center;
    padding: 2.5rem 0 1rem;
    border-bottom: 1px solid #2a2a2e;
    margin-bottom: 2rem;
}
.masthead h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    letter-spacing: -1px;
    color: #f5c842;
    margin: 0;
}
.masthead p {
    font-size: 0.85rem;
    color: #6b6b72;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* Tab strip */
[data-testid="stHorizontalBlock"] { gap: 0.5rem; }

/* Cards */
.movie-card {
    background: #18181c;
    border: 1px solid #2a2a2e;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.movie-card .title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: #f0ebe0;
}
.movie-card .seats {
    font-size: 0.8rem;
    color: #6b6b72;
    margin-top: 0.1rem;
}
.badge {
    background: #f5c842;
    color: #0d0d0f;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
}
.badge-low { background: #e05c4b; color: #fff; }
.badge-empty { background: #3a3a3f; color: #aaa; }

/* Section label */
.section-label {
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6b6b72;
    margin-bottom: 0.5rem;
}

/* Override Streamlit input backgrounds */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #18181c !important;
    border: 1px solid #2a2a2e !important;
    color: #e8e4dc !important;
    border-radius: 6px !important;
}

/* Buttons */
.stButton > button {
    background: #f5c842;
    color: #0d0d0f;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.4rem;
    font-size: 0.9rem;
}
.stButton > button:hover {
    background: #fad356;
    color: #0d0d0f;
}

/* Tabs */
.stTabs [data-testid="stTab"] {
    background: transparent;
    color: #6b6b72;
    border-bottom: 2px solid transparent;
    font-size: 0.9rem;
}
.stTabs [aria-selected="true"] {
    color: #f5c842 !important;
    border-bottom: 2px solid #f5c842 !important;
}

/* Divider */
hr { border-color: #2a2a2e; }

/* Success / error */
.stAlert { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Data layer ────────────────────────────────────────────────────────────────
DATABASE = "movies.json"

def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []

def save_data(data):
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data, indent=2))

if "movies" not in st.session_state:
    st.session_state.movies = load_data()

def movies():
    return st.session_state.movies

# ── Masthead ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <h1>🎬 CineDesk</h1>
  <p>Movie booking management</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_show, tab_add, tab_book, tab_cancel = st.tabs(
    ["  Now Showing  ", "  Add Movie  ", "  Book Tickets  ", "  Cancel Tickets  "]
)

# ── NOW SHOWING ───────────────────────────────────────────────────────────────
with tab_show:
    st.markdown('<p class="section-label">All movies in the system</p>', unsafe_allow_html=True)

    if not movies():
        st.info("No movies yet — add one in the **Add Movie** tab.")
    else:
        for m in movies():
            seats = m["available_seats"]
            if seats == 0:
                badge = '<span class="badge badge-empty">Sold out</span>'
            elif seats <= 5:
                badge = f'<span class="badge badge-low">{seats} left</span>'
            else:
                badge = f'<span class="badge">{seats} seats</span>'

            st.markdown(f"""
            <div class="movie-card">
              <div>
                <div class="title">{m["movie_name"]}</div>
                <div class="seats">Available seats</div>
              </div>
              {badge}
            </div>
            """, unsafe_allow_html=True)

# ── ADD MOVIE ─────────────────────────────────────────────────────────────────
with tab_add:
    st.markdown('<p class="section-label">Register a new movie</p>', unsafe_allow_html=True)

    with st.container():
        name = st.text_input("Movie name", placeholder="e.g. Interstellar", key="add_name")
        seats = st.number_input("Total seats", min_value=1, value=100, step=1, key="add_seats")

        if st.button("Add Movie", key="btn_add"):
            if not name.strip():
                st.error("Please enter a movie name.")
            elif any(m["movie_name"].lower() == name.strip().lower() for m in movies()):
                st.warning(f'"{name.strip()}" is already in the system.')
            else:
                st.session_state.movies.append({
                    "movie_name": name.strip(),
                    "available_seats": int(seats)
                })
                save_data(st.session_state.movies)
                st.success(f'**{name.strip()}** added with {int(seats)} seats.')
                st.rerun()

# ── BOOK TICKETS ──────────────────────────────────────────────────────────────
with tab_book:
    st.markdown('<p class="section-label">Reserve seats for a movie</p>', unsafe_allow_html=True)

    if not movies():
        st.info("No movies available. Add one first.")
    else:
        movie_names = [m["movie_name"] for m in movies()]
        selected = st.selectbox("Choose a movie", movie_names, key="book_select")
        movie_obj = next(m for m in movies() if m["movie_name"] == selected)

        avail = movie_obj["available_seats"]
        st.markdown(f'<p class="section-label">Available seats: <strong style="color:#f5c842">{avail}</strong></p>', unsafe_allow_html=True)

        qty = st.number_input("Seats to book", min_value=1, max_value=max(avail, 1),
                               value=1, step=1, key="book_qty",
                               disabled=(avail == 0))

        if st.button("Confirm Booking", key="btn_book", disabled=(avail == 0)):
            if qty > avail:
                st.error(f"Only {avail} seat(s) available.")
            else:
                movie_obj["available_seats"] -= int(qty)
                save_data(st.session_state.movies)
                st.success(f"✅ {int(qty)} ticket(s) booked for **{selected}**.")
                st.rerun()

        if avail == 0:
            st.error("This show is sold out.")

# ── CANCEL TICKETS ────────────────────────────────────────────────────────────
with tab_cancel:
    st.markdown('<p class="section-label">Release previously booked seats</p>', unsafe_allow_html=True)

    if not movies():
        st.info("No movies in the system.")
    else:
        movie_names = [m["movie_name"] for m in movies()]
        selected_c = st.selectbox("Choose a movie", movie_names, key="cancel_select")
        movie_obj_c = next(m for m in movies() if m["movie_name"] == selected_c)

        qty_c = st.number_input("Seats to cancel", min_value=1, value=1, step=1, key="cancel_qty")

        if st.button("Cancel Tickets", key="btn_cancel"):
            movie_obj_c["available_seats"] += int(qty_c)
            save_data(st.session_state.movies)
            st.success(f"✅ {int(qty_c)} ticket(s) cancelled for **{selected_c}**.")
            st.rerun()