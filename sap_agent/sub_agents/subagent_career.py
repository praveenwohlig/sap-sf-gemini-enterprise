"""
subagent_career.py
══════════════════════════════════════════════════════════════
Subagent — Career Background & Skills

Handles: education, certifications, languages, previous employers,
         internal job history, special projects, training courses,
         functional expertise, leadership, awards, badges,
         memberships, and community involvement.
══════════════════════════════════════════════════════════════
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from . import tools_employee_profile as emp

career_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="career_agent",
    instruction=(
        "You are an HR data specialist for employee career history, background, and skills. "
        "Answer questions about education, certifications, languages spoken, previous employers, "
        "internal job history, special projects, training courses, functional expertise, "
        "leadership experience, awards, recognition badges, professional memberships, "
        "and community involvement. "
        "Always call the relevant tool first — never guess or fabricate values. "
        "Return data in a clear, well-labelled format."
    ),
    tools=[
        # Education & Qualifications
        FunctionTool(func=emp.get_my_education),
        FunctionTool(func=emp.get_my_certifications),
        FunctionTool(func=emp.get_my_languages),

        # Work Experience
        FunctionTool(func=emp.get_my_previous_employers),
        FunctionTool(func=emp.get_my_internal_job_history),
        FunctionTool(func=emp.get_my_special_projects),
        FunctionTool(func=emp.get_my_training_courses),

        # Skills & Expertise
        FunctionTool(func=emp.get_my_functional_expertise),
        FunctionTool(func=emp.get_my_leadership_experience),

        # Recognition & Memberships
        FunctionTool(func=emp.get_my_awards),
        FunctionTool(func=emp.get_my_badges),
        FunctionTool(func=emp.get_my_professional_memberships),
        FunctionTool(func=emp.get_my_community_involvement),
    ],
)
