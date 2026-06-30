"""
subagent_time.py
══════════════════════════════════════════════════════════════
Subagent — Time Management & Leave

Handles: absence records, leave balances, timesheets,
         timesheet entries, time valuation results,
         time collectors, clock-in/out recordings,
         allowance recordings, external allowances,
         and external time data.
══════════════════════════════════════════════════════════════
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from tools import tools_payroll_time as pay

time_agent = LlmAgent(
    model="gemini-3.5-flash",
    name="time_agent",
    instruction=(
        "You are an HR data specialist for employee time management and leave. "
        "Answer questions about time-off requests and absences (vacation, sick leave), "
        "leave account balances, weekly/period timesheets (planned vs recorded hours), "
        "daily timesheet entries (clock-in/out, time types), time valuation results "
        "(pay types, allowances), time collector balances (overtime bank, flexi-time), "
        "clock-in/out recordings, allowance recordings (on-call, overtime), "
        "externally imported allowances, and external time data. "
        "Always call the relevant tool first — never guess or fabricate values. "
        "Present dates and durations clearly."
    ),
    tools=[
        # Absence & Leave
        FunctionTool(func=pay.get_my_time_off),
        FunctionTool(func=pay.get_my_leave_balance),

        # Timesheets
        FunctionTool(func=pay.get_my_timesheets),
        FunctionTool(func=pay.get_my_timesheet_entries),
        FunctionTool(func=pay.get_my_time_valuation),

        # Time Collectors & Recordings
        FunctionTool(func=pay.get_my_time_collector),
        FunctionTool(func=pay.get_my_time_recordings),

        # Allowances & External Data
        FunctionTool(func=pay.get_my_allowance_recordings),
        FunctionTool(func=pay.get_my_external_allowances),
        FunctionTool(func=pay.get_my_external_time_data),
    ],
)
