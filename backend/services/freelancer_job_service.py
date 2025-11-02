"""
Freelancer Job Content Generator
Generates AI-powered job descriptions for copy/paste to Freelancer
"""

from openai import OpenAI
from config import settings
import logging

logger = logging.getLogger(__name__)
openai_client = OpenAI(api_key=settings.openai_api_key)

async def generate_freelancer_job_content(
    company_name: str,
    analysis_summary: str
) -> str:
    """
    Generate Freelancer-ready job posting text

    Args:
        company_name: Name of the company being analyzed
        analysis_summary: Summary of key uncertainties from the debate

    Returns:
        Formatted job posting as plain text (ready to copy/paste to Freelancer)
    """

    prompt = f"""
Generate a compelling Freelancer.com job posting for validating AI-powered investment analysis.

Company being analyzed: {company_name}
AI Analysis Uncertainties: {analysis_summary}

Create an engaging, narrative-driven job post with this structure:

**Opening Hook:**
AI meets human expertise: We're building an AI-powered investment analysis platform, and we need your human judgment to validate our agents' work.

**What's Happening:**
Our AI agent system just completed a comprehensive analysis of {company_name}. Eight specialized AI agents debated the investment case from multiple angles - market size, team quality, competitive moats, financials, and risks.

The result? A 50/50 split. Our bull and bear agents made equally compelling arguments.

This is where you come in.

**Your Role:**
We need an independent human researcher to:
• Review our AI agents' analysis and identify blind spots
• Validate (or challenge) key market assumptions the AI made
• Conduct primary research our AI can't do (customer interviews, expert calls)
• Provide human judgment on qualitative factors AI struggles with
• Help us understand if our agents missed critical context

**Specific Research Tasks:**
[Based on the uncertainties above, create 5-7 specific, actionable tasks like:]
• Interview 10-15 potential customers in {company_name}'s target market (real humans, not AI-generated insights!)
• Validate TAM estimates through primary research and industry expert conversations
• Assess competitive threats our AI may have underweighted or missed entirely
• Research regulatory/compliance factors that require human expertise
• Provide qualitative assessment of founder credibility and execution risk
• Challenge or confirm our AI's assumptions with real-world data

**What You'll Get:**
• Access to our full AI analysis (comprehensive reports from 8 specialized agents)
• Clear research questions derived from agent disagreements
• Unique insight into how AI-powered investment analysis actually works
• Your research will directly influence a real investment decision

**What We're Looking For:**
• 3+ years market research, competitive intelligence, or strategy consulting experience
• Comfortable evaluating AI-generated analysis (we'll show you what our agents found)
• Strong primary research skills - you need to talk to real people, not just read reports
• Critical thinking - we want you to challenge our AI's conclusions
• Experience in [relevant industry for {company_name}] (bonus)
• Available to start immediately

**Compensation:**
$60-80/hour for a maximum of 15 hours

---

Make this sound exciting and unique - emphasize the AI-meets-human angle.
Use a conversational, compelling tone while remaining professional.
Make the researcher feel like they're part of something innovative.
Be specific about {company_name} and the key uncertainties from the AI analysis.
"""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )

        job_content = response.choices[0].message.content

        logger.info(f"✅ Generated Freelancer job content for {company_name}")

        return job_content

    except Exception as e:
        logger.error(f"Failed to generate Freelancer job content: {e}")
        raise
