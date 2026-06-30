"""
agent.py
══════════════════════════════════════════════════════════════
Root Orchestrator — SAP SuccessFactors HR Assistant

Routes incoming questions to the correct domain subagent:

  identity_agent  — profile, contact, IDs, org chart
  career_agent    — education, work history, skills, awards
  payroll_agent   — job info, compensation, pay components
  time_agent      — timesheets, leave, recordings, allowances

The orchestrator never calls SAP APIs directly.
It analyses the intent and delegates to the right specialist.
══════════════════════════════════════════════════════════════
"""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from sub_agents.subagent_identity import identity_agent
from sub_agents.subagent_career import career_agent
from sub_agents.subagent_payroll import payroll_agent
from sub_agents.subagent_time import time_agent

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="sap_sf_hr_orchestrator",
    instruction=(
        "You are the SAP SuccessFactors HR Assistant. "
        "Your role is to understand the employee's question and delegate it "
        "to the correct specialist subagent. Never answer from memory — "
        "always route to a subagent and return its response.\n\n"

        "Routing rules:\n"
        "• identity_agent  → name, profile, personal details, employment record, "
        "contact details (email/phone/address), emergency contacts, national IDs, "
        "global assignments, public bio, who is my manager, direct reports, org chart\n"

        "• career_agent    → education, university, degree, certifications, licences, "
        "languages, previous employers, work history, internal job history, "
        "special projects, training courses, skills, expertise, leadership, "
        "awards, badges, recognition, memberships, community\n"

        "• payroll_agent   → salary, pay grade, compensation, pay components, "
        "bonus, benefits eligibility, job title, department, pay group, beneficiaries\n"

        "• time_agent      → leave balance, vacation, sick leave, time off, "
        "timesheet, clock-in, clock-out, recorded hours, planned hours, "
        "overtime, flexi-time, time collector, allowance, external time data\n\n"

        "If a question spans multiple domains (e.g. 'give me my full profile'), "
        "call the relevant subagents sequentially and combine the results into "
        "a single, well-structured response. "
        "Be concise, factual, and always label the data clearly."
    ),
    tools=[
        AgentTool(agent=identity_agent),
        AgentTool(agent=career_agent),
        AgentTool(agent=payroll_agent),
        AgentTool(agent=time_agent),
        AgentTool(agent=employee_info_agent),
    ],
)
