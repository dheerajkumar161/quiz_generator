import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_llm_chain_article_to_quiz():
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain.prompts import PromptTemplate
        from langchain.output_parsers import JsonOutputParser
    except ImportError:
        raise RuntimeError("Missing langchain-google-genai; please install dependencies.")
    llm = ChatGoogleGenerativeAI(model_name="gemini-pro", api_key=GEMINI_API_KEY, temperature=0.3)
    output_parser = JsonOutputParser()

    prompt_template = PromptTemplate(
        template="""
Given the following Wikipedia article, generate a quiz and associated metadata.

### Instructions:
- Use ONLY the provided article text, do not hallucinate facts.
- If information is not available, write \"Not specified\" for that field.
- Return a JSON object matching this format exactly:
{format_instructions}

--- ARTICLE START ---
{article_text}
--- ARTICLE END ---

### Notes
- Quiz: 5-10 multiple-choice questions. Each with:
    - question, 4 options, correct answer text, explanation, difficulty (easy/medium/hard)
- Extract: summary, sections, and key people, organizations, locations.
- Extract: 3-5 related Wikipedia topics for further reading.
""",
        input_variables=["article_text", "format_instructions"]
    )

    parser_instructions = """
{
  "url": "...",
  "title": "...",
  "summary": "...",
  "key_entities": {
    "people": ["..."],
    "organizations": ["..."],
    "locations": ["..."]
  },
  "sections": ["..."],
  "quiz": [
    {
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "...",
      "difficulty": "easy | medium | hard",
      "explanation": "..."
    }
  ],
  "related_topics": ["..."]
}
"""

    def generate_quiz(article_text, url, sections, summary):
        formatted_prompt = prompt_template.format(
            article_text=article_text,
            format_instructions=parser_instructions
        )
        response = llm.invoke(formatted_prompt)
        try:
            quiz_json = output_parser.parse(response.content)
        except Exception as e:
            raise RuntimeError("LLM output parse error: " + str(e))
        quiz_json["url"] = url
        quiz_json["summary"] = summary
        quiz_json["sections"] = sections
        return quiz_json

    return generate_quiz
