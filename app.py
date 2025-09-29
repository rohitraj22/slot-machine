import streamlit as st
import joblib
import time
import random
from game_logic import play_round, SYMBOLS

# --- State Management (Unchanged) ---
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
    st.metric(label="Your Final Score", value=f"{final_coins} 🪙")
    st.metric(label="Highest Score Achieved", value=f"{state['high_score']} 🪙")

    if state['coins'] <= 0:
        st.error("💔 You've run out of coins. 💔")
    else:
        st.success("✅ You stopped the game. Thanks for playing! ✅")

    if st.button("Start a New Game"):
        new_state = get_initial_state()
        save_state(new_state)
        st.rerun()
else:
    # --- Active Game Interface ---
    st.header(f"Your Balance: {state['coins']} 🪙")
    bet = st.number_input("Place your bet:", min_value=1, max_value=state['coins'], step=1)

    # **THE FIX: Create columns for layout, then put an st.empty() placeholder inside each one.**
    col1, col2, col3 = st.columns(3)
    placeholders = [col1.empty(), col2.empty(), col3.empty()]
    message_placeholder = st.empty()

    # Display the initial state in the placeholders
    last_spin = st.session_state.get('last_spin', ["❓", "❓", "❓"])
    last_message = st.session_state.get('last_message', "Place your bet and click 'Spin'!")
    for i, placeholder in enumerate(placeholders):
        placeholder.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{last_spin[i]}</h1>", unsafe_allow_html=True)
    message_placeholder.info(last_message)

    spin_col, stop_col = st.columns(2)

    if spin_col.button("Spin!", use_container_width=True, type="primary"):
        # --- Physics-Based Animation (Now correctly rendered) ---

        # 1. Determine final result
        new_coins, final_spin, message = play_round(bet, state['coins'])

        # 2. Setup reel strips and indices
        reel_strips = [random.sample(SYMBOLS * 10, len(SYMBOLS * 10)) for _ in range(3)]
        current_indices = [random.randint(0, 9) for _ in range(3)]

        # 3. Define animation parameters
        PHASES = {
            'ACCELERATE': {'duration': 5, 'start_speed': 0.1, 'end_speed': 0.02},
            'BLUR': {'duration': 15, 'speed': 0.01},
            'DECELERATE': {'duration': 5, 'start_speed': 0.02, 'end_speed': 0.1},
            'STOP_PAUSE': 0.3
        }
        
        reel_stop_frames = [
            PHASES['ACCELERATE']['duration'] + PHASES['BLUR']['duration'] + PHASES['DECELERATE']['duration'],
            PHASES['ACCELERATE']['duration'] + PHASES['BLUR']['duration'] * 2 + PHASES['DECELERATE']['duration'],
            PHASES['ACCELERATE']['duration'] + PHASES['BLUR']['duration'] * 3 + PHASES['DECELERATE']['duration']
        ]
        total_frames = max(reel_stop_frames)

        for i in range(1, total_frames + 1):
            spin_display = list(last_spin)
            min_sleep = 0.2

            for r in range(3):
                if i >= reel_stop_frames[r]:
                    spin_display[r] = final_spin[r]
                    continue
                
                accel_duration = PHASES['ACCELERATE']['duration']
                decel_start_frame = reel_stop_frames[r] - PHASES['DECELERATE']['duration']

                if i < accel_duration:
                    progress = i / accel_duration
                    speed = PHASES['ACCELERATE']['start_speed'] - (progress * (0.08))
                    increment = int(1 + progress * 4)
                elif i >= decel_start_frame:
                    progress = (i - decel_start_frame) / PHASES['DECELERATE']['duration']
                    speed = PHASES['DECELERATE']['start_speed'] + (progress * (0.08))
                    increment = int(5 - progress * 4)
                else:
                    speed = PHASES['BLUR']['speed']
                    increment = 5

                current_indices[r] = (current_indices[r] + increment) % len(reel_strips[r])
                spin_display[r] = reel_strips[r][current_indices[r]]
                min_sleep = min(min_sleep, speed)

            # **THE FIX: Update the content of the st.empty() placeholders, which replaces the old content.**
            for j, placeholder in enumerate(placeholders):
                placeholder.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{spin_display[j]}</h1>", unsafe_allow_html=True)
            
            if i in reel_stop_frames:
                time.sleep(PHASES['STOP_PAUSE'])
            else:
                time.sleep(min_sleep)

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
