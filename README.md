# LangChain + Gemini Student Agent

A complete implementation of the supplied assignment. The project creates a SQLite database (`students.db`), defines the four required LangChain tools with `@tool`, and gives those tools to a Gemini-powered LangChain agent. The user asks a normal-language question; the LLM decides which tools to call and whether additional tool calls are needed.

## Features

- SQLite `students` table with all five required records.
- `get_student_info(student_id)` tool.
- `get_student_marks(student_id)` tool.
- Safe `calculator(expression)` tool for totals and averages.
- `get_passing_rules()` tool.
- Gemini agent created using LangChain's current `create_agent` interface.
- No fixed/manual tool-call pipeline.
- Compound-question support, including the challenge question.
- `--trace` mode to visibly demonstrate which tools the agent selected.
- Automated tests for the database and all four tools.

## Requirements

- Python 3.10+
- A Gemini API key

## Setup

### 1. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and replace the placeholder with your Gemini API key:

```env
GOOGLE_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
```

`GEMINI_API_KEY` is also accepted if you prefer that environment-variable name.

### 4. Initialize the database

A ready-to-use `students.db` is already included, but you can recreate/update it at any time:

```bash
python init_db.py
```

### 5. Run the agent

Interactive mode:

```bash
python app.py
```

Ask one question directly:

```bash
python app.py "What is the total and average mark of 22CS045?"
```

Show which tools the LLM selected:

```bash
python app.py --trace "Is 22CS045 eligible to pass according to the university rules?"
```

Run all assignment examples:

```bash
python app.py --examples --trace
```

## Challenge question

```bash
python app.py --trace "I am 22CS045. Tell me my name, department, total marks, average marks, and whether I satisfy the university passing requirements."
```

For that question, the agent has access to all four tools and is instructed to continue calling tools until it has enough information to answer every requested part. The order is not hard-coded in Python.

## Expected challenge-question facts

These are useful for checking the answer produced by the agent:

- Name: Dhanushya
- Department: Computer Science
- Marks: Python 85, Database 72, AI 90, Web 78
- Total: 325
- Average: 81.25%
- Passing rules: average at least 40% and every subject at least 35
- Result: satisfies the stated passing requirements

## Project structure

```text
sjit_langchain_student_agent/
├── app.py                  # CLI / interactive entry point
├── agent.py                # Gemini model + LangChain agent
├── tools.py                # Four required @tool functions
├── database.py             # SQLite setup and data access
├── init_db.py              # Database initialization helper
├── students.db             # Ready-to-use SQLite DB
├── requirements.txt
├── .env.example
├── .gitignore
├── problem_statement.txt   # Original supplied assignment
└── tests/
    ├── test_database.py
    └── test_tools.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

The tests do not call Gemini, so they do not consume API quota. They validate the database records and the behavior of all four tools.

## Why this is an agent, not a fixed chain

The program does **not** contain code such as:

```python
marks = get_student_marks(...)
rules = get_passing_rules(...)
average = calculator(...)
```

inside the question-answering flow. Instead, it registers the tools with `create_agent(...)`. Gemini receives the user's question and tool descriptions, selects a tool, observes the returned result, and can select another tool if needed before producing the final answer.

## Notes

- The calculator uses a small AST-based arithmetic evaluator rather than Python `eval`, so arbitrary Python code cannot be executed through the calculator tool.
- Database lookup normalizes student IDs to uppercase.
- Tool outputs use JSON strings to make the observations easy for the LLM to interpret consistently.
