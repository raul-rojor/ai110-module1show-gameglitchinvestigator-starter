# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
The purpose of the game is for the user to attempt to guess a random secret integer in a certain range of numbers before their attempts limit is reached. The size of the domain the secret number may be in and the number of attempts the user gets to guess the number are determined by the difficulty mode the user chooses -- easy, normal, or hard. If the player selects the "show hints" option, the game tells the player that their previous guess was too high or too low relative to the secret number. If the user correctly guesses the secret number by submitting the number, then they win, but if the user runs out of attempts before then, they lose.
- [ ] Detail which bugs you found.
An initial multitude of bugs became clear after playing the game various times and taking a look at the code. The first obvious bug was the the hint directions were opposite of what they should be; high guesses were told to go higher and low guesses were told to go lower. Another problem was that the secret number was always between 1 and 100, inclusive, regardless of difficulty and attempts didn't decrease as difficulty increased. Also, users were allowed to input any integer, even outside of the range that the secret number could be in. The scoring was also incorrect since guessing too high would add points instead of subtracting and winning scores counted an extra attempt in their calculation. Additionally, attempts were counted before the guess was parsed, so invalid guess attempts would count as guesses as long as the submit button was clicked. Another issue was that if a game was lost or won (i.e., the game was completed), a new game could not be played, even if the difficulty was changed. Finally, in the code it could be seen that on even attempts the secret number was stringified before it was compared to guesses which sometimes led to string comparisons.
- [ ] Explain what fixes you applied.
Naturally, the fixes applied addressed the bugs listed above. These fixes included having "too high" guesses now output "go LOWER" and "too low" guesses now output "go HIGHER" in the check_guess method, dropping the lines which made even-attempt guesses and the secret into strings before comparing, generating random secret numbers based on the difficulty selected instead of a forced 1-100 range, changing the potential ranges for secret to increase as difficulty increases, adding low/high secret boundaries to parse_guess so that out of range guesses are rejected, fixed the score calculation for winning games and the incorrect points increase for high guesses, counting only valid guesses (only after guess passes parse_guess), decreasing attempts as difficulty increases, resetting the whole state of the game when "new game" is selected or when difficulty is changed, making the attempts counter update accurately, and ensuring the range the game tells the user to guess within matches the difficulty selected.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User selects "normal" difficulty mode
2. Game instructs user to "guess a number between 1 and 100" where "attempts left: 6"
3. User types "63" and clicks the "submit guess" button
4. Game outputs "too high — go LOWER!" since the "show hint" option had been selected by default and "attempts left:" counter drops to "5"
5. User deletes "63" and types "30" before clicking the "submit guess" button
6. Game outputs "too high — go LOWER!" and "attempts left:" counter drops to "4"
7. User deletes "30" and types "20" before clicking the "submit guess" button
8. Game outputs "too low — go HIGHER!" and "attempts left:" counter drops to "3"
9. User deletes "20" and types "27" before clicking the "submit guess" button
10. Game outputs "too low — go HIGHER!" and "attempts left:" counter drops to "2"
11. User deselects the "show hint" option and the "too low — go HIGHER!" text disappears
12. User deletes "27" and types "28" before clicking the "submit guess" button
13. "Attempts left:" counter drops to "1"
14. User deletes "27" and types "29" before clicking the "submit guess" button
15. Balloons cover the screen as they fly up from the bottom to the top of the page, "attempts left:" counter drops to 0, and game outputs "you won! The secret was 29. Final score: 25"

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
...........................                                                                                                                         [100%]
27 passed in 0.02s
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
