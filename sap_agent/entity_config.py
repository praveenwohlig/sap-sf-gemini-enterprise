"""
entity_config.py
══════════════════════════════════════════════════════════════
Central configuration for all SAP SuccessFactors OData entities.

Each entry defines:
  name        — OData entity set name
  result_key  — key used in the returned dict
  filter_by   — "userId" | "personIdExternal" | None (single-record fetch by key)
  select      — list of fields to request ($select)
  top         — max records to fetch (None = single-record mode)
  description — shown in tool docstring
  domain      — "employee_profile" | "payroll_time" | "org_chart"

Add / remove / edit fields here — no other file needs to change.
══════════════════════════════════════════════════════════════
"""

ENTITIES: list[dict] = [

    # ── Employee Profile ──────────────────────────────────────────────────────

    {
        "name": "User",
        "result_key": "profile",
        "filter_by": None,           # single-record fetch: User('{userId}')
        "select": [
            "userId", "username", "firstName", "lastName", "email",
            "title", "department", "location", "gender", "timeZone",
            "defaultLocale", "hireDate", "status", "displayName",
            "defaultFullName", "lastModifiedDateTime",
        ],
        "top": None,
        "description": "Return the employee's SAP SuccessFactors profile (name, email, title, status).",
        "domain": "employee_profile",
        "tool_name": "get_my_profile",
    },

    {
        "name": "PerPersonal",
        "result_key": "personal",
        "filter_by": None,           # single-record fetch by personIdExternal
        "select": [
            "personIdExternal", "firstName", "lastName", "middleName",
            "gender", "nationality", "dateOfBirth", "maritalStatus",
            "nativePreferredLang", "salutation", "lastModifiedDateTime",
        ],
        "top": None,
        "description": "Return the employee's personal info (name, gender, nationality, DOB).",
        "domain": "employee_profile",
        "tool_name": "get_my_personal",
    },

    {
        "name": "EmpEmployment",
        "result_key": "employment",
        "filter_by": None,           # single-record fetch: EmpEmployment('{userId}')
        "select": [
            "userId", "startDate", "endDate", "seniorityDate",
            "isContingentWorker", "employmentId", "assignmentClass",
            "lastModifiedDateTime",
        ],
        "top": None,
        "description": "Return the employee's employment record (start date, seniority, worker type).",
        "domain": "employee_profile",
        "tool_name": "get_my_employment",
    },

    {
        "name": "PerEmail",
        "result_key": "emails",
        "filter_by": "personIdExternal",
        "select": [
            "personIdExternal", "emailType", "emailAddress",
            "isPrimary", "lastModifiedDateTime",
        ],
        "top": 10,
        "description": "Return the employee's email address records (email type, address, primary flag).",
        "domain": "employee_profile",
        "tool_name": "get_my_email",
    },

    {
        "name": "PerPhone",
        "result_key": "phones",
        "filter_by": "personIdExternal",
        "select": [
            "personIdExternal", "phoneType", "phoneNumber",
            "isPrimary", "lastModifiedDateTime",
        ],
        "top": 10,
        "description": "Return the employee's phone number records (phone type, number, primary flag).",
        "domain": "employee_profile",
        "tool_name": "get_my_phone",
    },

    {
        "name": "PerAddressDEFLT",
        "result_key": "addresses",
        "filter_by": "personIdExternal",
        "select": [
            "personIdExternal", "addressType", "address1", "address2",
            "address3", "city", "state", "zipCode", "county",
            "country", "lastModifiedDateTime",
        ],
        "top": 10,
        "description": "Return the employee's home address (street, city, state, zip, country).",
        "domain": "employee_profile",
        "tool_name": "get_my_address",
    },

    {
        "name": "PerEmergencyContacts",
        "result_key": "emergency_contacts",
        "filter_by": "personIdExternal",
        "select": [
            "personIdExternal", "firstName", "lastName",
            "relationship", "phone", "isPrimary", "lastModifiedDateTime",
        ],
        "top": 10,
        "description": "Return the employee's emergency contacts (name, relationship, phone).",
        "domain": "employee_profile",
        "tool_name": "get_my_emergency_contacts",
    },

    {
        "name": "PerNationalId",
        "result_key": "national_ids",
        "filter_by": "personIdExternal",
        "select": [
            "personIdExternal", "country", "nationalId",
            "cardType", "isPrimary", "lastModifiedDateTime",
        ],
        "top": 10,
        "description": "Return the employee's national / government ID records (country, ID number, card type).",
        "domain": "employee_profile",
        "tool_name": "get_my_national_id",
    },

    # ── Job & Org Chart ───────────────────────────────────────────────────────

    {
        "name": "EmpJob",
        "result_key": "job",
        "filter_by": "userId",
        "select": [
            "userId", "jobTitle", "department", "location",
            "startDate", "emplStatus", "position", "jobCode",
            "payGrade", "payGroup", "managerId", "companyId",
            "businessUnit", "division", "costCenter",
            "fullPartTime", "regularTemp",
        ],
        "top": 1,
        "description": "Return the employee's current job info (title, department, pay grade, manager).",
        "domain": "org_chart",
        "tool_name": "get_my_job",
    },

    # ── Payroll / Time ────────────────────────────────────────────────────────

    {
        "name": "EmpCompensation",
        "result_key": "compensation",
        "filter_by": "userId",
        "select": [
            "userId", "startDate", "endDate", "seqNumber",
            "payType", "payGrade", "payGroup", "bonusTarget",
            "benefitsRate", "isEligibleForBenefits", "isEligibleForCar",
            "isHighlyCompensatedEmployee", "event", "eventReason",
            "lastModifiedDateTime",
        ],
        "top": 1,
        "description": "Return the employee's compensation info (pay grade, bonus target, benefits eligibility).",
        "domain": "payroll_time",
        "tool_name": "get_my_compensation",
    },

    {
        "name": "EmpPayCompRecurring",
        "result_key": "pay_components",
        "filter_by": "userId",
        "select": [
            "userId", "startDate", "endDate", "payComponent",
            "payComponentValue", "currency", "frequencyCode",
            "seqNumber", "lastModifiedDateTime",
        ],
        "top": 20,
        "description": "Return the employee's recurring pay components (salary, allowances, currency).",
        "domain": "payroll_time",
        "tool_name": "get_my_pay_components",
    },

    {
        "name": "EmployeeTime",
        "result_key": "time_off",
        "filter_by": "userId",
        "select": [
            "userId", "startDate", "endDate", "timeType",
            "quantityInDays", "quantityInHours", "approvalStatus",
            "deductionQuantity", "comment", "lastModifiedDateTime",
        ],
        "top": 10,
        "description": "Return the employee's time-off / absence records (vacation, sick leave, approval status).",
        "domain": "payroll_time",
        "tool_name": "get_my_time_off",
    },

    {
        "name": "TimeAccount",
        "result_key": "leave_balances",
        "filter_by": "userId",
        "select": [
            "userId", "timeAccountType", "balance",
            "bookingEndDate", "accountClosed", "lastModifiedDateTime",
        ],
        "top": 20,
        "description": "Return the employee's leave account balances (vacation balance, sick leave balance).",
        "domain": "payroll_time",
        "tool_name": "get_my_leave_balance",
    },

    {
        "name": "EmpBeneficiary",
        "result_key": "beneficiaries",
        "filter_by": "userId",
        "select": [
            "userId", "startDate", "endDate", "benefitType",
            "firstName", "lastName", "relationship",
            "percentage", "lastModifiedDateTime",
        ],
        "top": 20,
        "description": "Return the employee's beneficiary records (benefit type, name, relationship).",
        "domain": "payroll_time",
        "tool_name": "get_my_beneficiaries",
    },

    {
        "name": "EmpGlobalAssignment",
        "result_key": "global_assignments",
        "filter_by": "userId",
        "select": [
            "userId", "startDate", "endDate", "assignmentClass",
            "hostCompany", "hostBusinessUnit", "hostDivision",
            "hostDepartment", "lastModifiedDateTime",
        ],
        "top": 10,
        "description": "Return the employee's global assignment records (host company, dates).",
        "domain": "payroll_time",
        "tool_name": "get_my_global_assignment",
    },
]

# Build a lookup by tool_name for fast access
ENTITY_BY_TOOL: dict[str, dict] = {e["tool_name"]: e for e in ENTITIES}

# Domain groupings (used by agent to build instruction text)
DOMAINS = {
    "employee_profile": "employee profile, personal info, contact details, and IDs",
    "org_chart": "job details, org chart, manager, and direct reports",
    "payroll_time": "compensation, pay components, time off, leave balances, and beneficiaries",
}
