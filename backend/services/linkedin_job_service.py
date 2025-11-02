"""
LinkedIn Job Content Generator
Generates AI-powered job descriptions for copy/paste to LinkedIn
"""

from openai import OpenAI
from config import settings
import logging

logger = logging.getLogger(__name__)
openai_client = OpenAI(api_key=settings.openai_api_key)

async def generate_linkedin_job_content(
    company_name: str,
    analysis_summary: str
) -> str:
    """
    Generate LinkedIn-ready job posting text

    Args:
        company_name: Name of the company being analyzed
        analysis_summary: Summary of key uncertainties from the debate

    Returns:
        Formatted job posting as plain text (ready to copy/paste to LinkedIn)
    """

    prompt = f"""
Generate a LinkedIn job posting for a Contract Researcher position.

Company: {company_name}
Context: Investment analysis team had a 50/50 split debate. Need independent researcher to validate key market assumptions.

Key Uncertainties: {analysis_summary}

Create a compelling LinkedIn job post with:

**Job Title:** Contract Researcher - Market Validation for {company_name}

**About the Role:**
[2-3 sentences explaining why we need this research]

**What You'll Do:**
• [5-7 specific research tasks based on the uncertainties above]
• [Include competitive analysis, market validation, stakeholder interviews]
• [Compile findings into actionable report]

**What We're Looking For:**
• 3+ years market research experience
• Industry expertise in [relevant domain]
• Strong analytical and written communication skills
• Available to start within 1 week

**Project Details:**
💰 Compensation: $5,000 - $8,000
⏰ Duration: 4-6 weeks
📍 Location: Remote

**To Apply:**
Send your resume and a brief paragraph about your relevant experience to [contact email]

---

Format this as clean, LinkedIn-ready text that can be copied and pasted directly.
Use emojis where appropriate to make it engaging.
Make it specific to {company_name}'s situation.
Keep it professional but compelling.
"""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )

        job_content = response.choices[0].message.content

        logger.info(f"✅ Generated LinkedIn job content for {company_name}")

        return job_content

    except Exception as e:
        logger.error(f"Failed to generate LinkedIn job content: {e}")
        raise
