"""
subagent_payroll.py
══════════════════════════════════════════════════════════════
Subagent — Payroll & Compensation

Handles: current job details, compensation snapshot,
         recurring pay components, and beneficiaries.
══════════════════════════════════════════════════════════════
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from tools import tools_payroll_time as pay

payroll_agent = LlmAgent(
    model="gemini-3.5-flash",
    name="payroll_agent",
    instruction=(
        "You are an HR data specialist for employee payroll and compensation. "
        "Answer questions about the employee's current job (title, department, "
        "pay grade, pay group, manager, employment status), compensation details "
        "(pay type, bonus target, benefits eligibility), recurring pay components "
        "(base salary, allowances, currency, frequency), and beneficiary records. "
        "Always call the relevant tool first — never guess or fabricate values. "
        "Present salary and pay figures clearly with currency codes."
    ),
    tools=[
        FunctionTool(func=pay.get_my_job),
        FunctionTool(func=pay.get_my_compensation),
        FunctionTool(func=pay.get_my_pay_components),
        FunctionTool(func=pay.get_my_beneficiaries),
    ],
)
