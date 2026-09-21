from __future__ import annotations

import argparse

from agent import ask_agent
from database import initialize_database

EXAMPLES = [
    "What is the name and department of student 22CS045?",
    "What are the marks of 22CS047?",
    "What is the total and average mark of 22CS045?",
    "Is 22CS045 eligible to pass according to the university rules?",
    "I am 22CS045. Tell me my name, department, total marks, average marks, and whether I satisfy the university passing requirements.",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="LangChain + Gemini Student Agent")
    parser.add_argument("question", nargs="*", help="Question to ask the agent")
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Show the tool calls selected by the agent",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Run all assignment example questions",
    )
    args = parser.parse_args()

    initialize_database()

    if args.examples:
        for index, question in enumerate(EXAMPLES, start=1):
            print(f"\n[{index}] Q: {question}")
            print("A:", ask_agent(question, show_trace=args.trace))
        return

    if args.question:
        question = " ".join(args.question)
        print(ask_agent(question, show_trace=args.trace))
        return

    print("LangChain Student Agent (type 'exit' to quit)")
    print("Tip: add --trace when launching to see which tools Gemini selects.\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        try:
            print("Agent:", ask_agent(question, show_trace=args.trace))
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
