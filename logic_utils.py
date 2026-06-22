import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty.

    Harder difficulties use a wider range so the secret is harder to guess.
    Ranges grow monotonically: Easy < Normal < Hard.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def new_secret(difficulty: str) -> int:
    """Return a fresh secret number within the range for the given difficulty."""
    low, high = get_range_for_difficulty(difficulty)
    return random.randint(low, high)


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess and validate it against the
    inclusive [low, high] range for the current difficulty.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    # The UI tells the player to guess within [low, high], so reject anything
    # outside that range instead of silently accepting an impossible guess.
    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    The hint points the user toward the secret: if the guess is too high,
    they should go lower; if it is too low, they should go higher.

    outcome examples: "Win", "Too High", "Too Low"
    """
    # Coerce to int so comparisons stay numeric even if values arrive as strings.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Too high — go LOWER!"

    return "Too Low", "📈 Too low — go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update score based on outcome and the (1-based) attempt number.

    A win is worth more the sooner it happens: a first-attempt win earns the
    full 100 points, dropping 10 per extra attempt, with a floor of 10. Any
    wrong guess costs 5 points, regardless of direction.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
