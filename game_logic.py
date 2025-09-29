import random
SYMBOLS = ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍀"]
def play_round(bet, current_coins):
    if bet <= 0:
        return current_coins, ["❓", "❓", "❓"], "Bet must be greater than 0."
    if bet > current_coins:
        return current_coins, ["❓", "❓", "❓"], "You don't have enough coins."
        
    current_coins -= bet
    
    spin = random.choices(SYMBOLS, k=3)

    if spin[0] == spin[1] == spin[2]:
        winnings = bet * 10
        current_coins += winnings
        message = f"🎉 JACKPOT! You won {winnings} coins! 🎉"
    elif spin[0] == spin[1] or spin[0] == spin[2] or spin[1] == spin[2]:
        winnings = bet * 2
        current_coins += winnings
        message = f"✨ Two symbols match! You won {winnings} coins! ✨"
    else:
        message = "🙁 No match. Better luck next time!"
        
    return current_coins, spin, message
