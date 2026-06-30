"""
tools_compensation.py
══════════════════════════════════════════════════════════════
ADK Tools — Compensation domain

Entities covered:
  DeductionScreenId                 get_deduction_screen_ids()
  OneTimeDeduction                  get_my_one_time_deductions()
  RecurringDeduction                get_my_recurring_deductions()
  RecurringDeductionItem            get_my_recurring_deduction_items()
  EmpCompensation                   get_my_compensation()
  EmpCompensationCalculated         get_my_compensation_calculated()
  EmpCompensationGroupSumCalculated get_my_compensation_group_sum()
  EmpPayCompNonRecurring            get_my_pay_components_non_recurring()
  EmpPayCompRecurring               get_my_pay_components_recurring()

Field lists and filter patterns follow the ECCompensation OData spec.
══════════════════════════════════════════════════════════════
"""

from ..sap_sf_config import sf_client


# ── DeductionScreenId ─────────────────────────────────────────────────────────

def get_deduction_screen_ids() -> dict:
    """Return all deduction screen IDs used for configuring the Deduction UI in Employee Central."""
    data = sf_client.odata_get(
        entity="DeductionScreenId",
        top=50,
    )
    return {"deduction_screen_ids": data}


# ── OneTimeDeduction ──────────────────────────────────────────────────────────

def get_my_one_time_deductions(user_id: str = None) -> dict:
    """Return the employee's non-recurring (one-time) deduction records.

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    uid = user_id or sf_client.USER_ID
    data = sf_client.odata_get(
        entity="OneTimeDeduction",
        filter=f"userSysId eq '{uid}'",
        top=20,
    )
    return {"one_time_deductions": data}


# ── RecurringDeduction ────────────────────────────────────────────────────────

def get_my_recurring_deductions(user_id: str = None) -> dict:
    """Return the employee's recurring deduction records, including individual deduction items.

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    uid = user_id or sf_client.USER_ID
    data = sf_client.odata_get(
        entity="RecurringDeduction",
        filter=f"userSysId eq '{uid}'",
        expand="recurringItems",
        top=20,
    )
    return {"recurring_deductions": data}


# ── RecurringDeductionItem ────────────────────────────────────────────────────

def get_my_recurring_deduction_items(user_id: str = None) -> dict:
    """Return the employee's individual recurring deduction line items.

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    uid = user_id or sf_client.USER_ID
    data = sf_client.odata_get(
        entity="RecurringDeductionItem",
        filter=f"RecurringDeduction_userSysId eq '{uid}'",
        top=20,
    )
    return {"recurring_deduction_items": data}


# ── EmpCompensation ───────────────────────────────────────────────────────────

def get_my_compensation(
    user_id: str = None,
    from_date: str = None,
    to_date: str = None,
) -> dict:
    """Return the employee's compensation information (pay grade, bonus target, benefits eligibility).

    Args:
        user_id:   Employee user ID to look up. Defaults to the logged-in user.
        from_date: Start of effective date range in YYYY-MM-DD format (optional).
        to_date:   End of effective date range in YYYY-MM-DD format (optional).
    """
    uid = user_id or sf_client.USER_ID
    data = sf_client.odata_get(
        entity="EmpCompensation",
        filter=f"userId eq '{uid}' and effectiveLatestChange eq true",
        from_date=from_date,
        to_date=to_date,
        top=10,
    )
    return {"compensation": data}


# ── EmpCompensationCalculated ─────────────────────────────────────────────────

def get_my_compensation_calculated(user_id: str = None) -> dict:
    """Return the employee's calculated compensation values (Compa-Ratio, Range Penetration).

    Args:
        user_id: Employee user ID to look up. Defaults to the logged-in user.
    """
    uid = user_id or sf_client.USER_ID
    data = sf_client.odata_get(
        entity="EmpCompensation",
        filter=f"userId eq '{uid}'",
        expand="empCompensationCalculatedNav",
        top=1,
    )
    return {"compensation_calculated": data}


# ── EmpCompensationGroupSumCalculated ─────────────────────────────────────────

def get_my_compensation_group_sum(
    user_id: str = None,
    start_date: str = None,
) -> dict:
    """Return the employee's calculated pay component group sums from compensation information.

    Args:
        user_id:    Employee user ID to look up. Defaults to the logged-in user.
        start_date: Effective start date of the compensation record in YYYY-MM-DD format (optional).
    """
    uid = user_id or sf_client.USER_ID
    filter_expr = f"userId eq '{uid}'"
    if start_date:
        filter_expr += f" and startDate eq datetime'{start_date}T00:00:00'"

    data = sf_client.odata_get(
        entity="EmpCompensation",
        filter=filter_expr,
        expand="empCompensationGroupSumCalculatedNav",
        top=1,
    )
    return {"compensation_group_sum": data}


# ── EmpPayCompNonRecurring ────────────────────────────────────────────────────

def get_my_pay_components_non_recurring(
    user_id: str = None,
    pay_component_code: str = None,
) -> dict:
    """Return the employee's non-recurring (one-time) pay component records (bonuses, spot awards).

    Args:
        user_id:            Employee user ID to look up. Defaults to the logged-in user.
        pay_component_code: Filter by a specific pay component code (optional).
    """
    uid = user_id or sf_client.USER_ID
    filter_expr = f"userId eq '{uid}'"
    if pay_component_code:
        filter_expr += f" and payComponentCode eq '{pay_component_code}'"

    data = sf_client.odata_get(
        entity="EmpPayCompNonRecurring",
        filter=filter_expr,
        top=20,
    )
    return {"pay_components_non_recurring": data}


# ── EmpPayCompRecurring ───────────────────────────────────────────────────────

def get_my_pay_components_recurring(
    user_id: str = None,
    from_date: str = None,
    to_date: str = None,
    pay_component: str = None,
) -> dict:
    """Return the employee's recurring pay component records (base salary, allowances).

    Args:
        user_id:       Employee user ID to look up. Defaults to the logged-in user.
        from_date:     Start of effective date range in YYYY-MM-DD format (optional).
        to_date:       End of effective date range in YYYY-MM-DD format (optional).
        pay_component: Filter by a specific pay component, e.g. 'Base Salary' (optional).
    """
    uid = user_id or sf_client.USER_ID
    filter_expr = f"userId eq '{uid}' and effectiveLatestChange eq true"
    if pay_component:
        filter_expr += f" and payComponent eq '{pay_component}'"

    data = sf_client.odata_get(
        entity="EmpPayCompRecurring",
        filter=filter_expr,
        from_date=from_date,
        to_date=to_date,
        top=20,
    )
    return {"pay_components_recurring": data}
