# Pharmacy Management System

Odoo 18 Training Project

# Commit & Branch Convention

## Format
```
<dev>/<prefix>(<scope>): <description>
```
```
john/feat(pos): add dynamic button grid
sara/fix(auth): resolve token expiry
```

---

## Developer Nicknames
| Developer     | Prefix  |
|---------------|---------|
| John Smith    | `john`  |
| Sara Ali      | `sara`  |
| Mohamed Khaled| `mk`    |
> Add your entry here when onboarding.

---

## Allowed Prefixes
| Prefix     | Use For                        |
|------------|--------------------------------|
| `feat`     | New feature                    |
| `fix`      | Bug fix                        |
| `hotfix`   | Critical production patch      |
| `refactor` | Code restructure, no logic change |
| `chore`    | CI, deps, config               |
| `docs`     | Documentation only             |
| `test`     | Tests only                     |

---

## Branch Naming
```
<dev>/<prefix>/<TICKET-ID>-<description>
john/feat/POS-142-button-grid
sara/fix/AUTH-89-token-expiry
```
Nice—this is where your project really starts to look like a real system 🔥
I’ll give you the key system diagrams for your Pharmacy Management System in a clean, structured way so you can reuse them in documentation or implementation.

Alright—here’s your final, clean rubric in ONE table (ready to paste into Word, Excel, or PDF) 👇

⸻

📊 Pharmacy Management System — Final Rubric (Single Table)

Category	Criteria	Weight	Excellent (4)	Good (3)	Fair (2)	Poor (1)
Functional Requirements	Medicine Registration	8%	Complete fields + strong validation	Minor missing fields	Basic fields only	Not working
	Prescription Workflow	8%	Full flow (Draft → Confirmed → Delivered)	Minor issues	Partial flow	Not implemented
	Stock Monitoring	8%	Real-time + filters + highlighting	Limited filters	Basic tracking	No tracking
	Role-Based Access	8%	Fully enforced roles	Minor issues	Weak enforcement	No roles
	Reporting & Export	8%	Full Excel export + filters	Limited export	Basic export	Not implemented
System Logic & Validation	Data Validation	7%	All validations with clear errors	Most validations	Some missing	No validation
	Automation	7%	Fully automated (price, totals, refs)	Mostly automated	Limited automation	Manual
	Error Handling	6%	Clear & user-friendly	Some unclear	Basic handling	None
User Interface & Usability	Ease of Use	5%	Very intuitive	Mostly easy	Some confusion	Difficult
	Visual Feedback	5%	Clear highlights & states	Some feedback	Minimal	None
	Navigation	5%	Well-structured	Minor issues	Confusing	Poor
Output & Documents	PDF Receipt	5%	Professional + complete	Minor missing info	Basic	Not implemented
	Excel Report Format	5%	Clean + structured	Minor issues	Basic	Poor
Automation & Notifications	Expiry Alerts	5%	Auto daily alerts (30d + expired)	Limited alerts	Manual	None
	Scheduled Automation	5%	Fully automated jobs	Mostly working	Partial	None
Technical Quality	Code Structure	3%	Clean & modular	Mostly clean	Some issues	Messy
	Maintainability	2%	Easy to extend	Minor issues	Hard to modify	Not maintainable


⸻

🧮 Final Scoring
	•	Each criterion scored from 1 → 4
	•	Final Score = Σ (Score × Weight)
	•	Total = 100%

⸻

🏆 Grade Scale

Score	Grade
90–100%	ممتاز (Excellent)
75–89%	جيد جداً (Very Good)
60–74%	جيد (Good)
50–59%	مقبول (Pass)
<50%	ضعيف (Fail)

⸻

🧩 1. High-Level System Diagram (Architecture)

+-------------------+
|     Users         |
|-------------------|
| Pharmacist (Ahmed)|
| Manager (Sara)    |
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
| Medicines                |
| Prescriptions            |
| Users                    |
| Stock                    |
| Logs                     |
+---------------------------+


⸻

🔄 2. Use Case Diagram

        +------------------+
        |    Pharmacist    |
        +------------------+
          |   |   |   |   |
          |   |   |   |   +--> Print Receipt
          |   |   |   +------> Monitor Stock
          |   |   +----------> Create Prescription
          |   +--------------> Register Medicine
          +------------------> Receive Notifications


        +------------------+
        |     Manager      |
        +------------------+
          |   |   |
          |   |   +--> Export Reports
          |   +------> View All Data
          +----------> Manage Users


        +------------------+
        |     Cashier      |
        +------------------+
                 |
                 +--> View Data Only


⸻

🔁 3. Prescription Workflow (Activity Diagram)

[Start]
   |
   v
Create Prescription (Draft)
   |
   v
Add Patient + Medicines
   |
   v
[Validation Check]
   |---- No --> Show Error
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


⸻

🧱 4. Entity-Relationship Diagram (ERD)

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
                       |
              +--------v---------+
              | PrescriptionLine|
              |-----------------|
              | id              |
              | prescription_id|
              | medicine_id    |
              | quantity       |
              | price          |
              | subtotal       |
              +----------------+

+----------------+
|     User       |
|----------------|
| id             |
| name           |
| role           |
+----------------+


⸻

🔐 5. Role-Based Access Diagram

            +-------------------+
            |      Manager      |
            +-------------------+
            | Full Access       |
            | View All Data     |
            | Export Reports    |
            +---------+---------+
                      |
                      v
            +-------------------+
            |    Pharmacist     |
            +-------------------+
            | Manage Medicines  |
            | Manage Own Rx     |
            | No Financial Data |
            +---------+---------+
                      |
                      v
            +-------------------+
            |     Cashier       |
            +-------------------+
            | View Only         |
            +-------------------+


⸻

🔔 6. Expiry Notification Flow

[Daily Scheduler Trigger]
          |
          v
Check All Medicines
          |
          v
Is Expiry < 30 Days?
     | Yes
     v
Create Warning Notification
     
Is Expired?
     | Yes
     v
Create Urgent Alert

          |
          v
Display in:
- Medicine Record
- User Notification Panel

⸻


📁 Basic GitHub File Structure

pharmacy-management-system/
│
├── README.md
├── LICENSE
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
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── medicine.py
│       │   ├── prescription.py
│       │   ├── prescription_line.py
│       │   └── stock.py
│       │
│       ├── views/
│       │   ├── medicine_views.xml
│       │   ├── prescription_views.xml
│       │   ├── menu.xml
│       │   └── dashboard_views.xml
│       │
│       ├── security/
│       │   ├── ir.model.access.csv
│       │   └── security.xml
│       │
│       ├── data/
│       │   ├── sequence.xml
│       │   ├── scheduled_actions.xml
│       │   └── demo_data.xml
│       │
│       ├── report/
│       │   ├── prescription_report.xml
│       │   └── prescription_template.xml
│       │
│       ├── wizard/
│       │   ├── export_excel_wizard.py
│       │   └── export_excel_view.xml
│       │
│       └── static/
│           └── description/
│               └── icon.png
│
├── tests/
│   ├── test_medicine.py
│   ├── test_prescription.py
│   └── test_stock.py
│
└── scripts/
    ├── setup.sh
    └── run_odoo.sh


⸻

🧠 What Each Part Does (Quick Breakdown)

🔹 Root Files
	•	README.md → Project overview + how to run
	•	.gitignore → Ignore cache, logs, env files
	•	requirements.txt → Python dependencies

⸻

📂 addons/pharmacy_management/ (Core Module)

This is your main Odoo module
	•	models/ → Business logic (medicine, prescription, stock)
	•	views/ → UI (forms, lists, menus)
	•	security/ → Roles (Pharmacist, Manager, Cashier)
	•	data/ → Auto sequences + scheduled jobs (expiry alerts)
	•	report/ → PDF receipt templates
	•	wizard/ → Excel export popup logic
	•	static/ → Images, icons

⸻

📂 docs/
	•	Use cases
	•	Diagrams
	•	Documentation

⸻

📂 tests/
	•	Unit tests for your system (important for real projects)

⸻

📂 scripts/
	•	Quick setup and run scripts

🚀 Pro Tips (this is where most people mess up)
	•	Keep everything modular → don’t dump logic in one file
	•	Separate:
	•	Models (logic)
	•	Views (UI)
	•	Security (permissions)
	•	Always include:
	•	sequence.xml → for prescription IDs (PH/001)
	•	scheduled_actions.xml → for expiry notifications

---

## CI — `.github/workflows/lint-commits.yml`
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

---

## ✅ Valid &nbsp;&nbsp; ❌ Invalid
```bash
✅ git commit -m "john/feat(pos): add button grid"
✅ git commit -m "sara/fix(api): null check on product fetch"
❌ git commit -m "fixed stuff"
❌ git commit -m "feat(pos): missing dev prefix"
```
