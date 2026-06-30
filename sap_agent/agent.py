"""
agent.py
══════════════════════════════════════════════════════════════
ADK Agent — SAP SuccessFactors HR Assistant (Sandbox Mode)
Uses SAP API Hub APIKey — no SAML, no GCP credentials needed.

Tool sources:
  tools_employee_profile.py  — profile, contact, IDs, org chart
  tools_payroll_time.py      — job, compensation, time off, leave
══════════════════════════════════════════════════════════════
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from . import tools_employee_profile as emp
from . import tools_payroll_time as pay

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="sap_sf_hr_agent_sandbox",
    instruction=(
        "You are an HR assistant connected to SAP SuccessFactors sandbox. "
        "Use the available tools to answer questions about the employee's "
        "profile, personal info, contact details, national IDs, global assignments, "
        "org chart, job details, compensation, pay components, time off, and leave balances. "
        "This is a sandbox environment with sample data. "
        "Always call the relevant tool before answering — never guess field values."
    ),
    tools=[
        # ── Employee Profile ──────────────────────────────────────────────
        FunctionTool(func=emp.get_my_profile),
        FunctionTool(func=emp.get_my_personal),
        FunctionTool(func=emp.get_my_employment),
        FunctionTool(func=emp.get_my_email),
        FunctionTool(func=emp.get_my_phone),
        FunctionTool(func=emp.get_my_address),
        FunctionTool(func=emp.get_my_emergency_contacts),
        FunctionTool(func=emp.get_my_national_id),
        FunctionTool(func=emp.get_my_global_assignment),
        FunctionTool(func=emp.get_my_manager),
        FunctionTool(func=emp.list_direct_reports),

        # ── Payroll & Time ────────────────────────────────────────────────
        FunctionTool(func=pay.get_my_job),
        FunctionTool(func=pay.get_my_compensation),
        FunctionTool(func=pay.get_my_pay_components),
        FunctionTool(func=pay.get_my_beneficiaries),
        FunctionTool(func=pay.get_my_time_off),
        FunctionTool(func=pay.get_my_leave_balance),
    ],
)
