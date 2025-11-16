# backend/app/prompts.py
"""
Prompt templates used with LangChain / any LLM.
Tweak these during testing to reduce hallucination.
"""

QUIZ_PROMPT = """
You are a precise assistant that MUST create a factual multiple-choice quiz grounded ONLY in the provided article content.
DO NOT hallucinate or invent facts. If something cannot be answered from the text, avoid it.

Article Title:
{title}

Article Text:
{article_text}

INSTRUCTIONS:
- Create between 5 and 10 multiple-choice questions.
- Each question must have exactly 4 options (list of option strings).
- Provide the correct answer as the option text (do NOT return only a letter).
- Provide a one-line explanation (<= 30 words) referencing where the answer appears (e.g. 'Early life paragraph').
- Assign one of these difficulty levels: easy, medium, hard.
- Balance difficulties across the quiz (not all easy).

OUTPUT FORMAT (JSON ONLY):
{{
  "quiz": [
    {{
      "question": "...",
      "options": ["opt1","opt2","opt3","opt4"],
      "answer": "opt2",
      "explanation": "...",
      "difficulty": "medium"
    }}
    , ...
  ]
}}
Strictly return valid JSON. If you cannot make 5 valid questions grounded in the text, return as many grounded questions as possible.
"""

RELATED_PROMPT = """
From the article title and text, suggest 4-8 related Wikipedia topics (short phrases) for further reading.
Return JSON only in this form:
{{ "related_topics": ["topic1", "topic2", ...] }}
Do not hallucinate — related topics should be clearly connected to the article text.
"""
