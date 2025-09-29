# app.py
import streamlit as st
import joblib
from game_logic import play_round  # Import our refactored game logic

# --- State Management with Joblib ---
COIN_FILE = 'player_coins.joblib'

def load_coins():
    """Load coins from file, or return 100 if file doesn't exist."""
    try:
        return joblib.load(COIN_FILE)
    except FileNotFoundError:
        return 100

def save_coins(coins):
    """Save coins to a file."""
    joblib.dump(coins, COIN_FILE)

# --- UI Layout ---
st.title("🎰 Slot Machine 🎰")

# Load the current number of coins at the start of every script run
coins = load_coins()

# Display last spin result (if it exists)
if 'last_spin' not in st.session_state:
    st.session_state.last_spin = ["❓", "❓", "❓"]
if 'message' not in st.session_state:
    st.session_state.message = "Place your bet to start!"

# --- Main Game Interface ---
if coins > 0:
    st.header(f"Your Balance: {coins} 🪙")
    
    bet = st.number_input("Place your bet:", min_value=1, max_value=coins, step=1)

    if st.button("Spin!"):
        # Call the logic function
        new_coins, spin_result, message = play_round(bet, coins)
        
        # Save the new state
        save_coins(new_coins)
        
        # Store results for display and rerun the script to show changes
        st.session_state.last_spin = spin_result
        st.session_state.message = message
        st.rerun()

else:
    # Game Over screen
    st.error("💔 Game Over! You've run out of coins. 💔")
    if st.button("Start New Game"):
        save_coins(100) # Reset coins to 100
        st.rerun()

# Display the reels and message
col1, col2, col3 = st.columns(3)
col1.markdown(f"<h1 style='text-align: center;'>{st.session_state.last_spin[0]}</h1>", unsafe_allow_html=True)
col2.markdown(f"<h1 style='text-align: center;'>{st.session_state.last_spin[1]}</h1>", unsafe_allow_html=True)
col3.markdown(f"<h1 style='text-align: center;'>{st.session_state.last_spin[2]}</h1>", unsafe_allow_html=True)

st.info(st.session_state.message)
