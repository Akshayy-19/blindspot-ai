import os
import json
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()  # Reads OPENAI_API_KEY from your environment


# Prepared fallback questions so the project can be demonstrated without API credits.
# These are sample questions, not newly AI-generated questions.
DEMO_QUESTIONS = [
    {
        "topic": "Distributed databases",
        "question": "What is a distributed database?",
        "options": [
            "A collection of logically related data stored at multiple network-connected sites",
            "A database stored only in a spreadsheet",
            "A database that cannot be accessed over a network",
            "A collection of unrelated files on one computer"
        ],
        "answer": 0,
        "explanation": "A distributed database stores logically related data at multiple connected sites while appearing as one database to users."
    },
    {
        "topic": "Query processing",
        "question": "What is the main goal of distributed query processing?",
        "options": [
            "To delete duplicate tables",
            "To find an efficient execution plan for a query across different sites",
            "To prevent users from retrieving data",
            "To convert every query into an image"
        ],
        "answer": 1,
        "explanation": "Distributed query processing aims to execute a query efficiently when data is stored at different sites."
    },
    {
        "topic": "Data localization",
        "question": "What does data localization help determine in a distributed database?",
        "options": [
            "The font used in a report",
            "The user's password",
            "Which site or sites store the required data",
            "The color of the database interface"
        ],
        "answer": 2,
        "explanation": "Data localization identifies the sites where the data needed by a query is stored."
    },
    {
        "topic": "Distributed database benefits",
        "question": "Which is a potential benefit of a distributed database?",
        "options": [
            "It always removes the need for a network",
            "It makes all data storage impossible",
            "It prevents all database failures",
            "It can provide access to data stored at different locations"
        ],
        "answer": 3,
        "explanation": "A distributed database lets users access logically related data held across multiple network-connected sites."
    },
    {
        "topic": "Execution plans",
        "question": "Why does a query processor choose an efficient execution plan?",
        "options": [
            "To reduce unnecessary work and retrieve the requested result efficiently",
            "To change the meaning of the query",
            "To remove all database tables",
            "To avoid returning any results"
        ],
        "answer": 0,
        "explanation": "An efficient execution plan helps retrieve the requested result while reducing unnecessary processing and data transfer."
    }
]


@app.route("/", methods=["GET", "POST"])
def home():
    questions = []
    notes = ""
    error = ""
    demo_mode = False

    if request.method == "POST":
        notes = request.form.get("notes", "").strip()

        if len(notes) < 50:
            error = "Please paste at least a few sentences of study material."
        else:
            try:
                response = client.responses.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                    input=[
                        {
                            "role": "system",
                            "content": (
                                "Create exactly 5 multiple-choice study questions using only "
                                "the supplied study material. Return ONLY valid JSON in this shape: "
                                '{"questions":[{"topic":"short topic","question":"...","options":["A...","B...","C...","D..."],"answer":0,"explanation":"short explanation"}]}. '
                                "The answer field must be an integer from 0 to 3. Keep questions clear."
                            ),
                        },
                        {"role": "user", "content": notes},
                    ],
                )
                data = json.loads(response.output_text)
                questions = data["questions"]
                if len(questions) != 5:
                    raise ValueError("The AI did not return five questions.")
            except Exception:
                # Keep the app usable for demos if the API is unavailable or out of credits.
                questions = DEMO_QUESTIONS
                demo_mode = True

    return render_template(
        "index.html",
        questions=questions,
        notes=notes,
        error=error,
        demo_mode=demo_mode,
    )


if __name__ == "__main__":
    import webbrowser
    from threading import Timer

    Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True, use_reloader=False)
