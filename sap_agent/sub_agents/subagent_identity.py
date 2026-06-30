"""
subagent_identity.py
══════════════════════════════════════════════════════════════
Subagent — Identity & Org Chart

Handles: core profile, personal details, employment record,
         contact info, national IDs, global assignments,
         public profile, manager, and direct reports.
══════════════════════════════════════════════════════════════
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from ..tools import tools_employee_profile as emp

identity_agent = LlmAgent(
    model="gemini-3.5-flash",
    name="identity_agent",
    instruction=(
        "You are an HR data specialist for employee identity and organisational information. "
        "Answer questions about the employee's profile, personal details, employment record, "
        "contact information (email, phone, address, emergency contacts), "
        "national IDs, global assignments, public bio, manager, and direct reports. "
        "Always call the relevant tool first — never guess or fabricate values. "
        "Return data in a clear, well-labelled format."
    ),
    tools=[
        # Identity & Core Profile
        FunctionTool(func=emp.get_my_profile),
        FunctionTool(func=emp.get_my_personal_details),
        FunctionTool(func=emp.get_my_employment_record),
        FunctionTool(func=emp.get_my_public_profile),

        # Contact Information
        FunctionTool(func=emp.get_my_email_addresses),
        FunctionTool(func=emp.get_my_phone_numbers),
        FunctionTool(func=emp.get_my_home_address),
        FunctionTool(func=emp.get_my_emergency_contacts),

        # Government IDs & Global Assignments
        FunctionTool(func=emp.get_my_national_ids),
        FunctionTool(func=emp.get_my_global_assignments),

        # Org Chart
        FunctionTool(func=emp.get_my_manager),
        FunctionTool(func=emp.get_my_direct_reports),
    ],
)
