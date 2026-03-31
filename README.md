# 💊 Pharmacy Management System
> Odoo 18 Training Project

---

## 📑 Table of Contents
- [System Diagrams](#-system-diagrams)
- [Project Structure](#-project-structure)
- [Grading Rubric](#-grading-rubric)
- [Commit & Branch Convention](#-commit--branch-convention)

---

## 🧩 System Diagrams

### 1. High-Level Architecture

```
+-------------------+
|       Users       |
|-------------------|
| Pharmacist        |
| Manager           |
| Cashier           |
+---------+---------+
          |
          v
+---------------------------+
|   Pharmacy System (Odoo)  |
|---------------------------|
| - Medicine Module         |
| - Prescription Module     |
| - Inventory Module        |
| - Reporting Module        |
| - User Access Control     |
| - Notification System     |
+-----------+---------------+
            |
            v
+---------------------------+
|        Database           |
|---------------------------|
| Medicines                 |
| Prescriptions             |
| Users / Stock / Logs      |
+---------------------------+
```

---

### 2. Use Case Diagram

```
+------------------+        +------------------+        +------------------+
|    Pharmacist    |        |     Manager      |        |     Cashier      |
+------------------+        +------------------+        +------------------+
| Register Medicine|        | Export Reports   |        | View Data Only   |
| Create Rx        |        | View All Data    |        +------------------+
| Monitor Stock    |        | Manage Users     |
| Print Receipt    |        +------------------+
| Notifications    |
+------------------+
```

---

### 3. Prescription Workflow

```
[Start]
   |
   v
Create Prescription (Draft)
   |
   v
Add Patient + Medicines
   |
   v
[Validation Check] --No--> Show Error
   |
  Yes
   |
   v
Confirm Prescription
   |
   v
Deliver Medicines
   |
   v
Print Receipt (Optional)
   |
   v
[End]
```

---

### 4. Entity-Relationship Diagram (ERD)

```
+----------------+       +--------------------+
|   Medicine     |       |   Prescription     |
|----------------|       |--------------------|
| id             |<----+ | id                 |
| name           |     | | reference          |
| category       |     | | patient_name       |
| expiry_date    |     | | doctor_name        |
| stock_qty      |     | | state              |
| min_stock      |     | | total_amount       |
| price          |     | +--------------------+
+----------------+     |
                        |
               +--------v---------+
               | PrescriptionLine |
               |-----------------|
               | id               |
               | prescription_id  |
               | medicine_id      |
               | quantity         |
               | price / subtotal |
               +-----------------+

+----------------+
|     User       |
|----------------|
| id / name      |
| role           |
+----------------+
```

---

### 5. Role-Based Access

```
+-------------------+
|      Manager      |  Full Access · Export Reports · Manage Users
+-------------------+
          |
          v
+-------------------+
|    Pharmacist     |  Manage Medicines · Own Prescriptions
+-------------------+
          |
          v
+-------------------+
|     Cashier       |  View Only
+-------------------+
```

---

### 6. Expiry Notification Flow

```
[Daily Scheduler Trigger]
          |
          v
   Check All Medicines
          |
   +------+------+
   |             |
Expiry        Expired
< 30 Days?    Already?
   |             |
Warning       Urgent
Alert         Alert
   |             |
   +------+------+
          |
          v
  Display in Medicine Record
  + User Notification Panel
```

---

## 📁 Project Structure

```
pharmacy-management-system/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── docs/
│   ├── use_cases.md
│   ├── system_diagrams.md
│   └── api_reference.md
│
├── addons/
│   └── pharmacy_management/
│       ├── __init__.py
│       ├── __manifest__.py
│       ├── models/
│       │   ├── medicine.py
│       │   ├── prescription.py
│       │   ├── prescription_line.py
│       │   └── stock.py
│       ├── views/
│       │   ├── medicine_views.xml
│       │   ├── prescription_views.xml
│       │   ├── menu.xml
│       │   └── dashboard_views.xml
│       ├── security/
│       │   ├── ir.model.access.csv
│       │   └── security.xml
│       ├── data/
│       │   ├── sequence.xml
│       │   ├── scheduled_actions.xml
│       │   └── demo_data.xml
│       ├── report/
│       │   ├── prescription_report.xml
│       │   └── prescription_template.xml
│       ├── wizard/
│       │   ├── export_excel_wizard.py
│       │   └── export_excel_view.xml
│       └── static/description/
│           └── icon.png
│
├── tests/
│   ├── test_medicine.py
│   ├── test_prescription.py
│   └── test_stock.py
│
└── scripts/
    ├── setup.sh
    └── run_odoo.sh
```

---

## 📊 Grading Rubric

| Category | Criteria | Weight | Excellent (4) | Good (3) | Fair (2) | Poor (1) |
|---|---|---|---|---|---|---|
| **Functional** | Medicine Registration | 8% | Complete fields + validation | Minor missing fields | Basic fields only | Not working |
| | Prescription Workflow | 8% | Full flow Draft→Confirmed→Delivered | Minor issues | Partial flow | Not implemented |
| | Stock Monitoring | 8% | Real-time + filters + highlighting | Limited filters | Basic tracking | No tracking |
| | Role-Based Access | 8% | Fully enforced roles | Minor issues | Weak enforcement | No roles |
| | Reporting & Export | 8% | Full Excel export + filters | Limited export | Basic export | Not implemented |
| **Validation** | Data Validation | 7% | All validations with clear errors | Most validations | Some missing | No validation |
| | Automation | 7% | Fully automated (price, totals, refs) | Mostly automated | Limited | Manual |
| | Error Handling | 6% | Clear & user-friendly | Some unclear | Basic | None |
| **UI/UX** | Ease of Use | 5% | Very intuitive | Mostly easy | Some confusion | Difficult |
| | Visual Feedback | 5% | Clear highlights & states | Some feedback | Minimal | None |
| | Navigation | 5% | Well-structured | Minor issues | Confusing | Poor |
| **Output** | PDF Receipt | 5% | Professional + complete | Minor missing info | Basic | Not implemented |
| | Excel Report | 5% | Clean + structured | Minor issues | Basic | Poor |
| **Automation** | Expiry Alerts | 5% | Auto daily alerts (30d + expired) | Limited alerts | Manual | None |
| | Scheduled Jobs | 5% | Fully automated | Mostly working | Partial | None |
| **Technical** | Code Structure | 3% | Clean & modular | Mostly clean | Some issues | Messy |
| | Maintainability | 2% | Easy to extend | Minor issues | Hard to modify | Not maintainable |

### 🏆 Grade Scale

| Score | Grade |
|---|---|
| 90–100% | ممتاز — Excellent |
| 75–89% | جيد جداً — Very Good |
| 60–74% | جيد — Good |
| 50–59% | مقبول — Pass |
| < 50% | ضعيف — Fail |

> **Final Score** = Σ (Criterion Score × Weight) across all 17 criteria.

---

## 🔖 Commit & Branch Convention

### Format
```
<dev>/<prefix>(<scope>): <description>
```

```bash
john/feat(pos): add dynamic button grid
sara/fix(auth): resolve token expiry
```

### Developer Nicknames

| Developer      | Prefix |
|----------------|--------|
| John Smith     | `john` |
| Sara Ali       | `sara` |
| Mohamed Khaled | `mk`   |

> Add your entry here when onboarding.

### Allowed Prefixes

| Prefix     | Use For                           |
|------------|-----------------------------------|
| `feat`     | New feature                       |
| `fix`      | Bug fix                           |
| `hotfix`   | Critical production patch         |
| `refactor` | Code restructure, no logic change |
| `chore`    | CI, deps, config                  |
| `docs`     | Documentation only                |
| `test`     | Tests only                        |

### Branch Naming
```
<dev>/<prefix>/<TICKET-ID>-<description>

john/feat/POS-142-button-grid
sara/fix/AUTH-89-token-expiry
```

### CI — `.github/workflows/lint-commits.yml`

```yaml
name: Lint Commits
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: npm i -D @commitlint/cli
      - run: npx commitlint --from=HEAD~1 --to=HEAD
```

### ✅ Valid — ❌ Invalid

```bash
# Valid
git commit -m "john/feat(pos): add button grid"
git commit -m "sara/fix(api): null check on product fetch"

# Invalid
git commit -m "fixed stuff"
git commit -m "feat(pos): missing dev prefix"
```