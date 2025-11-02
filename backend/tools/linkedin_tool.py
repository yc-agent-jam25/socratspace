"""
LinkedIn Profile Analyzer Tool
Analyzes LinkedIn profiles and posts via Metorial LinkedIn MCP or direct RapidAPI
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional
try:
    from backend.tools.mcp_client import mcp_client
    from backend.config import settings
except ImportError:
    from tools.mcp_client import mcp_client
    from config import settings
import logging
import asyncio
import os
import requests
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class LinkedInAnalyzerInput(BaseModel):
    """Input schema for LinkedIn analyzer"""
    username: str = Field(..., description="LinkedIn username/profile identifier (e.g., 'john-doe' or 'in/john-doe')")
    analyze_posts: bool = Field(
        default=True,
        description="Whether to fetch and analyze LinkedIn posts (default: True)"
    )
    top_n: int = Field(
        default=10,
        description="Number of top posts to analyze based on engagement (default: 10)"
    )

class LinkedInAnalyzerTool(BaseTool):
    """
    LinkedIn profile and posts analysis tool for founder evaluation
    """
    name: str = "LinkedIn Profile Analyzer"
    description: str = """
    Analyzes LinkedIn profiles and posts to evaluate founder professional background, network, and thought leadership.

    Use this tool to:
    - Check founder's professional experience and career trajectory
    - Analyze LinkedIn post engagement and thought leadership
    - Identify industry connections and network quality
    - Evaluate content quality and posting frequency
    - Assess professional credibility and expertise
    - Find top-performing posts and engagement metrics
    - Look for red flags (inactive profile, low engagement, negative sentiment)

    Returns: Profile stats, post analysis, engagement metrics, and professional credibility assessment.
    """
    args_schema: Type[BaseModel] = LinkedInAnalyzerInput

    def _fetch_profile_via_rapidapi(self, username: str) -> dict:
        """
        Fetch LinkedIn profile information directly via RapidAPI
        Supports both person profiles and company profiles
        
        Args:
            username: LinkedIn username/profile identifier (person or company)
            
        Returns:
            Dictionary with profile data or empty dict if not available
        """
        rapidapi_key = os.getenv("RAPIDAPI_KEY")
        if not rapidapi_key:
            return {}
        
        headers = {
            "x-rapidapi-key": rapidapi_key,
            "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
        }
        
        # Try person profile endpoints - use linkedin-api8 first (most comprehensive)
        person_endpoints = [
            ("https://linkedin-api8.p.rapidapi.com/", {"username": username}, "linkedin-api8.p.rapidapi.com"),
            ("https://linkedin-data-api.p.rapidapi.com/get-profile", {"username": username}, "linkedin-data-api.p.rapidapi.com"),
            ("https://linkedin-data-api.p.rapidapi.com/profile", {"username": username}, "linkedin-data-api.p.rapidapi.com"),
            ("https://linkedin-data-api.p.rapidapi.com/get-profile-info", {"username": username}, "linkedin-data-api.p.rapidapi.com"),
        ]
        
        for url, params, host in person_endpoints:
            try:
                headers_copy = headers.copy()
                headers_copy["x-rapidapi-host"] = host
                response = requests.get(url, headers=headers_copy, params=params, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    # Check for service suspension messages
                    if result.get('success') is False:
                        message = result.get('message', '')
                        if 'suspended' in message.lower():
                            logger.warning(f"LinkedIn API service suspended: {message}")
                            continue  # Try next endpoint
                    
                    # Verify we got valid data (data can be None if profile doesn't exist or API limit reached)
                    if result:
                        # linkedin-api8 returns {'success': true, 'data': {...}} or {'success': true, 'data': None}
                        if result.get('data') is not None:
                            return result
                        # Also accept direct data format (no wrapper)
                        elif 'firstName' in result or 'username' in result:
                            return result
            except requests.exceptions.RequestException:
                continue
            except Exception as e:
                logger.warning(f"Error parsing response from {url}: {e}")
                continue
        
        # Try company profile endpoint (companies use different format)
        # Companies might use: company/google, google, or linkedin.com/company/google
        company_username = username.replace("linkedin.com/company/", "").replace("company/", "").strip()
        company_endpoints = [
            ("https://linkedin-data-api.p.rapidapi.com/get-company", {"universalName": company_username}),
            ("https://linkedin-data-api.p.rapidapi.com/get-company", {"username": company_username}),
            ("https://linkedin-data-api.p.rapidapi.com/company", {"universalName": company_username}),
        ]
        
        for url, params in company_endpoints:
            try:
                response = requests.get(url, headers=headers, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    # Mark as company data for special handling
                    if data.get('success') or data.get('data', {}).get('type'):
                        return {"is_company": True, **data}
                    return data
            except requests.exceptions.RequestException:
                continue
        
        # If no profile endpoint works, return empty
        return {}

    def _fetch_via_rapidapi(self, username: str) -> dict:
        """
        Fetch LinkedIn posts directly via RapidAPI (fallback method)
        
        Args:
            username: LinkedIn username/profile identifier
            
        Returns:
            Dictionary with posts data or error information
        """
        rapidapi_key = os.getenv("RAPIDAPI_KEY")
        if not rapidapi_key:
            raise ValueError("RAPIDAPI_KEY not found in environment variables")
        
        url = "https://linkedin-data-api.p.rapidapi.com/get-profile-posts"
        headers = {
            "x-rapidapi-key": rapidapi_key,
            "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
        }
        querystring = {"username": username}
        
        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=30)
            
            # Check for subscription errors
            if response.status_code == 403:
                error_data = response.json() if response.content else {}
                if "not subscribed" in str(error_data).lower() or "subscription" in str(error_data).lower():
                    raise Exception(
                        "LinkedIn Data API subscription required. "
                        "Please subscribe to the LinkedIn Data API on RapidAPI: "
                        "https://rapidapi.com/ - Search for 'LinkedIn Data API' and subscribe to a plan."
                    )
            
            # Check for rate limiting
            if response.status_code == 429:
                raise Exception(
                    "Rate limit exceeded. "
                    "You've hit the API request limit for your subscription tier. "
                    "Please wait a few minutes or upgrade your RapidAPI plan."
                )
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                error_data = e.response.json() if e.response.content else {}
                if "not subscribed" in str(error_data).lower():
                    raise Exception(
                        "LinkedIn Data API subscription required. "
                        "Subscribe at: https://rapidapi.com/ (search for 'LinkedIn Data API')"
                    )
            logger.error(f"RapidAPI HTTP error: {str(e)}")
            raise Exception(f"Failed to fetch LinkedIn data: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"RapidAPI request failed: {str(e)}")
            raise Exception(f"Failed to fetch LinkedIn data: {str(e)}")

    def _format_profile_info(self, profile_data: dict, posts_data: list = None) -> str:
        """
        Format profile information for analysis
        
        Args:
            profile_data: Profile information dict
            posts_data: Optional posts data (may contain author info)
            
        Returns:
            Formatted profile information string
        """
        profile_info = []
        
        # Extract from profile_data
        if profile_data:
            # Check if this is company data
            is_company = profile_data.get('is_company', False)
            # Handle API response format: {"success": true, "data": {...}} or direct data
            if 'data' in profile_data:
                profile_data_value = profile_data.get('data')
                # Check if data is None (API might return success but data=None)
                if profile_data_value is not None and isinstance(profile_data_value, dict):
                    data = profile_data_value
                elif isinstance(profile_data, dict) and ('firstName' in profile_data or 'username' in profile_data):
                    # Direct data format (no wrapper)
                    data = profile_data
                else:
                    # data is None - return helpful message
                    message = profile_data.get('message', '')
                    if message:
                        return f"LinkedIn API returned: {message}\n\nThis might indicate:\n- Service suspension\n- Rate limit reached\n- Subscription limitations\n- Profile not found in API database"
                    return "Profile data not available from API."
            elif isinstance(profile_data, dict):
                data = profile_data
            else:
                data = {}
            
            if is_company or data.get('type') == 'Public Company' or data.get('type') == 'Company':
                # Handle company profile data
                name = data.get('name', '')
                headline = data.get('tagline', '')
                industry = ", ".join(data.get('industries', [])) if data.get('industries') else data.get('industry', '')
                location = None
                if data.get('headquarter'):
                    hq = data.get('headquarter', {})
                    location = f"{hq.get('city', '')}, {hq.get('country', '')}".strip(', ')
                
                staff_count = data.get('staffCount', '')
                follower_count = data.get('followerCount', '')
                description = data.get('description', '')[:300] + "..." if len(data.get('description', '')) > 300 else data.get('description', '')
                website = data.get('website', '')
                founded = data.get('founded', '')
                specialities = ", ".join(data.get('specialities', [])) if data.get('specialities') else ''
                
                profile_info.append(f"Company: {name}")
                if headline:
                    profile_info.append(f"Tagline: {headline}")
                if industry:
                    profile_info.append(f"Industry: {industry}")
                if location:
                    profile_info.append(f"Headquarters: {location}")
                if staff_count:
                    profile_info.append(f"Staff Count: {staff_count:,}")
                if follower_count:
                    profile_info.append(f"Followers: {follower_count:,}")
                if description:
                    profile_info.append(f"Description: {description}")
                if website:
                    profile_info.append(f"Website: {website}")
                if founded:
                    profile_info.append(f"Founded: {founded}")
                if specialities:
                    profile_info.append(f"Specialities: {specialities}")
                
                return "\n".join(profile_info)
            
            # Handle person profile data (linkedin-api8 format or other formats)
            # Check for linkedin-api8 format (has firstName/lastName directly)
            if data and isinstance(data, dict) and ('firstName' in data or 'position' in data):
                # linkedin-api8 format
                try:
                    name = f"{data.get('firstName', '')} {data.get('lastName', '')}".strip()
                    headline = data.get('headline') or (data.get('multiLocaleHeadline', {}) or {}).get('en', '')
                    summary = data.get('summary', '')
                    geo = data.get('geo') or {}
                    if isinstance(geo, dict):
                        location = geo.get('full') or f"{geo.get('city', '')}, {geo.get('country', '')}".strip(', ')
                    else:
                        location = ""
                    
                    # Check for premium/creator indicators
                    is_top_voice = data.get('isTopVoice', False)
                    is_creator = data.get('isCreator', False)
                    is_premium = data.get('isPremium', False)
                    
                    profile_info.append(f"Name: {name}")
                    if headline:
                        profile_info.append(f"Headline: {headline}")
                    if location:
                        profile_info.append(f"Location: {location}")
                    if is_top_voice:
                        profile_info.append("🎖️ Top Voice")
                    if is_creator:
                        profile_info.append("✍️ Creator")
                    if is_premium:
                        profile_info.append("⭐ Premium Member")
                    if summary:
                        profile_info.append(f"Summary: {summary[:300]}...")
                    
                    # Format experience (linkedin-api8 uses 'position' or 'fullPositions')
                    positions = data.get('fullPositions') or data.get('position')
                    if positions is None:
                        positions = []
                    if positions and isinstance(positions, list):
                        profile_info.append("\n💼 Work Experience:")
                        for i, pos in enumerate(positions[:5], 1):  # Limit to top 5
                            if not isinstance(pos, dict):
                                continue
                            title = pos.get('title') or (pos.get('multiLocaleTitle', {}) or {}).get('en_US', '')
                            company = pos.get('companyName') or (pos.get('multiLocaleCompanyName', {}) or {}).get('en_US', '')
                            start_date = pos.get('start', {}) or {}
                            end_date = pos.get('end', {}) or {}
                            
                            if start_date.get('year') or end_date.get('year'):
                                start_str = f"{start_date.get('year', '')}" if start_date.get('year') else ""
                                end_str = f"{end_date.get('year', '')}" if end_date.get('year') else "Present"
                                duration = f"{start_str}-{end_str}" if start_str else end_str
                            else:
                                duration = ""
                            
                            if title or company:
                                exp_str = f"  {i}. "
                                if title:
                                    exp_str += f"{title}"
                                if company:
                                    exp_str += f" at {company}"
                                if duration:
                                    exp_str += f" ({duration})"
                                profile_info.append(exp_str)
                                
                                # Add description if available
                                if pos.get('description'):
                                    desc = pos.get('description', '')[:150]
                                    profile_info.append(f"     {desc}...")
                    
                    # Format education (linkedin-api8 uses 'educations')
                    educations = data.get('educations')
                    if educations is None:
                        educations = []
                    if educations and isinstance(educations, list):
                        profile_info.append("\n🎓 Education:")
                        for i, edu in enumerate(educations[:3], 1):  # Limit to top 3
                            if not isinstance(edu, dict):
                                continue
                            school = edu.get('schoolName', '')
                            degree = edu.get('degree', '')
                            field = edu.get('fieldOfStudy', '')
                            if school or degree:
                                edu_str = f"  {i}. "
                                if degree:
                                    edu_str += f"{degree}"
                                if field:
                                    edu_str += f" in {field}"
                                if school:
                                    edu_str += f" from {school}"
                                profile_info.append(edu_str)
                    
                    # Format skills (linkedin-api8 has 'skills' array)
                    skills = data.get('skills')
                    if skills and isinstance(skills, list) and len(skills) > 0:
                        profile_info.append("\n🛠️ Top Skills:")
                        try:
                            top_skills = sorted(skills, key=lambda x: (x.get('endorsementsCount', 0) if isinstance(x, dict) else 0), reverse=True)[:5]
                            skill_names = [s.get('name', '') for s in top_skills if isinstance(s, dict) and s.get('name')]
                            if skill_names:
                                profile_info.append(f"  {', '.join(skill_names)}")
                        except (TypeError, AttributeError):
                            # Fallback: just list skill names if available
                            skill_names = [s.get('name', '') if isinstance(s, dict) else str(s) for s in skills[:5] if s and s is not None]
                            if skill_names:
                                profile_info.append(f"  {', '.join([n for n in skill_names if n])}")
                except Exception as e:
                    logger.warning(f"Error formatting linkedin-api8 profile data: {e}")
                    # Add basic info even if formatting fails
                    if data.get('firstName') or data.get('lastName'):
                        name = f"{data.get('firstName', '')} {data.get('lastName', '')}".strip()
                        if name:
                            profile_info.append(f"Name: {name}")
                    if data.get('headline'):
                        profile_info.append(f"Headline: {data.get('headline', '')}")
            
            else:
                # Fallback to other API formats
                name = (
                    data.get('name') or 
                    data.get('fullName') or 
                    f"{data.get('firstName', '')} {data.get('lastName', '')}".strip()
                )
                headline = data.get('headline') or data.get('title') or data.get('position')
                industry = data.get('industry') or data.get('sector')
                location = data.get('location') or data.get('country')
                experience = data.get('experience') or data.get('positions') or data.get('workExperience')
                education = data.get('education') or data.get('schools')
                connections = data.get('connections') or data.get('connectionCount')
                summary = data.get('summary') or data.get('about')
                
                if name:
                    profile_info.append(f"Name: {name}")
                if headline:
                    profile_info.append(f"Headline: {headline}")
                if industry:
                    profile_info.append(f"Industry: {industry}")
                if location:
                    profile_info.append(f"Location: {location}")
                if connections:
                    profile_info.append(f"Connections: {connections}")
                if summary:
                    profile_info.append(f"Summary: {summary[:200]}...")
                
                # Format experience
                if experience:
                    profile_info.append("\n💼 Work Experience:")
                    exp_list = experience if isinstance(experience, list) else experience.get('values', [])
                    for i, exp in enumerate(exp_list[:5], 1):  # Limit to top 5
                        title = exp.get('title') or exp.get('positionTitle')
                        company = exp.get('companyName') or (exp.get('company', {}).get('name') if isinstance(exp.get('company'), dict) else None)
                        duration = exp.get('duration') or exp.get('timePeriod')
                        if title or company:
                            exp_str = f"  {i}. "
                            if title:
                                exp_str += f"{title}"
                            if company:
                                exp_str += f" at {company}"
                            if duration:
                                exp_str += f" ({duration})"
                            profile_info.append(exp_str)
                
                # Format education
                if education:
                    profile_info.append("\n🎓 Education:")
                    edu_list = education if isinstance(education, list) else education.get('values', [])
                    for i, edu in enumerate(edu_list[:3], 1):  # Limit to top 3
                        school = edu.get('schoolName') or (edu.get('school', {}).get('name') if isinstance(edu.get('school'), dict) else None)
                        degree = edu.get('degree') or edu.get('fieldOfStudy')
                        if school or degree:
                            edu_str = f"  {i}. "
                            if degree:
                                edu_str += f"{degree}"
                            if school:
                                edu_str += f" from {school}"
                            profile_info.append(edu_str)
        
        # Fallback: Extract from posts data (author info)
        elif posts_data and len(posts_data) > 0:
            first_post = posts_data[0]
            author_name = first_post.get('Author Name', '').strip()
            author_headline = first_post.get('Author Headline', '').strip()
            author_profile = first_post.get('Author Profile', '')
            
            if author_name:
                profile_info.append(f"Name: {author_name}")
            if author_headline:
                profile_info.append(f"Headline: {author_headline}")
            if author_profile:
                profile_info.append(f"Profile URL: {author_profile}")
        
        if not profile_info:
            return "Profile information not available from API."
        
        return "\n".join(profile_info)

    def _analyze_posts_data(self, posts_data: list, top_n: int = 10) -> str:
        """
        Analyze LinkedIn posts data and format for LLM consumption
        
        Args:
            posts_data: List of post dictionaries
            top_n: Number of top posts to highlight
            
        Returns:
            Formatted analysis string
        """
        if not posts_data or posts_data is None:
            return "No posts found for this profile."
        
        # Ensure posts_data is a list
        if not isinstance(posts_data, list):
            return "No posts found for this profile."
        
        # Calculate metrics
        total_posts = len(posts_data)
        total_likes = sum(post.get('Like Count', 0) for post in posts_data)
        total_reactions = sum(post.get('Total Reactions', 0) for post in posts_data)
        avg_likes = total_likes / total_posts if total_posts > 0 else 0
        avg_reactions = total_reactions / total_posts if total_posts > 0 else 0
        
        # Get top posts by engagement
        sorted_posts = sorted(
            posts_data,
            key=lambda x: x.get('Total Reactions', 0),
            reverse=True
        )
        top_posts = sorted_posts[:top_n]
        
        # Extract dates for activity analysis
        dates = []
        for post in posts_data:
            date_str = post.get('Posted Date', '')
            if date_str:
                try:
                    dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
                except ValueError:
                    pass
        
        # Activity analysis
        if dates:
            dates.sort(reverse=True)
            most_recent = dates[0].strftime("%Y-%m-%d")
            oldest = dates[-1].strftime("%Y-%m-%d")
            days_active = (dates[0] - dates[-1]).days if len(dates) > 1 else 0
            avg_days_between = days_active / len(dates) if len(dates) > 1 else 0
        else:
            most_recent = "Unknown"
            oldest = "Unknown"
            avg_days_between = 0
        
        # Format analysis
        analysis = f"""
=== LinkedIn Profile Analysis ===
Total Posts Analyzed: {total_posts}

📊 Engagement Metrics:
- Total Likes: {total_likes:,}
- Total Reactions: {total_reactions:,}
- Average Likes per Post: {avg_likes:.1f}
- Average Reactions per Post: {avg_reactions:.1f}

📅 Activity Timeline:
- Most Recent Post: {most_recent}
- Oldest Post: {oldest}
- Average Days Between Posts: {avg_days_between:.1f} days

🏆 Top {min(top_n, len(top_posts))} Posts by Engagement:
"""
        for i, post in enumerate(top_posts, 1):
            text_preview = post.get('Text', '')[:150] + "..." if len(post.get('Text', '')) > 150 else post.get('Text', '')
            likes = post.get('Like Count', 0)
            reactions = post.get('Total Reactions', 0)
            date = post.get('Posted Date', 'Unknown')
            url = post.get('Post URL', 'N/A')
            
            analysis += f"""
{i}. Date: {date} | Reactions: {reactions} | Likes: {likes}
   Preview: {text_preview}
   URL: {url}
"""
        
        # Add assessment notes
        analysis += f"""
=== Professional Assessment ===
"""
        
        if avg_reactions > 50:
            analysis += "✅ Strong engagement - indicates active professional network and thought leadership\n"
        elif avg_reactions > 20:
            analysis += "✓ Moderate engagement - reasonable professional presence\n"
        else:
            analysis += "⚠ Low engagement - may indicate inactive network or low visibility\n"
        
        if avg_days_between < 7:
            analysis += "✅ High posting frequency - active thought leader\n"
        elif avg_days_between < 30:
            analysis += "✓ Regular posting - consistent professional presence\n"
        else:
            analysis += "⚠ Low posting frequency - may be less active on LinkedIn\n"
        
        analysis += f"""
Red Flags to Consider:
- Very low engagement could indicate fake/bot account or inactive network
- Infrequent posting may suggest lack of thought leadership
- Negative sentiment in posts could indicate professional issues
"""
        
        return analysis

    def _run(self, username: str, analyze_posts: bool = True, top_n: int = 10) -> str:
        """
        Execute LinkedIn analysis via Metorial LinkedIn MCP or direct RapidAPI

        Args:
            username: LinkedIn username/profile identifier
            analyze_posts: Whether to fetch and analyze posts
            top_n: Number of top posts to analyze

        Returns:
            Formatted string with LinkedIn profile and posts analysis
        """

        async def analyze():
            try:
                logger.info(f"Analyzing LinkedIn profile '{username}' (analyze_posts: {analyze_posts}, top_n: {top_n})")

                # Try using Metorial MCP first (preferred method)
                use_metorial = settings.mcp_linkedin_id is not None
                
                if use_metorial:
                    try:
                        # Call MCP via Metorial with natural language
                        result = await mcp_client.call_mcp(
                            mcp_name="linkedin",
                            tool_name="analyze_profile",  # For logging only
                            parameters={
                                "username": username,
                                "analyze_posts": analyze_posts,
                                "top_n": top_n
                            },
                            natural_message=f"""
                            Analyze the LinkedIn profile for user "{username}".

                            Please provide:
                            1. **Profile Overview**: Basic profile information, headline, industry
                            2. **Post Analysis** (if analyze_posts is True):
                               - Fetch and save LinkedIn posts for this profile
                               - Calculate engagement metrics (likes, reactions, comments)
                               - Identify top {top_n} performing posts by engagement
                               - Analyze posting frequency and activity timeline
                            3. **Professional Assessment**:
                               - Network engagement level
                               - Thought leadership indicators
                               - Posting consistency
                            4. **Red Flags**:
                               - Low engagement (possible inactive/bot account)
                               - Infrequent posting
                               - Negative sentiment

                            Format as a structured professional evaluation suitable for founder due diligence.
                            """
                        )

                        # Extract text from RunResult
                        linkedin_content = result.text

                        # Format for LLM consumption
                        formatted = f"""
=== LinkedIn Professional Evaluation ===
Username: {username}
Post Analysis: {"Included" if analyze_posts else "Excluded"}

{linkedin_content}

=== End of LinkedIn Analysis ===

Professional Credibility Score: Evaluate based on engagement, posting frequency, and content quality.
Red Flags: Watch for inactive profiles, low engagement, or lack of professional thought leadership.
"""
                        logger.info(f"LinkedIn analysis completed via Metorial MCP for '{username}'")
                        return formatted

                    except Exception as mcp_error:
                        logger.warning(f"Metorial MCP failed, falling back to direct API: {str(mcp_error)}")
                        use_metorial = False  # Fall back to direct API

                # Fallback: Direct RapidAPI integration
                if not use_metorial:
                    # Check if RapidAPI key is available
                    rapidapi_key = os.getenv("RAPIDAPI_KEY")
                    if not rapidapi_key:
                        return f"""
⚠️ LinkedIn Profile Analyzer is not configured.

To use this tool, you need to add one of the following to your .env file:

Option 1: RapidAPI (Direct API Access)
  RAPIDAPI_KEY=your_rapidapi_key_here
  
  Get your key from: https://rapidapi.com/
  - Search for "LinkedIn Data API"
  - Subscribe to a plan (some have free tiers)
  - Copy your X-RapidAPI-Key from Dashboard → Security

Option 2: Metorial MCP (Recommended if using other MCPs)
  MCP_LINKEDIN_ID=your_metorial_deployment_id
  
  Deploy LinkedIn MCP on Metorial and use the deployment ID.

Note: Without API access, LinkedIn profile analysis cannot be performed.
"""
                    
                    logger.info("Using direct RapidAPI integration")
                    
                    # Fetch profile information
                    profile_data = {}
                    try:
                        profile_data = self._fetch_profile_via_rapidapi(username)
                        logger.info(f"Profile data fetched: {bool(profile_data)}")
                    except Exception as e:
                        logger.warning(f"Could not fetch profile info: {str(e)}")
                    
                    # Fetch posts data (optional - may fail if posts endpoint doesn't exist)
                    posts = []
                    try:
                        api_response = self._fetch_via_rapidapi(username)
                        
                        # Parse and transform data (similar to original MCP implementation)
                        if api_response and isinstance(api_response, dict):
                            posts_data = api_response.get('data', [])
                            if posts_data and isinstance(posts_data, list):
                                for post in posts_data:
                                    if not isinstance(post, dict):
                                        continue
                                    author = post.get('author', {}) or {}
                                    if not isinstance(author, dict):
                                        author = {}
                                    images = post.get('image', []) or []
                                    if not isinstance(images, list):
                                        images = []
                                    
                                    posts.append({
                                        "Post URL": post.get('postUrl', ''),
                                        "Text": post.get('text', ''),
                                        "Like Count": post.get('likeCount', 0),
                                        "Total Reactions": post.get('totalReactionCount', 0),
                                        "Posted Date": post.get('postedDate', ''),
                                        "Posted Timestamp": post.get('postedDateTimestamp', ''),
                                        "Share URL": post.get('shareUrl', ''),
                                        "Author Name": f"{author.get('firstName', '')} {author.get('lastName', '')}".strip(),
                                        "Author Profile": author.get('url', ''),
                                        "Author Headline": author.get('headline', ''),
                                        "Author Profile Picture": (author.get('profilePictures', [{}])[0].get('url', '') if author.get('profilePictures') and isinstance(author.get('profilePictures'), list) else ''),
                                        "Main Image": (images[0].get('url', '') if images and isinstance(images[0], dict) else ''),
                                        "All Images": ", ".join([img.get('url', '') for img in images if isinstance(img, dict)]),
                                    })
                    except Exception as e:
                        logger.warning(f"Could not fetch posts: {str(e)}")
                        # Continue without posts - profile info is still valuable
                    
                    # Format profile information
                    profile_section = self._format_profile_info(profile_data, posts)
                    
                    if not analyze_posts:
                        return f"""
=== LinkedIn Profile Information ===
Username: {username}

{profile_section}

=== End of Profile Information ===

Note: Set analyze_posts=True to get detailed post analysis.
"""
                    
                    # Analyze posts
                    if posts and isinstance(posts, list) and len(posts) > 0:
                        posts_analysis = self._analyze_posts_data(posts, top_n)
                    else:
                        posts_analysis = "No posts found."
                    
                    # Format for LLM consumption
                    formatted = f"""
=== LinkedIn Professional Evaluation ===
Username: {username}

📋 Profile Overview:
{profile_section}

{posts_analysis if posts else ""}

=== End of LinkedIn Analysis ===

Professional Credibility Score: Evaluate based on profile completeness, engagement metrics, posting frequency, and content quality.
Red Flags: Watch for incomplete profiles, inactive profiles (low engagement, infrequent posting), or lack of professional thought leadership.
"""
                    
                    logger.info(f"LinkedIn analysis completed via RapidAPI for '{username}'")
                    return formatted

            except Exception as e:
                error_msg = f"Error analyzing LinkedIn profile '{username}': {str(e)}"
                logger.error(error_msg)
                return f"❌ {error_msg}\n\nNote: Profile may not exist, may be private, or RapidAPI key may be missing."

        return asyncio.run(analyze())

