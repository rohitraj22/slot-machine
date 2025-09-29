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
st.title("🎰 Realistic Slot Machine 🎰")

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
    # --- Active Game Interface ---
    st.header(f"Your Balance: {state['coins']}")
    bet = st.number_input("Place your bet:", min_value=1, max_value=state['coins'], step=1)

    reel_placeholders = st.columns(3)
    message_placeholder = st.empty()

    last_spin = st.session_state.get('last_spin', ["❓", "❓", "❓"])
    last_message = st.session_state.get('last_message', "Place your bet and click 'Spin'!")

    for i, reel in enumerate(reel_placeholders):
        reel.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{last_spin[i]}</h1>", unsafe_allow_html=True)
    message_placeholder.info(last_message)

    spin_col, stop_col = st.columns(2)

    if spin_col.button("Spin!", use_container_width=True, type="primary"):
       
        new_coins, final_spin, message = play_round(bet, state['coins'])

        reel_strips = [random.sample(SYMBOLS * 10, len(SYMBOLS * 10)) for _ in range(3)]

        BLUR_SPEED = 0.02   # Time between frames during blur
        SLOWDOWN_SPEED = 0.1 # Time between frames during slowdown
        REEL_STOP_PAUSE = 0.3 # Pause after a reel stops
        
        TOTAL_DURATION = 50 # Total animation frames
        REEL_1_SLOWDOWN = 15 # Frame when reel 1 starts to slow down
        REEL_1_STOP = 20     # Frame when reel 1 stops
        REEL_2_SLOWDOWN = 30
        REEL_2_STOP = 35
        REEL_3_SLOWDOWN = 45
        REEL_3_STOP = 50
        
        start_indices = [random.randint(0, len(s) - 1) for s in reel_strips]
        
        for i in range(1, TOTAL_DURATION + 1):
            spin_display = ["", "", ""]
            current_sleep_time = BLUR_SPEED

            if i < REEL_1_STOP:
                idx = (start_indices[0] + i) % len(reel_strips[0])
                spin_display[0] = reel_strips[0][idx]
                if i > REEL_1_SLOWDOWN:
                    current_sleep_time = SLOWDOWN_SPEED # Slow down
            else:
                spin_display[0] = final_spin[0]

            if i < REEL_2_STOP:
                idx = (start_indices[1] + i * 2) % len(reel_strips[1]) # Spin faster
                spin_display[1] = reel_strips[1][idx]
                if i > REEL_2_SLOWDOWN:
                    current_sleep_time = SLOWDOWN_SPEED
            else:
                spin_display[1] = final_spin[1]

            if i < REEL_3_STOP:
                idx = (start_indices[2] + i * 3) % len(reel_strips[2]) # Spin fastest
                spin_display[2] = reel_strips[2][idx]
                if i > REEL_3_SLOWDOWN:
                    current_sleep_time = SLOWDOWN_SPEED
            else:
                spin_display[2] = final_spin[2]

            # Update UI
            for j, reel in enumerate(reel_placeholders):
                reel.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{spin_display[j]}</h1>", unsafe_allow_html=True)

            # Pause when a reel stops to create impact
            if i == REEL_1_STOP or i == REEL_2_STOP:
                time.sleep(REEL_STOP_PAUSE)
            else:
                time.sleep(current_sleep_time)

        # Finalize state
        st.session_state.last_message = message
        st.session_state.last_spin = final_spin
        state['coins'] = new_coins
        state['high_score'] = max(state['high_score'], new_coins)
        save_state(state)
        st.rerun()

    if stop_col.button("Stop Playing", use_container_width=True):
        state['game_over'] = True
        save_state(state)
        st.rerun()
