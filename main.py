def calculate_gross_salary(emp, payroll_config):
    """Calculate gross salary from basic pay, allowances, overtime, and incentives."""
    basic = emp["basic_pay"]
    hra = basic * payroll_config["hra_rate"]
    da = basic * payroll_config["da_rate"]
    travel_allowance = payroll_config["travel_allowance"]
    allowances = round(hra + da + travel_allowance, 2)

    # Standard monthly hours assumed as 160 (e.g., 20 days * 8 hours)
    hourly_rate = basic / payroll_config["standard_hours"]
    overtime_pay = round(emp["overtime_hours"] * hourly_rate * payroll_config["overtime_multiplier"], 2)

    # Performance incentive as a percentage of basic pay
    incentive_pay = round(basic * (emp["performance_rating_pct"] / 100.0), 2)

    gross_salary = round(basic + allowances + overtime_pay + incentive_pay, 2)

    earnings = {
        "basic_pay": round(basic, 2),
        "hra": round(hra, 2),
        "da": round(da, 2),
        "travel_allowance": round(travel_allowance, 2),
        "allowances_total": allowances,
        "overtime_pay": overtime_pay,
        "incentive_pay": incentive_pay,
        "gross_salary": gross_salary,
    }
    return earnings


def calculate_progressive_tax(gross_salary, slabs):
    """Apply progressive slab-based deductions on monthly gross salary."""
    tax = 0.0
    previous_limit = 0.0

    for upper_limit, rate in slabs:
        if gross_salary > previous_limit:
            taxable_in_slab = min(gross_salary, upper_limit) - previous_limit
            tax += taxable_in_slab * rate
            previous_limit = upper_limit
        else:
            break

    return round(tax, 2)


def calculate_deductions(emp, gross_salary, payroll_config):
    """Calculate PF, professional tax, and progressive income/payroll deduction."""
    basic = emp["basic_pay"]
    pf = round(min(basic, payroll_config["pf_wage_cap"]) * payroll_config["pf_rate"], 2)

    prof_tax = 0.0
    for min_gross, pt_amount in payroll_config["professional_tax_slabs"]:
        if gross_salary >= min_gross:
            prof_tax = pt_amount

    progressive_deduction = calculate_progressive_tax(gross_salary, payroll_config["progressive_slabs"])
    total_deductions = round(pf + prof_tax + progressive_deduction, 2)
    net_salary = round(gross_salary - total_deductions, 2)

    return {
        "pf": pf,
        "professional_tax": round(prof_tax, 2),
        "progressive_deduction": progressive_deduction,
        "total_deductions": total_deductions,
        "net_salary": net_salary,
    }


def print_salary_statement(emp, earnings, deductions, month_label):
    """Generate a clean formatted salary statement for an employee."""
    print("=" * 62)
    print(f"SALARY STATEMENT - {month_label.upper()}")
    print("=" * 62)
    print(f"Employee ID : {emp['emp_id']:<15} Name : {emp['name']}")
    print(f"Designation : {emp['designation']:<15} Dept : {emp['department']}")
    print("-" * 62)
    print(f"{'EARNINGS':<35} {'AMOUNT (₹)':>25}")
    print("-" * 62)
    print(f"{'Basic Pay':<35} {earnings['basic_pay']:>25.2f}")
    print(f"{'House Rent Allowance (HRA)':<35} {earnings['hra']:>25.2f}")
    print(f"{'Dearness Allowance (DA)':<35} {earnings['da']:>25.2f}")
    print(f"{'Travel Allowance':<35} {earnings['travel_allowance']:>25.2f}")
    print(f"{'Overtime Pay (' + str(emp['overtime_hours']) + ' hrs)':<35} {earnings['overtime_pay']:>25.2f}")
    print(f"{'Performance Incentive':<35} {earnings['incentive_pay']:>25.2f}")
    print("-" * 62)
    print(f"{'GROSS SALARY':<35} {earnings['gross_salary']:>25.2f}")
    print("-" * 62)
    print(f"{'DEDUCTIONS':<35} {'AMOUNT (₹)':>25}")
    print("-" * 62)
    print(f"{'Provident Fund (PF)':<35} {deductions['pf']:>25.2f}")
    print(f"{'Professional Tax':<35} {deductions['professional_tax']:>25.2f}")
    print(f"{'Progressive Tax / Deduction':<35} {deductions['progressive_deduction']:>25.2f}")
    print("-" * 62)
    print(f"{'TOTAL DEDUCTIONS':<35} {deductions['total_deductions']:>25.2f}")
    print(f"{'NET PAYABLE SALARY':<35} {deductions['net_salary']:>25.2f}")
    print("=" * 62 + "\n")


def main():
    payroll_config = {
        "hra
