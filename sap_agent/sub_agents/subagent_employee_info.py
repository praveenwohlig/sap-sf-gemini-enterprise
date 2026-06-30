"""
subagent_employee_info.py
══════════════════════════════════════════════════════════════
Subagent — Employee Information

Handles: employment termination, pension payout, work permits,
         job relationships, hire date changes,
         and person-level termination summary.
══════════════════════════════════════════════════════════════
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from ..tools import tools_employee_info as info

employee_info_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="employee_info_agent",
    instruction=(
        "You are an HR data specialist for employee information. "
        "Answer questions about the employee's employment termination details, "
        "pension payout schedule, work permits, job relationships, "
        "hire date changes, and person-level termination summary. "
        "Always call the relevant tool first — never guess or fabricate values. "
        "Return data in a clear, well-labelled format."
    ),
    tools=[
        # Employment Termination
        FunctionTool(func=info.get_my_employment_termination),

        # Pension Payout
        FunctionTool(func=info.get_my_pension_payout),

        # Work Permits
        FunctionTool(func=info.get_my_work_permits),

        # Job Relationships
        FunctionTool(func=info.get_my_job_relationships),

        # Hire Date Changes
        FunctionTool(func=info.get_my_hire_date_changes),

        # Person-level Termination Summary
        FunctionTool(func=info.get_my_person_emp_termination_info),
    ],
)
