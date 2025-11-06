LEARNING PATH (AI Assisted Development)

This project is your training ground. The goal is not to rush. The goal is to learn programming, testing, version control, software design, and good habits at a steady pace.

This document gives you a repeatable workflow and the prompts you will use with Codex or Copilot inside VS Code.

1. Environment Setup (Once)
Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip

Install core tools
pip install typer rich pytest pytest-cov black isort flake8 mypy bandit

Project layout to aim for (you will grow into this)
src/stoic_journal/
  __init__.py
  __main__.py
  app.py
  storage.py
  models.py
  commands/
tests/

2. Daily Development Loop

Repeat this every time you work:

Pick one small feature.

Use the Teach Me prompt to understand the concept first.

Write code in small steps.

Run checks:

black src tests; isort src tests
flake8 src tests
mypy src
bandit -q -r src
pytest -q --cov=src --cov-report=term-missing


If something fails, use the Debug prompt and paste the output.

When code is working, ask for a Code Review and apply improvements.

Commit when clean.

This is how professionals work.
Small steps, constant feedback.

3. Prompts to Use While Learning
Teach Me a Concept
Teach me like a new junior developer.
Topic: <example: SQLite connection, CLI arguments, file paths>
Explain what it is, why it matters, and show a tiny working example.
Give me a short exercise and tell me how to know if I did it correctly.

Build a Small Feature
Act as my mentor. I am adding a small feature to my journaling CLI.
My level is beginner. Go slowly.
1. Tell me which files to change.
2. Give code in small pieces and say exactly where to paste it.
3. Explain each piece in simple language.
4. Tell me the command to run and what output to expect.
5. If errors appear I will paste them for step-by-step debugging.

Debug Step by Step
Here is the error and code.
Help me debug step-by-step:
- Suggest the most likely cause
- Give me one single change to try
- Tell me the command to run
- Tell me what output to look for
If the fix does not work, propose the next step.

Code Review
Review this code like a senior developer teaching a junior.
Comment on correctness, clarity, naming, and structure.
Suggest small improvements and explain why they matter.

Security and Privacy Check
Security pass for a local journal:
Check for secrets in code, unsafe file handling, injection risk, and logging of private content.
Suggest the smallest safe fixes and show exactly what to change.

4. Learning Roadmap

Take these one at a time.

Add entry and list entries

Use a platform appropriate data directory for the SQLite file

Add a schema version table and a simple migration path

Add tags and search

Add edit and delete functionality

Add export to JSON or Markdown

Add logging that avoids leaking journal text

Package so you can run python -m stoic_journal

Later: build a tiny read-only web viewer using FastAPI

Each step uses the same loop: learn, build small, test, review, commit.

5. Glossary in Plain Language

Virtual environment: A private copy of Python for this project only.

Package: A folder containing Python code with __init__.py.

Module: A single Python file like storage.py.

CLI: A program you run using the terminal.

Type hint: A small label that helps tools catch mistakes early.

Linter: A tool that points out style or logic mistakes.

Unit test: A small automated check that proves one thing works.

SQLite: A tiny database stored in a single local file.

6. Useful Commands

Activate environment:

.\.venv\Scripts\Activate.ps1


Run the CLI:

python -m stoic_journal list


Run checks:

black src tests; isort src tests
flake8 src tests
mypy src
bandit -q -r src
pytest -q

7. When You Feel Stuck

Use this:

I am stuck. Here is the code and the error.
Help me continue one small step at a time.
Guide me slowly.


You are learning how to think like a developer. That is the real skill.
Take your time. Work in small steps. Ask questions. Commit when clean.

You are doing this correctly.

Now save, then commit:
git add LEARNING_PATH.md
git commit -m "docs: add clean learning path"