# BlindSpot AI

A beginner-friendly mini project that creates practice questions from study material using the OpenAI API. If the API is unavailable or out of credits, it switches to a clearly labelled prepared demo quiz.

## Features
- Paste academic text
- Generate five MCQs using OpenAI API when available
- Demo fallback when API calls fail or credits run out
- Answer scoring, explanations, and weak-topic feedback
- Responsive layout
- Opens the browser automatically when started

## Run on Windows in VS Code

1. Open this folder in VS Code.
2. Open Terminal → New Terminal.
3. Activate your environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
4. Install dependencies if needed:
   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Set your API key for this terminal if not already configured:
   ```powershell
   $env:OPENAI_API_KEY="your_api_key_here"
   ```
6. Start the app:
   ```powershell
   python app.py
   ```
7. Your browser should open at `http://127.0.0.1:5000`.

## Important demo behavior
If the OpenAI API returns an error (for example, no API credits), the app shows a prepared sample quiz about distributed databases. The page clearly labels this as demo mode. The fallback questions are not generated from the user's pasted text and do not require API credits.

## Security
Never commit an API key to GitHub. Keep it in an environment variable and do not share screenshots containing the key.

## Project flow
1. Student pastes notes.
2. Flask sends notes to the OpenAI API.
3. If the API succeeds, generated questions are shown.
4. If the API fails, the prepared demo quiz is shown.
5. JavaScript calculates the score and lists topics to revise.
