# backend/app/llm_client.py
"""
Simple LangChain/OpenAI example wrapper.
Replace with your provider (Gemini/Vertex/etc.) by changing the LLM class and env var handling.
Keep temperature low (0-0.2) for deterministic, grounded outputs.
"""

import os
import json
import re
from .prompts import QUIZ_PROMPT, RELATED_PROMPT

# LangChain/OpenAI imports
from langchain.llms import OpenAI  # change if using a different provider
from langchain import LLMChain
from langchain.prompts import PromptTemplate

def _safe_parse_json(text: str):
    """
    Try direct json parse, else extract first JSON object substring.
    Returns dict or raises ValueError.
    """
    try:
        return json.loads(text)
    except Exception:
        # try to extract {...}
        m = re.search(r"\{(?:[^{}]|(?R))*\}", text, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise ValueError("Failed to parse JSON from LLM output")

def get_llm():
    """
    Create a LangChain LLM instance. Replace or extend for Gemini/Vertex.
    Requires OPENAI_API_KEY in env for this example.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    return OpenAI(temperature=0, openai_api_key=api_key, max_tokens=1200)

def generate_quiz_and_topics(title: str, article_text: str) -> dict:
    llm = get_llm()

    # Quiz
    quiz_prompt = PromptTemplate(input_variables=["title", "article_text"], template=QUIZ_PROMPT)
    quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt)
    quiz_out = quiz_chain.run({"title": title, "article_text": article_text})

    # Related topics
    rel_prompt = PromptTemplate(input_variables=["title", "article_text"], template=RELATED_PROMPT)
    rel_chain = LLMChain(llm=llm, prompt=rel_prompt)
    rel_out = rel_chain.run({"title": title, "article_text": article_text})

    # Parse outputs
    try:
        quiz_json = _safe_parse_json(quiz_out)
    except Exception as e:
        # best-effort fallback: return empty quiz and include raw text for debugging
        quiz_json = {"quiz": []}
        # Optionally log quiz_out to file or monitoring system

    try:
        rel_json = _safe_parse_json(rel_out)
    except Exception:
        rel_json = {"related_topics": []}

    return {
        "quiz": quiz_json.get("quiz", []),
        "related_topics": rel_json.get("related_topics", [])
    }
