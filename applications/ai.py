import json
import re

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma2:2b"


def _clean_json_reply(raw_reply):
    text = raw_reply.strip()
    text = re.sub(r"^```(json)?", "", text.strip())
    text = re.sub(r"```$", "", text.strip())
    return text.strip()


def _ask_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    headers = {"Accept": "*/*", "Content-Type": "application/json"}
    response = requests.post(
        OLLAMA_URL, headers=headers, data=json.dumps(payload), timeout=60
    )
    response.raise_for_status()
    return response.json()["response"]


def generate_interview_questions(job):
    """
    Takes a Job instance and returns a list of 5 question strings,
    based on that job's title and description.
    """
    prompt = f"""You are helping screen a candidate for this job.

Job title: {job.title}
Job description: {job.description}

Write exactly 5 interview questions for this role.
Return ONLY a JSON array of 5 strings.
Do NOT include explanations, markdown, code fences, or any extra text.
The response must begin with '[' and end with ']'.
Example: ["Question 1?", "Question 2?", "Question 3?", "Question 4?", "Question 5?"]"""

    raw_reply = _ask_ollama(prompt)

    try:
        questions = json.loads(_clean_json_reply(raw_reply))
    except (json.JSONDecodeError, TypeError):
        # if the AI ever replies with something that isn't valid JSON,
        # fall back to generic questions instead of crashing the page
        questions = [
            "Tell us about your relevant experience for this role.",
            "Why do you want this job?",
            "Describe a challenging project you have worked on.",
            "How do you handle tight deadlines?",
            "What makes you a good fit for this position?",
        ]
    return questions


def evaluate_interview_answers(job, questions, answers):
    """
    Takes the job, the questions asked, and the applicant's answers,
    and returns (score, feedback) where score is 0-100.
    """
    qa_text = "\n".join(
        f"Q{i + 1}: {q}\nA{i + 1}: {a}" for i, (q, a) in enumerate(zip(questions, answers))
    )

    prompt = f"""You are evaluating a candidate's interview answers for this job.

Job title: {job.title}
Job description: {job.description}

{qa_text}

Score the candidate from 0 to 100 based on how relevant and strong their
answers are for this specific job.
Return ONLY valid JSON in this exact shape.
Do NOT include explanations, markdown, code fences, or any extra text.
{{"score": 0, "feedback": "2-3 sentences of feedback"}}"""

    raw_reply = _ask_ollama(prompt)

    try:
        result = json.loads(_clean_json_reply(raw_reply))
        score = int(result.get("score", 0))
        feedback = result.get("feedback", "")
    except (json.JSONDecodeError, TypeError, ValueError):
        score = 0
        feedback = "We could not automatically evaluate these answers."

    return score, feedback