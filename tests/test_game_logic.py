import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    new_secret,
    parse_guess,
    update_score,
)


# --- get_range_for_difficulty: difficulty range logic ---

def test_easy_range():
    # Easy uses the narrowest range
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_hard_range():
    # Hard uses the widest range (harder to guess)
    assert get_range_for_difficulty("Hard") == (1, 200)


def test_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Impossible") == (1, 100)


def test_range_widens_with_difficulty():
    # The range size must grow monotonically: Easy < Normal < Hard
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")

    easy_size = easy_high - easy_low
    normal_size = normal_high - normal_low
    hard_size = hard_high - hard_low

    assert easy_size < normal_size < hard_size


# --- new_secret: secret generation tracks the selected difficulty ---

@pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard", "Impossible"])
def test_new_secret_within_range(difficulty):
    # A generated secret must always fall inside the difficulty's range.
    # Run many times since the value is random.
    low, high = get_range_for_difficulty(difficulty)
    for _ in range(1000):
        secret = new_secret(difficulty)
        assert isinstance(secret, int)
        assert low <= secret <= high


def test_new_secret_respects_difficulty_bounds():
    # Hard's wider range should be able to produce values above Easy's max,
    # confirming the secret tracks the selected difficulty (the bug we fixed).
    hard_secrets = {new_secret("Hard") for _ in range(2000)}
    _, easy_high = get_range_for_difficulty("Easy")
    assert any(secret > easy_high for secret in hard_secrets)


# --- check_guess: outcome and hint direction ---
# check_guess returns an (outcome, message) tuple.

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_hint_points_in_correct_direction():
    # The bug we fixed: hints were reversed. A guess that is too high must tell
    # the user to go LOWER, and a guess that is too low must tell them to go HIGHER.
    _, high_message = check_guess(60, 50)
    assert "LOWER" in high_message.upper()
    assert "HIGHER" not in high_message.upper()

    _, low_message = check_guess(40, 50)
    assert "HIGHER" in low_message.upper()
    assert "LOWER" not in low_message.upper()


# --- parse_guess: input parsing and difficulty-range validation ---
# parse_guess returns an (ok, guess_int, error_message) tuple.

def test_parse_valid_guess_within_range():
    ok, value, err = parse_guess("42", 1, 100)
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_accepts_range_boundaries():
    ok_low, low_val, _ = parse_guess("1", 1, 100)
    ok_high, high_val, _ = parse_guess("100", 1, 100)
    assert (ok_low, low_val) == (True, 1)
    assert (ok_high, high_val) == (True, 100)


def test_parse_empty_or_none_prompts_for_a_guess():
    for raw in ("", None):
        ok, value, err = parse_guess(raw, 1, 100)
        assert ok is False
        assert value is None
        assert err == "Enter a guess."


def test_parse_non_number_is_rejected():
    ok, value, err = parse_guess("abc", 1, 100)
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_truncates_decimal_input():
    ok, value, _ = parse_guess("5.9", 1, 100)
    assert ok is True
    assert value == 5


def test_parse_rejects_guess_below_range():
    ok, value, err = parse_guess("0", 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in err


def test_parse_rejects_guess_above_range():
    ok, value, err = parse_guess("250", 1, 200)
    assert ok is False
    assert value is None
    assert "between 1 and 200" in err


# --- update_score: win reward and wrong-guess penalty ---

def test_first_attempt_win_earns_full_points():
    # Winning on the first attempt earns the full 100 points.
    assert update_score(0, "Win", 1) == 100


def test_win_loses_ten_points_per_extra_attempt():
    # Each attempt beyond the first costs 10 points off the win reward.
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 5) == 60


def test_win_points_floor_at_ten():
    # A very late win still awards at least 10 points (never zero/negative).
    assert update_score(0, "Win", 20) == 10


def test_too_high_always_penalizes_regardless_of_parity():
    # The bug we fixed: "Too High" used to ADD points on even attempts.
    # A wrong guess must cost 5 points whether the attempt is odd or even.
    assert update_score(50, "Too High", 1) == 45
    assert update_score(50, "Too High", 2) == 45


def test_too_low_penalizes():
    assert update_score(50, "Too Low", 3) == 45


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(42, "Pending", 1) == 42
