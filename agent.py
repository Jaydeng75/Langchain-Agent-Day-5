from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import TOOLS

load_dotenv()

SYSTEM_PROMPT = """You are a student-information assistant connected to a SQLite-backed tool set.

Rules:
1. Use the registered tools whenever a question depends on student data, marks, arithmetic, or university passing rules.
2. Never invent student details or marks.
3. If the user asks for a student's name or department, use get_student_info.
4. If the user asks for marks, total, average, or pass eligibility, use get_student_marks.
5. If the user asks for a total or average, you MUST use calculator for the arithmetic instead of doing the arithmetic yourself.
6. If the user asks whether a student satisfies the university passing requirements, you MUST use get_student_marks, get_passing_rules, and calculator. A student satisfies the rules only if the overall average is at least the required minimum AND every subject mark is at least the per-subject minimum.
7. For a compound question, keep selecting tools until every requested part can be answered. Do not follow a fixed tool sequence; choose only the tools needed for the user's actual question.
8. If a student ID is not found, say so clearly and do not fabricate an answer.
9. Keep final answers concise and include the student ID when useful.
"""


def build_agent():
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing Gemini API key. Set GOOGLE_API_KEY (recommended) or GEMINI_API_KEY in your environment or .env file."
        )

    model = ChatGoogleGenerativeAI(
        model=model_name,
        api_key=api_key,
        temperature=0,
    )
    return create_agent(model=model, tools=TOOLS, system_prompt=SYSTEM_PROMPT)


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if block.get("type") == "text" and "text" in block:
                    parts.append(str(block["text"]))
                elif "text" in block:
                    parts.append(str(block["text"]))
        return "\n".join(part for part in parts if part)
    return str(content)


def ask_agent(question: str, show_trace: bool = False) -> str:
    agent = build_agent()
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )

    messages = result.get("messages", [])
    if show_trace:
        print("\n--- Agent tool trace ---")
        for message in messages:
            tool_calls = getattr(message, "tool_calls", None)
            if tool_calls:
                for call in tool_calls:
                    name = call.get("name", "unknown_tool")
                    args = call.get("args", {})
                    print(f"CALL  {name}({args})")
            if getattr(message, "type", "") == "tool":
                tool_name = getattr(message, "name", "tool")
                print(f"RESULT {tool_name}: {_content_to_text(message.content)}")
        print("--- End trace ---\n")

    if not messages:
        return "No response was returned by the agent."
    return _content_to_text(messages[-1].content)
