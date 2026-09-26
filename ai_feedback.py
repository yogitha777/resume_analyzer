"""
Optional Advanced Feature (PDF Section 13): LLM-generated resume feedback
using a controlled prompt for ResumeIQ.

This module is intentionally optional and safe-by-default:
- If no GEMINI_API_KEY is set, `generate_ai_feedback` returns None and the
  app simply skips this section — no crash, no requirement to use it.
- The prompt is "controlled": it only ever receives the extracted skill list,
  the target role, and the missing skills — never the raw resume text, and
  never any personal/identifying information. This keeps the feature aligned
  with the Responsible AI rules in Module 12 of the project brief.
"""

import os


def _get_api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY", "").strip() or None


def is_ai_feedback_available() -> bool:
    """Lets the UI check whether it should even show the feature toggle."""
    return _get_api_key() is not None


def generate_ai_feedback(
    target_role: str,
    matching_skills: list,
    missing_skills: list,
    match_score: float,
) -> str | None:
    """
    Generates a short, encouraging feedback paragraph using Gemini.

    Returns None if no API key is configured, or a short error string if the
    call fails, so the caller can display it gracefully rather than crash.
    """
    api_key = _get_api_key()
    if not api_key:
        return None

    # Controlled prompt: fixed structure, only skill-level data, explicit
    # constraints on tone and scope so the model can't be steered into
    # commenting on anything outside job-related skills.
    prompt = f"""You are a career coaching assistant helping a student improve
their resume for a specific job role. You are given only skill-level data,
never the resume text itself or any personal information.

Target role: {target_role}
Overall match score: {match_score}%
Skills already present: {", ".join(matching_skills) if matching_skills else "none detected"}
Missing skills for this role: {", ".join(missing_skills) if missing_skills else "none"}

Write a short (4-6 sentence), encouraging, constructive piece of feedback for
the student. Rules:
- Only discuss job-related skills, projects, and learning suggestions.
- Do not mention or speculate about gender, age, name, nationality, ethnicity,
  religion, marital status, disability, or any personal characteristic.
- Do not claim the student is unqualified — frame missing skills as growth
  areas, not deficiencies.
- Do not guarantee job placement or interview outcomes.
- Keep it plain text, no markdown headers.
"""

    try:
        from google import genai
        from google.genai import types, errors

        client = genai.Client(api_key=api_key)

        # Candidate models list in order of preference to ensure SDK compatibility
        candidate_models = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-2.5-pro",
        ]

        # Dynamically attempt model discovery if available
        available_model = None
        try:
            models_page = client.models.list()
            for m in models_page:
                name = getattr(m, "name", "") or ""
                # Strip leading 'models/' prefix if present
                clean_name = name.replace("models/", "")
                if "gemini" in clean_name and "flash" in clean_name:
                    available_model = clean_name
                    break
        except Exception:
            pass

        if available_model:
            candidate_models.insert(0, available_model)

        last_error = None
        for model_name in candidate_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        http_options=types.HttpOptions(
                            timeout=15_000,
                            retry_options=types.HttpRetryOptions(
                                attempts=2,
                                initial_delay=1.0,
                                max_delay=3.0,
                                http_status_codes=[429, 500, 502, 503, 504],
                            ),
                        )
                    ),
                )
                text = (response.text or "").strip()
                if text:
                    return text
                else:
                    return (
                        "⚠️ AI feedback unavailable right now (empty response). "
                        "Showing rule-based results only."
                    )
            except errors.ClientError as exc:
                if exc.code == 404:
                    last_error = exc
                    continue  # Try next candidate model
                elif exc.code in (401, 403):
                    return "⚠️ AI feedback unavailable right now (invalid or unauthorized API key). Showing rule-based results only."
                elif exc.code == 429:
                    return "⚠️ AI feedback unavailable right now (rate limit or quota exceeded). Showing rule-based results only."
                else:
                    return f"⚠️ AI feedback unavailable right now ({exc.message or 'request rejected'}). Showing rule-based results only."
            except Exception as e:
                last_error = e
                break

        if isinstance(last_error, errors.ClientError) and last_error.code == 404:
            return "⚠️ AI feedback unavailable right now (model not found — check the model name is current). Showing rule-based results only."
        return f"⚠️ AI feedback unavailable right now ({last_error.__class__.__name__ if last_error else 'Unknown error'}). Showing rule-based results only."

    except errors.ClientError as exc:
        if exc.code in (401, 403):
            reason = "invalid or unauthorized API key"
        elif exc.code == 404:
            reason = "model not found — check the model name is current"
        elif exc.code == 429:
            reason = "rate limit or quota exceeded"
        else:
            reason = exc.message or "request rejected"
        return f"⚠️ AI feedback unavailable right now ({reason}). Showing rule-based results only."

    except errors.ServerError:
        return (
            "⚠️ AI feedback unavailable right now (Gemini is temporarily "
            "unreachable). Showing rule-based results only."
        )

    except TimeoutError:
        return (
            "⚠️ AI feedback unavailable right now (request timed out). "
            "Showing rule-based results only."
        )

    except Exception as exc:
        return f"⚠️ AI feedback unavailable right now ({exc.__class__.__name__}). Showing rule-based results only."
