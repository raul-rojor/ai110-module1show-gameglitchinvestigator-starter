# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
The game seemed to contradict itself in the information it was presenting to me as a player. For example, the instructions tell me to guess a number between 1-100, yet even after guessing 100, the game hinted me to submit a higher number. I then submitted 101, and I was told to go lower. However, I instead submited 105 and was hinted to guess higher.
During my initial plays of the game, I noticed that the player may be hinted to guess higher after they just guessed a number exceeding the possible answer limit of 100 and that the hints I was given pushed me in the opposite direction from the answer (even when my previous guess was inside 1-100).

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Guess<num| Hint 'higher'   |Hints 'Go LOWER!'|        None            |
|Guess>num| Hint 'lower'    |Hints 'Go HIGHER!'|       None            |
|Guess -10| Asked to guess >1 | Hints 'Go LOWER!' |    None            |
|Guess 9999| Asked to guess <101 | Hints 'Go HIGHER!'| None            |
|First guess|'Attempts left' -= 1|'Attempts left' unchanged|  None     |
|'New Game' after losing/winning|Restarts game|Disallows guesses| None |
|Easy/Hard modes|Makes game respectively difficult|Game ignores mode description on the left|None|
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude Code to help me fix bugs in this project.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I asked Claude to refactor the parse_guess method, pointing out how it currently allows for guesses outside of the intended range, asking it to verify if my analysis is correct, and telling it to check if other parts of the method or calls to it need fixing. The AI agreed with my thoughts. It suggested adding low and high parameters to the function and checking that the guess is within that range using conditionals. It also suggested increasing the attempts count only after a valid guess had been entered. Within the same answer, the AI model also provided tests for the changes in the test_game_logic.py file. This inclusion surprised me since I didn't prompt it to do so yet and I had closed previous conversations where I had asked for tests for previous bugs. The tests passed and the app reflected the correctness of the suggestions made once I launched and played it.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
Although I didn't have an experience where Claude Code gave me an incorrect or directly misleading suggestion during refactoring, it did give me an incomplete fix my first time prompting it. I asked the agent to refactor the get_range_for_difficulty method so that the low and high values in the range for the secret int match the difficulty level. The AI indeed suggested a refactored of the method in logic_utils.py and imported it in app.py, but it didn't make it so that "the low and high values in the range for the secret int match the difficulty level." The failure in completely fixing the logic came from me asking the AI to fix this logic only in this particular method and not to find related code lines that fail to call the method (or it's outputs from previous calls). I tested result by asking the AI for and verifying a pytest which was correct. I then tested the game itself and realized that the refactoring only changed the left sidebar text, not the game logic. From this experience, I learned to be more lengthy and detailed in my refactoring prompts so that the AI takes a more wholistic approach in it's fixing of fauly logic that I point out.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
After I checked and accepted an AI 'fix' to an existing bug, I asked it to create the necessary pytests to ensure the change works as intended. I then looked through the pytest(s) to make sure the edge cases I can think of are covered and made sure they all passed. After this step, I ran the game with special attention to the previously bugged feature to make sure it now ran properly.
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
After changing the parse_guess method, I had Claude Code make me pytests to ensure edge cases for all possible guess inputs are covered. The tests accounted for integer guesses correctly within secret's boundary, integer guesses on the limit of the range (which are valid since the range is inclusive), an empty string/None guess, guesses with letters, float guesses, integer guesses below the lower limit of the range, and integer guesses above the upper limit of the range. All of the input guesses mentioned above are string objects in the tests to reflect the actual process in the application, but they were mentioned above as different object types to easily explain them (they are attempted to be made ints within the parse_guess function). The passing of all of these tests showed me that my code can correctly handle all potential guess input cases.
- Did AI help you design or understand any tests? How?
AI helped me design all of my tests by suggesting them to me after I prompted it to create pytests that account for all possible edge cases related to the change made. I then read slowly through each test which allowed me to understand the tests without AI assistance and verify the tests' design myself.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit "reruns" and session state work hand-in-hand. Any interaction a user makes with a Streamlit app causes Streamlit to rerun the entire app script from top to bottom. However, the app likely needs to remember certain values across reruns, through the user's whole experience. Session state is how Streamlit keeps memory of values to ensure data is kept regardless of reruns. Session state therefore holds a dictionary keeping values for app functions necessitating memory.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
In future projects, I want to make sure I create tests for debugging that I do. Before I prompt an AI coding assistant to help me create these tests, I will write out every possible edge case I can imagine that interacts with the code I changed. I will then ask the AI to make the tests and verify that there are no potential edge cases unaccounted for in the tests.
- What is one thing you would do differently next time you work with AI on a coding task?
When working with AI on my next coding task, I will ask my AI assistant prompts that include not only details about the narrow task I am giving it (like checking code in a specific part of a script), but also details about how that narrow task connects to my broader goals and I'll give it instructions to incorporate these broader understandings into it's plan to complete the narrow task. This is because I realized that when I employ this prompting strategy, the AI often highlights how code I wasn't focused on is interconnected to the code I was focused on, and how changes in the latter could affect the former.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
Before this project I tended to view AI assistance with coding as a force greater than me that I could only direct. Now I see myself having a more active part of the coding process as I immerse myself in and direct the code architecture while letting AI generated code handle the time-intensive details.
