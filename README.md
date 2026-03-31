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

------

# 🏥 نظام إدارة الصيدلية — Pharmacy Management System

> نظام متكامل لإدارة الصيدليات يشمل إدارة الأدوية، الروشتات، المخزون، والمبيعات.  
> A full-featured pharmacy management system covering medicines, prescriptions, inventory, and sales.

---

## 📋 فهرس المحتويات / Table of Contents

- [نظرة عامة / Overview](#-نظرة-عامة--overview)
- [المميزات / Features](#-المميزات--features)
- [المتطلبات / Requirements](#-المتطلبات--requirements)
- [التثبيت / Installation](#-التثبيت--installation)
- [هيكل المشروع / Project Structure](#-هيكل-المشروع--project-structure)
- [الصلاحيات / Roles & Permissions](#-الصلاحيات--roles--permissions)
- [معيار التقييم / Evaluation Rubric](#-معيار-التقييم--evaluation-rubric)
- [المساهمة / Contributing](#-المساهمة--contributing)

---

## 🌐 نظرة عامة / Overview

نظام إدارة صيدلية مبني على **Python Odoo** يوفر:

- ✅ إدارة كاملة للأدوية والمخزون
- ✅ إنشاء وطباعة الروشتات الطبية
- ✅ نظام صلاحيات متعدد المستويات
- ✅ تقارير وتصدير Excel / PDF
- ✅ تنبيهات انتهاء الصلاحية التلقائية

Built on **Python Odoo**, providing full medicine management, prescription handling, role-based access control, reporting, and automated expiry alerts.

---

## ✨ المميزات / Features

| الميزة | الوصف |
|---|---|
| 💊 **إدارة الأدوية** | تسجيل، تعديل، وحذف الأدوية بجميع بياناتها |
| 📝 **الروشتات الطبية** | إنشاء روشتات متعددة الأدوية مع بيانات المريض |
| 📦 **إدارة المخزون** | متابعة الكميات مع تنبيهات الحد الأدنى |
| 🔐 **نظام الصلاحيات** | ثلاثة مستويات: مدير / صيدلي / كاشير |
| 📊 **التقارير** | تصدير Excel وطباعة PDF |
| 🔔 **التنبيهات التلقائية** | فحص يومي لانتهاء صلاحية الأدوية |
| 🧮 **الحسابات التلقائية** | أسعار، خصومات، وضرائب محسوبة تلقائياً |

---

## ⚙️ المتطلبات / Requirements

```txt
Python        >= 3.10
Odoo          >= 16.0
PostgreSQL    >= 14
Node.js       >= 18.x   (for frontend assets)
```

### Python Dependencies

```txt
odoo-addon-account
odoo-addon-stock
xlsxwriter >= 3.0.0
reportlab  >= 4.0.0
```

---

## 🚀 التثبيت / Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/pharmacy-management.git
cd pharmacy-management

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # Linux / macOS
# venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add module to Odoo addons path
# In odoo.conf:
# addons_path = /path/to/your/addons,/path/to/pharmacy-management

# 5. Initialize the database
python odoo-bin -d pharmacy_db -i pharmacy_management --stop-after-init

# 6. Run the server
python odoo-bin -d pharmacy_db
```

---

## 🗂️ هيكل المشروع / Project Structure

```
pharmacy_management/
│
├── 📁 models/
│   ├── medicine.py           # Medicine model & inventory logic
│   ├── prescription.py       # Prescription model
│   ├── sale_order.py         # Sales & billing
│   └── stock_alert.py        # Expiry & stock alerts
│
├── 📁 views/
│   ├── medicine_views.xml    # Medicine UI forms & lists
│   ├── prescription_views.xml
│   ├── dashboard_views.xml
│   └── report_templates.xml  # PDF invoice templates
│
├── 📁 wizards/
│   ├── export_excel.py       # Excel export logic
│   └── stock_report.py       # Stock reporting wizard
│
├── 📁 security/
│   ├── ir.model.access.csv   # Model-level permissions
│   └── pharmacy_security.xml # Role definitions
│
├── 📁 data/
│   └── scheduled_actions.xml # Daily cron jobs
│
├── 📁 static/
│   └── src/
│       ├── css/              # Custom styles
│       └── js/               # POS button grid & UI logic
│
├── __manifest__.py
└── README.md
```

---

## 🔐 الصلاحيات / Roles & Permissions

| الصلاحية | مدير | صيدلي | كاشير |
|---|:---:|:---:|:---:|
| إدارة الأدوية | ✅ | ✅ | ❌ |
| إنشاء الروشتات | ✅ | ✅ | ❌ |
| عمليات البيع | ✅ | ❌ | ✅ |
| إدارة المخزون | ✅ | ✅ | ❌ |
| التقارير والتصدير | ✅ | ❌ | ❌ |
| إدارة المستخدمين | ✅ | ❌ | ❌ |

---

## 📊 معيار التقييم / Evaluation Rubric

يُستخدم هذا المعيار لتقييم جودة تسليم المشروع من 100 درجة.  
This rubric is used to evaluate project deliverables out of 100.

---

### 1️⃣ الوظائف الأساسية — `/ 20`

#### 💊 تسجيل الأدوية
- [ ] يتم حفظ الدواء بجميع بياناته (الاسم، الجرعة، الشركة)
- [ ] لا يقبل النظام إدخال بيانات ناقصة
- [ ] يظهر الدواء بشكل صحيح بعد الحفظ
- [ ] يمكن تعديله أو حذفه بسهولة

`__ / 4`

#### 📝 إنشاء الروشتة
- [ ] يمكن إضافة أكثر من دواء في نفس الروشتة
- [ ] تُحفظ بيانات المريض مع الروشتة
- [ ] تظهر الروشتة بشكل منظم وقابل للطباعة
- [ ] يمكن البحث عنها واسترجاعها

`__ / 4`

#### 📦 متابعة المخزون
- [ ] يظهر تحذير عند نقص الكمية
- [ ] يتحدث المخزون تلقائياً عند البيع
- [ ] يمكن عرض تقرير بالأدوية الناقصة
- [ ] يوجد حد أدنى للمخزون قابل للضبط

`__ / 4`

#### 🔐 التحكم في الصلاحيات
- [ ] المدير يملك كامل الصلاحيات
- [ ] الصيدلي يمكنه إنشاء الروشتات فقط
- [ ] الكاشير يمكنه البيع والفواتير فقط
- [ ] لا يستطيع أي مستخدم تجاوز صلاحياته

`__ / 4`

#### 📤 التصدير إلى Excel
- [ ] يمكن تصدير قائمة الأدوية
- [ ] يمكن تصدير تقارير المبيعات
- [ ] الملف منظم وقابل للقراءة
- [ ] لا يحدث خطأ أثناء التصدير

`__ / 4`

---

### 2️⃣ منطق النظام — `/ 12`

#### ✔️ التحقق من صحة البيانات
- [ ] لا يقبل تاريخ انتهاء صلاحية في الماضي
- [ ] لا يقبل أرقامًا سالبة في الكميات أو الأسعار
- [ ] يظهر رسالة خطأ واضحة عند الإدخال الخاطئ
- [ ] يمنع الحفظ حتى تُصحَّح الأخطاء

`__ / 4`

#### 🧮 الحساب التلقائي
- [ ] يحسب السعر الإجمالي تلقائياً
- [ ] يحسب الخصم إن وُجد
- [ ] يحسب الضريبة إن وُجدت
- [ ] النتيجة دقيقة دون أخطاء حسابية

`__ / 4`

#### 🚨 التعامل مع الأخطاء
- [ ] لا يتعطل النظام عند إدخال بيانات خاطئة
- [ ] تظهر رسائل خطأ مفهومة للمستخدم
- [ ] يمكن التراجع عن العملية عند الخطأ
- [ ] يتم تسجيل الأخطاء في سجل (log)

`__ / 4`

---

### 3️⃣ سهولة الاستخدام — `/ 12`

#### 🧭 سهولة التعامل مع النظام
- [ ] يمكن إتمام المهام الأساسية بخطوات قليلة
- [ ] لا يحتاج المستخدم لتدريب مطوّل
- [ ] التنقل بين الصفحات سلس وسريع
- [ ] يعمل بشكل صحيح على الشاشات المختلفة

`__ / 4`

#### 🎨 وضوح الألوان والتنبيهات
- [ ] الألوان تعكس حالة البيانات (أحمر / أخضر / برتقالي)
- [ ] التنبيهات واضحة ومميزة
- [ ] لا يوجد ازدحام بصري في الواجهة
- [ ] الخطوط مقروءة وبحجم مناسب

`__ / 4`

#### 📂 تنظيم القوائم
- [ ] القوائم مرتبة بشكل منطقي
- [ ] يوجد بحث وفلترة في القوائم الطويلة
- [ ] يمكن الوصول لأي قسم بسرعة
- [ ] لا توجد قوائم مكررة أو غير ضرورية

`__ / 4`

---

### 4️⃣ المخرجات — `/ 8`

#### 🖨️ طباعة فاتورة PDF
- [ ] الفاتورة تحتوي على جميع البيانات المطلوبة
- [ ] التنسيق واضح ومرتب
- [ ] يمكن طباعتها مباشرة أو حفظها
- [ ] تحتوي على شعار / بيانات الصيدلية

`__ / 4`

#### 📊 شكل ملف Excel
- [ ] العناوين واضحة في الصف الأول
- [ ] البيانات في الأعمدة الصحيحة
- [ ] لا توجد خلايا مدمجة تعيق الفلترة
- [ ] الأرقام بصيغة رقمية وليست نصية

`__ / 4`

---

### 5️⃣ التنبيهات — `/ 8`

#### ⏰ تنبيه انتهاء صلاحية الأدوية
- [ ] يظهر تنبيه قبل انتهاء الصلاحية بفترة كافية
- [ ] يحدد اسم الدواء وتاريخ انتهاء صلاحيته
- [ ] يمكن ضبط مدة التنبيه المسبق
- [ ] يُسجَّل التنبيه في قائمة التنبيهات

`__ / 4`

#### 🤖 التشغيل التلقائي
- [ ] يعمل الفحص اليومي تلقائياً دون تدخل
- [ ] يُرسَل إشعار للمسؤول عند اكتشاف مشكلة
- [ ] لا يتوقف عند إغلاق المتصفح
- [ ] يمكن الاطلاع على آخر وقت تشغيل

`__ / 4`

---

### 6️⃣ الجودة التقنية — `/ 8`

#### 🗂️ تنظيم الكود
- [ ] الكود مقسم إلى ملفات / وحدات منفصلة
- [ ] الأسماء واضحة وتعبيرية
- [ ] لا يوجد كود مكرر (DRY Principle)
- [ ] يوجد تعليقات توضيحية في الأجزاء المعقدة

`__ / 4`

#### 🔧 سهولة التعديل
- [ ] يمكن إضافة ميزة جديدة دون كسر القديمة
- [ ] الإعدادات منفصلة عن منطق الكود
- [ ] يمكن فهم الكود من شخص آخر بسهولة
- [ ] لا توجد تبعيات معقدة بين المكونات

`__ / 4`

---

### 🧮 الدرجة الإجمالية / Final Score

| الفئة | الدرجة |
|---|---|
| الوظائف الأساسية | `__ / 20` |
| منطق النظام | `__ / 12` |
| سهولة الاستخدام | `__ / 12` |
| المخرجات | `__ / 8` |
| التنبيهات | `__ / 8` |
| الجودة التقنية | `__ / 8` |
| **المجموع** | **`__ / 68`** |

> **لتحويل الدرجة إلى 100:**  
> `النتيجة النهائية = (مجموعك ÷ 68) × 100`

---

### 🏆 سلّم التقدير / Grading Scale

| النتيجة | التقدير |
|:---:|---|
| 90 – 100 | ⭐ ممتاز / Excellent |
| 75 – 89 | ✅ جيد جداً / Very Good |
| 60 – 74 | 👍 جيد / Good |
| 50 – 59 | ⚠️ مقبول / Acceptable |
| < 50 | ❌ ضعيف / Poor |

---

## 🤝 المساهمة / Contributing

```bash
# 1. Fork the project
# 2. Create your feature branch
git checkout -b feature/AmazingFeature

# 3. Commit your changes
git commit -m 'feat: add AmazingFeature'

# 4. Push to the branch
git push origin feature/AmazingFeature

# 5. Open a Pull Request
```

### Commit Convention

```
feat:     ميزة جديدة / New feature
fix:      إصلاح خطأ / Bug fix
docs:     توثيق / Documentation
refactor: إعادة هيكلة / Refactoring
test:     اختبارات / Tests
```

---

## 📄 الترخيص / License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">

Made with ❤️ for better pharmacy management  
صُنع بـ ❤️ لإدارة صيدلية أفضل

</div>

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