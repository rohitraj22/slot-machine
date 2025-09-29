import streamlit as st
import joblib
import time
import random
from game_logic import play_round, SYMBOLS

STATE_FILE = 'game_state.joblib'

def get_initial_state():
    return {'coins': 100, 'high_score': 100, 'game_over': False}

def load_state():
    try:
        return joblib.load(STATE_FILE)
    except FileNotFoundError:
        return get_initial_state()

def save_state(state):
    joblib.dump(state, STATE_FILE)

# --- UI Layout ---
st.set_page_config(page_title="Spinning Slots", page_icon="🎰")
st.title("🎰 Slot Machine 🎰")

# Load game state
state = load_state()

# --- Main Game Logic ---

if state.get('game_over', False) or state['coins'] <= 0:
    # --- Game Over Screen ---
    st.header("Game Over!")
    final_coins = 0 if state['coins'] < 0 else state['coins']
    st.metric(label="Your Final Score", value=f"{final_coins}")
    st.metric(label="Highest Score Achieved", value=f"{state['high_score']}")

    if state['coins'] <= 0:
        st.error("You've run out of coins!")
    else:
        st.success("You stopped the game. Thanks for playing!")

    if st.button("Start a New Game"):
        new_state = get_initial_state()
        save_state(new_state)
        st.rerun()
else:
    # --- Active Game Interface (Corrected Logic) ---
    st.header(f"Your Balance: {state['coins']} 🪙")

    bet = st.number_input("Place your bet:", min_value=1, max_value=state['coins'], step=1)

    reel_placeholders = st.columns(3)
    message_placeholder = st.empty()

    # Get the last known spin and message from the session state
    last_spin = st.session_state.get('last_spin', ["❓", "❓", "❓"])
    last_message = st.session_state.get('last_message', "Place your bet and click 'Spin'!")

    # Display the last known state
    for i, reel in enumerate(reel_placeholders):
        reel.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{last_spin[i]}</h1>", unsafe_allow_html=True)
    message_placeholder.info(last_message)

    # Buttons
    spin_col, stop_col = st.columns(2)

    if spin_col.button("Spin!", use_container_width=True, type="primary"):
        new_coins, final_spin, message = play_round(bet, state['coins'])

        # --- The Animation ---
        ANIMATION_FRAMES = 20
        SLEEP_TIME = 0.05
        for i in range(ANIMATION_FRAMES + 1):
            spin_display = list(final_spin)
            if i < ANIMATION_FRAMES * 0.5:
                spin_display[0] = random.choice(SYMBOLS)
            if i < ANIMATION_FRAMES * 0.75:
                spin_display[1] = random.choice(SYMBOLS)
            if i < ANIMATION_FRAMES:
                spin_display[2] = random.choice(SYMBOLS)

            for j, reel in enumerate(reel_placeholders):
                reel.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{spin_display[j]}</h1>", unsafe_allow_html=True)
            
            if i < ANIMATION_FRAMES:
                time.sleep(SLEEP_TIME)

        st.session_state.last_message = message
        st.session_state.last_spin = final_spin

        # Update and save the overall game state
        state['coins'] = new_coins
        state['high_score'] = max(state['high_score'], new_coins)
        save_state(state)
        
        # Rerun to update the balance and message display
        st.rerun()

    if stop_col.button("Stop Playing", use_container_width=True):
        state['game_over'] = True
        save_state(state)
        st.rerun()
