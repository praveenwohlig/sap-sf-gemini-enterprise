"""
subagent_compensation.py
══════════════════════════════════════════════════════════════
Subagent — Compensation

Handles: deduction screen IDs, one-time deductions,
         recurring deductions and items, compensation info,
         calculated compensation values, non-recurring and
         recurring pay components.
══════════════════════════════════════════════════════════════
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from tools import tools_compensation as comp

compensation_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="compensation_agent",
    instruction=(
        "You are an HR data specialist for employee compensation. "
        "Answer questions about the employee's compensation details, "
        "pay grades, bonus targets, benefits eligibility, one-time and "
        "recurring deductions, non-recurring pay components (bonuses, spot awards), "
        "and recurring pay components (base salary, allowances). "
        "For effective-dated entities, always use the latest effective record. "
        "Always call the relevant tool first — never guess or fabricate values. "
        "Present monetary values with their currency codes clearly."
    ),
    tools=[
        # Deduction Configuration
        FunctionTool(func=comp.get_deduction_screen_ids),

        # Deductions
        FunctionTool(func=comp.get_my_one_time_deductions),
        FunctionTool(func=comp.get_my_recurring_deductions),
        FunctionTool(func=comp.get_my_recurring_deduction_items),

        # Compensation Info
        FunctionTool(func=comp.get_my_compensation),
        FunctionTool(func=comp.get_my_compensation_calculated),
        FunctionTool(func=comp.get_my_compensation_group_sum),

        # Pay Components
        FunctionTool(func=comp.get_my_pay_components_non_recurring),
        FunctionTool(func=comp.get_my_pay_components_recurring),
    ],
)
