# 🚀 Moments That Matter — Copilot Command Centre

## Full Build Guide

Aşağıda projenin tamamını, dosya dosya, modül modül inşa ediyorum. Bu proje GitHub'a atılacak, Streamlit ile canlı çalışacak ve RACV hiring manager'ına "bu adam bizim işimizi zaten yapmış" dedirtecek şekilde tasarlandı.

---

## Proje yapısı

```
moments-that-matter/
│
├── README.md
├── requirements.txt
├── .env.example
├── config.py
│
├── app.py                          # Ana Streamlit uygulaması
│
├── pages/
│   ├── 1_🏠_Dashboard.py
│   ├── 2_🤖_Copilot_Agents.py
│   ├── 3_🧪_Experiment_Registry.py
│   ├── 4_📊_ROI_Calculator.py
│   ├── 5_📚_Prompt_Library.py
│   ├── 6_🛡️_Governance.py
│   └── 7_🎓_Training_Hub.py
│
├── data/
│   ├── experiments.json
│   ├── prompts.json
│   ├── risk_assessments.json
│   ├── kpi_metrics.json
│   └── training_modules.json
│
├── agents/
│   ├── member_context_agent.py
│   ├── policy_navigator_agent.py
│   ├── next_best_action_agent.py
│   ├── communication_drafter_agent.py
│   └── prompt_coach_agent.py
│
├── governance/
│   ├── risk_matrix.py
│   ├── compliance_checker.py
│   └── audit_logger.py
│
├── utils/
│   ├── data_loader.py
│   ├── metrics.py
│   ├── charts.py
│   └── openai_client.py
│
└── assets/
    ├── racv_style.css
    └── logo.png
```

---

## 1. Requirements & Configuration

### `requirements.txt`

```text
streamlit==1.41.1
openai==1.58.1
pandas==2.2.3
plotly==5.24.1
python-dotenv==1.0.1
pydantic==2.10.3
streamlit-option-menu==0.4.0
streamlit-extras==0.5.0
datetime
uuid
json
```

### `.env.example`

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
ORGANIZATION_NAME=RACV
```

### `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    ORG_NAME = os.getenv("ORGANIZATION_NAME", "RACV")

    # Departmanlar — RACV'nin gerçek yapısına uygun
    DEPARTMENTS = [
        "Roadside Assistance",
        "Insurance & Claims",
        "Member Contact Centre",
        "Home Services",
        "Energy Services",
        "Travel Services",
        "Corporate Services",
    ]

    # Experiment durumları
    EXPERIMENT_STAGES = ["Pipeline", "In-Flight", "Completed", "Scaled", "Stopped"]

    # Risk seviyeleri
    RISK_LEVELS = ["Low", "Medium", "High", "Critical"]

    # KPI kategorileri
    KPI_CATEGORIES = [
        "Average Handling Time",
        "First Contact Resolution",
        "After-Call Work Duration",
        "Escalation Rate",
        "Response Consistency",
        "Employee Confidence Score",
        "AI Adoption Rate",
        "Prompt Reuse Rate",
        "Compliance Exception Count",
        "Member Satisfaction Signal",
    ]

    # Avustralya AI governance referansları
    AU_GOVERNANCE = {
        "framework": "Australia's Voluntary AI Safety Standard",
        "privacy": "Privacy Act 1988 (Cth)",
        "consumer": "Australian Consumer Law",
        "principles": [
            "Human oversight and control",
            "Transparency and explainability",
            "Fairness and non-discrimination",
            "Privacy protection and data governance",
            "Reliability and safety",
            "Contestability and redress",
            "Accountability",
            "Secure by design",
        ],
    }
```

---

## 2. Utility Modules

### `utils/openai_client.py`

```python
from openai import OpenAI
from config import Config


def get_client() -> OpenAI:
    return OpenAI(api_key=Config.OPENAI_API_KEY)


def chat(
    system_prompt: str,
    user_message: str,
    model: str = Config.OPENAI_MODEL,
    temperature: float = 0.4,
    max_tokens: int = 2048,
) -> str:
    """RACV Copilot agent'ları için merkezi chat fonksiyonu."""
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content
```

### `utils/data_loader.py`

```python
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(filename: str) -> list | dict:
    filepath = DATA_DIR / filename
    if not filepath.exists():
        # Dosya yoksa boş yapı döndür
        if filename.endswith(".json"):
            return []
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename: str, data: list | dict) -> None:
    filepath = DATA_DIR / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def load_experiments() -> list:
    return load_json("experiments.json")


def save_experiments(data: list) -> None:
    save_json("experiments.json", data)


def load_prompts() -> list:
    return load_json("prompts.json")


def save_prompts(data: list) -> None:
    save_json("prompts.json", data)


def load_risk_assessments() -> list:
    return load_json("risk_assessments.json")


def save_risk_assessments(data: list) -> None:
    save_json("risk_assessments.json", data)


def load_kpi_metrics() -> list:
    return load_json("kpi_metrics.json")


def save_kpi_metrics(data: list) -> None:
    save_json("kpi_metrics.json", data)


def load_training_modules() -> list:
    return load_json("training_modules.json")
```

### `utils/metrics.py`

```python
import pandas as pd
from datetime import datetime, timedelta
import random


def generate_sample_kpi_data(departments: list, kpis: list) -> pd.DataFrame:
    """Demo amaçlı örnek KPI verileri üretir."""
    rows = []
    base_date = datetime(2025, 1, 1)

    for dept in departments:
        for month_offset in range(12):
            date = base_date + timedelta(days=30 * month_offset)
            for kpi in kpis:
                # AI öncesi baseline
                baseline = _get_baseline(kpi)
                # AI sonrası iyileşme (aylar ilerledikçe artan)
                improvement_factor = min(0.05 * (month_offset + 1), 0.35)
                current = _apply_improvement(baseline, improvement_factor, kpi)

                rows.append(
                    {
                        "department": dept,
                        "date": date.strftime("%Y-%m"),
                        "kpi": kpi,
                        "baseline": round(baseline, 2),
                        "current": round(current, 2),
                        "improvement_pct": round(
                            abs(current - baseline) / baseline * 100, 1
                        ),
                    }
                )

    return pd.DataFrame(rows)


def _get_baseline(kpi: str) -> float:
    baselines = {
        "Average Handling Time": random.uniform(420, 600),       # saniye
        "First Contact Resolution": random.uniform(0.55, 0.65),  # oran
        "After-Call Work Duration": random.uniform(120, 180),     # saniye
        "Escalation Rate": random.uniform(0.18, 0.28),           # oran
        "Response Consistency": random.uniform(0.60, 0.72),      # oran
        "Employee Confidence Score": random.uniform(3.0, 3.8),   # 1-5
        "AI Adoption Rate": random.uniform(0.10, 0.20),          # oran
        "Prompt Reuse Rate": random.uniform(0.05, 0.15),         # oran
        "Compliance Exception Count": random.uniform(8, 15),     # adet
        "Member Satisfaction Signal": random.uniform(3.2, 3.8),  # 1-5
    }
    return baselines.get(kpi, 50.0)


def _apply_improvement(baseline: float, factor: float, kpi: str) -> float:
    # Bazı KPI'larda düşüş iyidir (handling time, escalation, exceptions)
    decrease_is_good = [
        "Average Handling Time",
        "After-Call Work Duration",
        "Escalation Rate",
        "Compliance Exception Count",
    ]
    if kpi in decrease_is_good:
        return baseline * (1 - factor)
    return baseline * (1 + factor)


def calculate_roi(
    time_saved_hours_per_week: float,
    num_employees: int,
    avg_hourly_cost: float = 45.0,
    weeks: int = 52,
) -> dict:
    """Basit ROI hesaplayıcı."""
    annual_hours_saved = time_saved_hours_per_week * num_employees * weeks
    annual_cost_saving = annual_hours_saved * avg_hourly_cost
    return {
        "annual_hours_saved": round(annual_hours_saved),
        "annual_cost_saving_aud": round(annual_cost_saving),
        "monthly_cost_saving_aud": round(annual_cost_saving / 12),
        "per_employee_hours_saved": round(time_saved_hours_per_week * weeks, 1),
    }
```

### `utils/charts.py`

```python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def experiment_pipeline_chart(experiments: list) -> go.Figure:
    """Experiment'lerin stage dağılımını gösteren funnel chart."""
    stage_order = ["Pipeline", "In-Flight", "Completed", "Scaled", "Stopped"]
    stage_counts = {}
    for exp in experiments:
        stage = exp.get("stage", "Pipeline")
        stage_counts[stage] = stage_counts.get(stage, 0) + 1

    stages = [s for s in stage_order if s in stage_counts]
    counts = [stage_counts[s] for s in stages]

    colors = {
        "Pipeline": "#4A90D9",
        "In-Flight": "#F5A623",
        "Completed": "#7ED321",
        "Scaled": "#50E3C2",
        "Stopped": "#D0021B",
    }

    fig = go.Figure(
        go.Funnel(
            y=stages,
            x=counts,
            marker=dict(color=[colors.get(s, "#999") for s in stages]),
            textinfo="value+percent initial",
        )
    )
    fig.update_layout(
        title="AI Experiment Pipeline",
        font=dict(size=14),
        height=400,
    )
    return fig


def department_adoption_chart(experiments: list) -> go.Figure:
    """Departman bazlı experiment dağılımı."""
    dept_counts = {}
    for exp in experiments:
        dept = exp.get("department", "Unknown")
        dept_counts[dept] = dept_counts.get(dept, 0) + 1

    df = pd.DataFrame(
        list(dept_counts.items()), columns=["Department", "Experiments"]
    ).sort_values("Experiments", ascending=True)

    fig = px.bar(
        df,
        x="Experiments",
        y="Department",
        orientation="h",
        color="Experiments",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        title="Experiments by Department",
        showlegend=False,
        height=400,
    )
    return fig


def kpi_trend_chart(df: pd.DataFrame, selected_kpi: str) -> go.Figure:
    """Belirli bir KPI'ın zaman içindeki trendini gösterir."""
    kpi_data = df[df["kpi"] == selected_kpi].groupby("date").mean(numeric_only=True).reset_index()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=kpi_data["date"],
            y=kpi_data["baseline"],
            name="Baseline (Pre-AI)",
            line=dict(color="#D0021B", dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=kpi_data["date"],
            y=kpi_data["current"],
            name="Current (With AI)",
            line=dict(color="#7ED321", width=3),
            fill="tonexty",
            fillcolor="rgba(126, 211, 33, 0.1)",
        )
    )
    fig.update_layout(
        title=f"{selected_kpi} — Trend Over Time",
        xaxis_title="Month",
        yaxis_title="Value",
        height=400,
    )
    return fig


def risk_distribution_chart(assessments: list) -> go.Figure:
    """Risk assessment dağılımını gösteren pie chart."""
    risk_counts = {}
    for a in assessments:
        level = a.get("risk_level", "Unknown")
        risk_counts[level] = risk_counts.get(level, 0) + 1

    colors = {
        "Low": "#7ED321",
        "Medium": "#F5A623",
        "High": "#D0021B",
        "Critical": "#8B0000",
    }

    fig = go.Figure(
        go.Pie(
            labels=list(risk_counts.keys()),
            values=list(risk_counts.values()),
            marker=dict(colors=[colors.get(k, "#999") for k in risk_counts.keys()]),
            hole=0.4,
        )
    )
    fig.update_layout(title="Risk Level Distribution", height=400)
    return fig
```

---

## 3. Copilot Agent Modülleri

### `agents/member_context_agent.py`

```python
from utils.openai_client import chat

SYSTEM_PROMPT = """You are the RACV Member Context Copilot — an internal AI assistant 
that helps RACV employees quickly understand a member's situation during critical moments.

Your role:
- Summarise the member's current situation, history, products, and open requests
- Highlight the most relevant context for the current interaction
- Flag any urgency indicators (safety concerns, repeated contacts, escalation history)
- Present information in a clear, scannable format

Rules:
- You are an INTERNAL tool — never generate content to send directly to the member
- Always indicate confidence level in your summary
- Flag if information seems incomplete and suggest what to verify
- Follow RACV's tone: professional, caring, member-first
- Never make binding commitments or policy decisions
- All outputs are decision SUPPORT, not decisions themselves

Output format:
## Member Context Brief
**Member**: [Name / ID]
**Current Situation**: [1-2 sentence summary]
**Products & Entitlements**: [bullet list]
**Recent Interactions**: [last 3-5 touchpoints]
**Open Requests/Claims**: [if any]
**⚠️ Flags**: [urgency, patterns, or concerns]
**Confidence**: [High / Medium / Low — explain gaps]
"""


def get_member_context(member_info: str) -> str:
    """Üye bilgilerini alıp bağlam özeti üretir."""
    return chat(
        system_prompt=SYSTEM_PROMPT,
        user_message=f"Summarise the following member context for the frontline agent:\n\n{member_info}",
    )


# Demo için örnek üye senaryoları
DEMO_SCENARIOS = {
    "roadside_emergency": {
        "title": "🚗 Roadside Emergency — Stranded Member",
        "input": """Member: Sarah Chen (ID: MEM-2847193)
Membership: Premium Roadside + Home Emergency (since 2019)
Location: Princes Freeway, near Werribee (GPS: -37.8997, 144.6614)
Time: 7:42 PM, Tuesday evening, winter
Vehicle: 2021 Toyota RAV4, registration ABC-123

Current call reason: Vehicle broke down, engine warning light came on, 
car won't start. She has two children (ages 4 and 7) in the car.
Temperature outside: 9°C

Recent history:
- 3 months ago: Battery replacement service (roadside)
- 8 months ago: Insurance claim — minor parking lot damage, resolved
- Active home insurance policy, renewal due in 6 weeks

No previous complaints. Member satisfaction survey last year: 4/5.
Has RACV app installed, push notifications enabled.""",
    },
    "insurance_claim": {
        "title": "🏠 Insurance Claim — Storm Damage",
        "input": """Member: James & Linda Morrison (ID: MEM-1593847)
Membership: Gold member since 2015
Products: Home & Contents Insurance (Premium), 2x Car Insurance, Travel Insurance

Current call reason: Major storm damage to roof and living room. 
Water ingress has damaged ceiling, carpet, and electronics.
Date of event: Last night (severe thunderstorm warning was active)

Property: 42 Elm Street, Hawthorn VIC 3122
Policy: HOM-2024-88431, Sum insured $850,000 (building), $120,000 (contents)
Excess: $500

Recent history:
- No previous home claims in 9 years of membership
- Car insurance claim 2 years ago — at-fault accident, resolved smoothly
- Called 2 hours ago but was on hold for 35 minutes, then disconnected
- Now calling back, likely frustrated

Special notes: James mentioned Linda has a medical condition requiring 
climate-controlled environment. They need urgent temporary accommodation.""",
    },
    "multi_service_query": {
        "title": "📞 Multi-Service Query — Loyal Member",
        "input": """Member: Robert Nguyen (ID: MEM-0934821)
Membership: Platinum member since 2008 (17 years)
Products: Premium Roadside, Home Insurance, 3x Car Insurance, 
Solar Energy plan, Annual Travel Insurance

Current call reason: Wants to understand his total RACV relationship — 
considering whether to renew everything or shop around.
Mentioned a competitor offered cheaper car insurance.

Recent history:
- 2 roadside assists this year (battery + flat tyre)
- Solar panel installation completed 4 months ago, very satisfied
- Home insurance renewal processed last month (5% increase noted)
- Booked RACV resort stay for Easter holidays
- Participated in member feedback survey — score: 3/5 (down from 4/5)

Sentiment indicators: Long-term loyal but showing signs of price sensitivity.
High lifetime value member. Flight risk: moderate-to-high.""",
    },
}
```

### `agents/policy_navigator_agent.py`

```python
from utils.openai_client import chat

SYSTEM_PROMPT = """You are the RACV Policy & Process Navigator — an internal AI assistant 
that helps RACV employees quickly find the correct policy, procedure, entitlement, 
or process step relevant to a member's situation.

Your role:
- Identify the most relevant policies and procedures for the given scenario
- Explain entitlements, coverage limits, and exclusions clearly
- Outline the correct process steps the employee should follow
- Highlight any exceptions, escalation triggers, or approval requirements

Rules:
- Reference specific policy sections and process names where possible
- If unsure about a specific detail, say so explicitly and recommend verification
- Present complex policy in plain language that frontline staff can act on immediately
- Never make binding interpretations — always frame as guidance pending formal review
- Flag where human review or supervisor approval is required

Output format:
## Policy & Process Guidance
**Scenario Type**: [category]
**Applicable Policies**: [list with brief descriptions]
**Member Entitlements**: [what the member is entitled to]
**Process Steps**: [numbered action list]
**⚠️ Escalation Triggers**: [when to involve supervisor/specialist]
**📋 Documentation Required**: [what needs to be recorded]
**Confidence**: [High / Medium / Low]
"""


def navigate_policy(scenario: str) -> str:
    return chat(
        system_prompt=SYSTEM_PROMPT,
        user_message=f"Find the relevant policy and process guidance for this situation:\n\n{scenario}",
    )


DEMO_SCENARIOS = {
    "roadside_entitlements": {
        "title": "🔧 Roadside — Premium Member Entitlements",
        "input": """A Premium Roadside member's car has broken down on the freeway 
at night with children in the car. What are their entitlements? 
What process should I follow? Are there any priority or safety protocols?""",
    },
    "storm_claim_process": {
        "title": "🌧️ Insurance — Storm Damage Claim Process",
        "input": """A member is reporting storm damage to their home — roof damage 
and water ingress affecting living areas. They have a medical situation 
requiring urgent temporary accommodation. What's the claims process? 
What emergency provisions exist? What approvals do I need?""",
    },
    "retention_authority": {
        "title": "💰 Retention — Discount Authority & Process",
        "input": """A 17-year Platinum member with multiple products is considering 
leaving due to a competitor's cheaper car insurance offer. What retention 
tools are available? What discount authority do I have? What's the 
escalation path if my authority is insufficient?""",
    },
}
```

### `agents/next_best_action_agent.py`

```python
from utils.openai_client import chat

SYSTEM_PROMPT = """You are the RACV Next Best Action Assistant — an internal AI tool 
that recommends the most appropriate next steps for RACV employees 
during member interactions.

Your role:
- Analyse the current member situation and interaction context
- Recommend the single best next action with clear rationale
- Provide 2-3 alternative actions ranked by priority
- Consider member sentiment, urgency, lifetime value, and operational constraints
- Factor in any open issues, upcoming renewals, or cross-sell opportunities

Rules:
- Recommendations are SUGGESTIONS — the employee always makes the final decision
- Prioritise member safety and wellbeing above all else
- Consider both immediate resolution and long-term relationship impact
- Flag if specialist involvement is recommended
- Be specific and actionable — avoid vague suggestions

Output format:
## Recommended Next Actions
**Context Summary**: [1 sentence]

### ✅ Primary Recommendation
**Action**: [specific action]
**Rationale**: [why this is the best next step]
**Expected Outcome**: [what this achieves]

### Alternative Actions
1. **[Action]** — [brief rationale]
2. **[Action]** — [brief rationale]

### ⚠️ Considerations
- [risk or sensitivity to be aware of]
- [timing or dependency notes]
"""


def get_next_best_action(context: str) -> str:
    return chat(
        system_prompt=SYSTEM_PROMPT,
        user_message=f"Based on this interaction context, what should the employee do next?\n\n{context}",
    )
```

### `agents/communication_drafter_agent.py`

```python
from utils.openai_client import chat

SYSTEM_PROMPT = """You are the RACV Communication Drafting Assistant — an internal AI tool 
that helps employees draft professional, empathetic communications to members.

You draft:
- Email responses to members
- SMS notifications
- Internal case notes and handover summaries
- Follow-up communications
- Escalation briefs

Rules:
- Match RACV's brand voice: professional, warm, caring, clear
- All drafts are SUGGESTIONS — employee must review and personalise before sending
- Never include binding commitments, specific dollar amounts, or legal promises
- Use plain Australian English (colour, organisation, etc.)
- Include placeholders [LIKE THIS] for details the employee must verify
- Adjust tone based on situation urgency and member sentiment
- For distressed members: lead with empathy, then action

Output format:
## Draft Communication
**Type**: [Email / SMS / Case Note / Handover]
**Tone**: [Empathetic / Professional / Urgent / Reassuring]
**Review Required**: Yes — employee must verify all details before sending

---
[Draft content here]
---

**⚠️ Review Checklist**:
- [ ] All [PLACEHOLDERS] filled with verified information
- [ ] No binding commitments made
- [ ] Tone appropriate for member's situation
- [ ] Correct member name and reference numbers
"""


def draft_communication(request: str) -> str:
    return chat(
        system_prompt=SYSTEM_PROMPT,
        user_message=request,
    )


DEMO_SCENARIOS = {
    "storm_damage_email": {
        "title": "📧 Storm Damage — Empathetic Claim Acknowledgement",
        "input": """Draft an email to James & Linda Morrison acknowledging their storm damage 
claim. Key context: They were disconnected on their first call (35 min hold), 
Linda has a medical condition needing climate control, roof and living room 
damaged. They need temporary accommodation urgently. We've now logged the 
claim and arranged an emergency assessor for tomorrow morning.""",
    },
    "case_handover": {
        "title": "📋 Shift Handover — Complex Member Case",
        "input": """Write a case handover note for the next shift. Robert Nguyen, 17-year 
Platinum member, called about potentially leaving RACV. He has 7 products 
with us. I've offered a loyalty review and scheduled a callback from 
the retention specialist for tomorrow at 2pm. His main concern is car 
insurance pricing. He seemed open to staying if we can demonstrate value 
across his whole relationship.""",
    },
    "follow_up_sms": {
        "title": "📱 Roadside — Follow-up SMS After Service",
        "input": """Draft a follow-up SMS to Sarah Chen after her roadside emergency last night. 
Her car was towed to the nearest Toyota dealer. She had two young children 
and it was cold. We arranged an Uber home for her. The dealer will call her 
tomorrow about the diagnosis. We want to check she's okay and confirm 
next steps.""",
    },
}
```

### `agents/prompt_coach_agent.py`

```python
from utils.openai_client import chat

SYSTEM_PROMPT = """You are the RACV Prompt Coach — an internal AI assistant that helps 
RACV employees write better prompts and use AI tools more effectively 
and responsibly.

Your role:
- Help employees improve their AI prompts for better results
- Teach prompt engineering principles in simple, practical terms
- Evaluate prompts for effectiveness, clarity, and safety
- Flag any prompts that might violate RACV AI Policy or governance rules
- Suggest approved prompt templates for common tasks

Rules:
- Use plain language — many users are non-technical
- Always explain WHY a prompt works or doesn't work
- Rate prompts on: Clarity, Specificity, Safety, Expected Quality
- If a prompt requests something that should not be AI-generated 
  (legal decisions, binding commitments, personal data exposure), flag it
- Encourage responsible use at every opportunity

Output format:
## Prompt Review
**Original Prompt**: [what the user wrote]
**Rating**: ⭐ [1-5] / 5

### Analysis
- **Clarity**: [score + explanation]
- **Specificity**: [score + explanation]  
- **Safety**: [score + explanation]
- **Expected Output Quality**: [score + explanation]

### Improved Version
[The better prompt]

### Why This Is Better
[Explanation in plain language]

### ⚠️ Governance Notes
[Any policy/safety considerations]
"""


def coach_prompt(user_prompt: str) -> str:
    return chat(
        system_prompt=SYSTEM_PROMPT,
        user_message=f"Please review and improve this prompt:\n\n{user_prompt}",
    )


def suggest_prompt_template(task_description: str) -> str:
    return chat(
        system_prompt=SYSTEM_PROMPT,
        user_message=f"Suggest an approved prompt template for this task:\n\n{task_description}",
    )
```

---

## 4. Governance Modülleri

### `governance/risk_matrix.py`

```python
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


@dataclass
class RiskAssessment:
    id: str
    experiment_id: str
    experiment_name: str
    department: str
    assessed_by: str
    assessed_date: str

    # Risk boyutları (1-5 ölçeğinde)
    data_sensitivity: int          # Kullanılan veri ne kadar hassas?
    decision_impact: int           # AI çıktısı ne kadar kritik kararlara etki ediyor?
    automation_level: int          # İnsan kontrolü ne kadar az?
    member_facing: int             # Çıktı doğrudan üyeye mi gidiyor?
    reversibility: int             # Hata durumunda geri dönüş ne kadar kolay?
    regulatory_exposure: int       # Düzenleyici risk ne kadar yüksek?

    # Hesaplanan alanlar
    total_score: int = 0
    risk_level: str = "Low"
    requires_review: bool = False
    mitigation_notes: str = ""

    def calculate_risk(self):
        self.total_score = (
            self.data_sensitivity
            + self.decision_impact
            + self.automation_level
            + self.member_facing
            + self.reversibility
            + self.regulatory_exposure
        )

        if self.total_score <= 10:
            self.risk_level = "Low"
            self.requires_review = False
        elif self.total_score <= 17:
            self.risk_level = "Medium"
            self.requires_review = False
        elif self.total_score <= 24:
            self.risk_level = "High"
            self.requires_review = True
        else:
            self.risk_level = "Critical"
            self.requires_review = True

        return self

    def to_dict(self) -> dict:
        return asdict(self)


def create_assessment(
    experiment_id: str,
    experiment_name: str,
    department: str,
    assessed_by: str,
    scores: dict,
    mitigation_notes: str = "",
) -> RiskAssessment:
    assessment = RiskAssessment(
        id=str(uuid.uuid4())[:8],
        experiment_id=experiment_id,
        experiment_name=experiment_name,
        department=department,
        assessed_by=assessed_by,
        assessed_date=datetime.now().strftime("%Y-%m-%d"),
        data_sensitivity=scores.get("data_sensitivity", 1),
        decision_impact=scores.get("decision_impact", 1),
        automation_level=scores.get("automation_level", 1),
        member_facing=scores.get("member_facing", 1),
        reversibility=scores.get("reversibility", 1),
        regulatory_exposure=scores.get("regulatory_exposure", 1),
        mitigation_notes=mitigation_notes,
    )
    return assessment.calculate_risk()


# Australian AI governance uyumluluk kontrolleri
COMPLIANCE_CHECKLIST = {
    "human_oversight": {
        "label": "Human Oversight & Control",
        "question": "Is there a human review step before AI outputs are actioned?",
        "required_for": ["Medium", "High", "Critical"],
    },
    "transparency": {
        "label": "Transparency & Explainability",
        "question": "Can users understand how the AI reached its output?",
        "required_for": ["Low", "Medium", "High", "Critical"],
    },
    "fairness": {
        "label": "Fairness & Non-discrimination",
        "question": "Has the use case been tested for bias across member demographics?",
        "required_for": ["Medium", "High", "Critical"],
    },
    "privacy": {
        "label": "Privacy Protection (Privacy Act 1988)",
        "question": "Does this comply with the Australian Privacy Principles for personal data handling?",
        "required_for": ["Low", "Medium", "High", "Critical"],
    },
    "data_minimisation": {
        "label": "Data Minimisation",
        "question": "Does the AI use only the minimum data necessary for the task?",
        "required_for": ["Medium", "High", "Critical"],
    },
    "contestability": {
        "label": "Contestability & Redress",
        "question": "Can a member challenge an AI-influenced decision and get human review?",
        "required_for": ["High", "Critical"],
    },
    "audit_trail": {
        "label": "Audit Trail",
        "question": "Are AI interactions logged for accountability and review?",
        "required_for": ["Medium", "High", "Critical"],
    },
    "incident_response": {
        "label": "Incident Response Plan",
        "question": "Is there a documented plan if the AI produces harmful or incorrect outputs?",
        "required_for": ["High", "Critical"],
    },
}
```

### `governance/compliance_checker.py`

```python
from governance.risk_matrix import COMPLIANCE_CHECKLIST


def check_compliance(risk_level: str, completed_checks: dict) -> dict:
    """
    Belirli bir risk seviyesi için compliance durumunu kontrol eder.
    
    Args:
        risk_level: "Low", "Medium", "High", or "Critical"
        completed_checks: {"check_id": True/False, ...}
    
    Returns:
        Compliance raporu
    """
    required_checks = []
    passed = []
    failed = []

    for check_id, check_info in COMPLIANCE_CHECKLIST.items():
        if risk_level in check_info["required_for"]:
            required_checks.append(check_id)
            if completed_checks.get(check_id, False):
                passed.append(check_id)
            else:
                failed.append(check_id)

    total_required = len(required_checks)
    total_passed = len(passed)
    compliance_pct = (total_passed / total_required * 100) if total_required > 0 else 100

    status = "✅ Compliant" if compliance_pct == 100 else "⚠️ Gaps Found" if compliance_pct >= 60 else "❌ Non-Compliant"

    return {
        "risk_level": risk_level,
        "status": status,
        "compliance_percentage": round(compliance_pct, 1),
        "total_required": total_required,
        "total_passed": total_passed,
        "passed_checks": passed,
        "failed_checks": failed,
        "failed_details": [
            {
                "id": cid,
                "label": COMPLIANCE_CHECKLIST[cid]["label"],
                "question": COMPLIANCE_CHECKLIST[cid]["question"],
            }
            for cid in failed
        ],
    }
```

### `governance/audit_logger.py`

```python
import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG_PATH = Path(__file__).parent.parent / "data" / "audit_log.json"


def log_event(
    event_type: str,
    agent_name: str,
    user: str,
    department: str,
    details: str = "",
    risk_flag: bool = False,
) -> dict:
    """Her AI etkileşimini audit log'a kaydeder."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "agent_name": agent_name,
        "user": user,
        "department": department,
        "details": details[:500],  # max 500 karakter
        "risk_flag": risk_flag,
    }

    # Mevcut log'u yükle veya yeni oluştur
    log = []
    if AUDIT_LOG_PATH.exists():
        with open(AUDIT_LOG_PATH, "r") as f:
            log = json.load(f)

    log.append(entry)

    # Son 10000 kayıt tut
    if len(log) > 10000:
        log = log[-10000:]

    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_PATH, "w") as f:
        json.dump(log, f, indent=2, default=str)

    return entry


def get_recent_events(limit: int = 50) -> list:
    if not AUDIT_LOG_PATH.exists():
        return []
    with open(AUDIT_LOG_PATH, "r") as f:
        log = json.load(f)
    return log[-limit:][::-1]  # En yeni en üstte
```

---

## 5. Örnek Veri Dosyaları

### `data/experiments.json`

```json
[
  {
    "id": "EXP-001",
    "name": "Roadside Call Summarisation",
    "department": "Roadside Assistance",
    "description": "Auto-summarise roadside calls to reduce after-call work by generating case notes from conversation context.",
    "stage": "In-Flight",
    "owner": "Sarah Mitchell",
    "start_date": "2025-03-01",
    "risk_level": "Medium",
    "baseline_metric": "Average 4.2 min after-call work per interaction",
    "target_metric": "Reduce to under 2 min after-call work",
    "current_result": "2.8 min average in pilot group (33% reduction)",
    "ai_tool": "Microsoft Copilot + Custom Agent",
    "participants": 12,
    "governance_status": "Approved",
    "notes": "Pilot running with 12 operators in Tullamarine hub. Positive feedback on draft quality."
  },
  {
    "id": "EXP-002",
    "name": "Claims First Contact Triage",
    "department": "Insurance & Claims",
    "description": "AI-assisted triage of incoming claims to classify urgency, identify policy coverage, and suggest next steps for claims handlers.",
    "stage": "Pipeline",
    "owner": "Michael Torres",
    "start_date": "2025-05-01",
    "risk_level": "High",
    "baseline_metric": "Average 8.5 min first contact handling time",
    "target_metric": "Reduce to 5.5 min with improved accuracy",
    "current_result": "Not yet started",
    "ai_tool": "Microsoft Copilot + Policy Navigator Agent",
    "participants": 0,
    "governance_status": "Under Review",
    "notes": "Governance review required due to sensitive claims data. Risk assessment in progress."
  },
  {
    "id": "EXP-003",
    "name": "Member Context Brief Generator",
    "department": "Member Contact Centre",
    "description": "Generate a one-page member context brief before each interaction, summarising history, products, sentiment, and open issues.",
    "stage": "Completed",
    "owner": "Jenny Park",
    "start_date": "2025-01-15",
    "risk_level": "Low",
    "baseline_metric": "Agents spend 2-3 min manually reviewing member history",
    "target_metric": "Instant context brief in under 10 seconds",
    "current_result": "Average 8 second generation time. 91% agent satisfaction rating.",
    "ai_tool": "Microsoft Copilot + Member Context Agent",
    "participants": 35,
    "governance_status": "Approved",
    "notes": "Successfully completed 8-week pilot. Ready for scaling decision."
  },
  {
    "id": "EXP-004",
    "name": "Prompt-Assisted Email Drafting",
    "department": "Member Contact Centre",
    "description": "AI-drafted email responses for common member enquiries, reviewed and personalised by agents before sending.",
    "stage": "Scaled",
    "owner": "David Kim",
    "start_date": "2024-11-01",
    "risk_level": "Medium",
    "baseline_metric": "Average 6 min to draft a member email",
    "target_metric": "Under 2 min with AI draft + human review",
    "current_result": "1.8 min average. Deployed across 3 contact centre teams.",
    "ai_tool": "Microsoft Copilot",
    "participants": 85,
    "governance_status": "Approved",
    "notes": "First experiment to reach full scale. Human review step maintained. Quality audit passed."
  },
  {
    "id": "EXP-005",
    "name": "Solar Installation Scheduling Optimiser",
    "department": "Energy Services",
    "description": "AI-assisted scheduling that considers installer availability, weather forecasts, and member preferences.",
    "stage": "Pipeline",
    "owner": "Amanda Russo",
    "start_date": "2025-06-15",
    "risk_level": "Low",
    "baseline_metric": "Manual scheduling takes 15 min per booking",
    "target_metric": "Reduce to 5 min with AI-suggested optimal slots",
    "current_result": "Not yet started",
    "ai_tool": "Microsoft Copilot + Power Automate",
    "participants": 0,
    "governance_status": "Approved",
    "notes": "Low-risk operational efficiency use case. Good candidate for quick win."
  },
  {
    "id": "EXP-006",
    "name": "Travel Disruption Response Assistant",
    "department": "Travel Services",
    "description": "AI assistant for travel support agents handling flight cancellations, rebookings, and insurance claim initiation.",
    "stage": "In-Flight",
    "owner": "Lisa Wang",
    "start_date": "2025-04-01",
    "risk_level": "Medium",
    "baseline_metric": "Average 12 min handling time for disruption calls",
    "target_metric": "Under 7 min with AI-assisted rebooking guidance",
    "current_result": "8.3 min average in pilot (31% reduction)",
    "ai_tool": "Microsoft Copilot + Custom Agent",
    "participants": 8,
    "governance_status": "Approved",
    "notes": "Running well. Team feedback: 'saves the most time on policy lookups for international cover'."
  },
  {
    "id": "EXP-007",
    "name": "Automated Claims Documentation Review",
    "department": "Insurance & Claims",
    "description": "AI pre-review of claims documentation for completeness before human assessor review.",
    "stage": "Stopped",
    "owner": "Tom Bradley",
    "start_date": "2025-02-01",
    "risk_level": "High",
    "baseline_metric": "20% of claims returned for missing documentation",
    "target_metric": "Under 8% return rate",
    "current_result": "Stopped — accuracy below acceptable threshold (72% vs 90% target)",
    "ai_tool": "Microsoft Copilot + Azure AI Document Intelligence",
    "participants": 5,
    "governance_status": "Suspended",
    "notes": "Stopped after 4-week pilot. Document variety too high for current model. Will revisit with improved training data in Q3."
  }
]
```

### `data/prompts.json`

```json
[
  {
    "id": "PRM-001",
    "title": "Member Context Summary",
    "category": "Member Service",
    "department": "All",
    "status": "Approved",
    "prompt": "Summarise this member's situation in 3-4 sentences. Include: their current issue, relevant products they hold, any recent interactions, and urgency level. Format: Start with the most important fact. Member data: [PASTE MEMBER DETAILS]",
    "use_case": "Before any member interaction to get quick context",
    "tips": "Always paste actual member data, not just the member ID. Remove any data you don't need for the specific interaction.",
    "governance_notes": "Approved for internal use. Do not include in any external communications.",
    "created_by": "AI Transformation Team",
    "created_date": "2025-01-10",
    "usage_count": 342
  },
  {
    "id": "PRM-002",
    "title": "Empathetic Email Response — Claims",
    "category": "Communication",
    "department": "Insurance & Claims",
    "status": "Approved",
    "prompt": "Draft a professional and empathetic email to a member about their insurance claim. Context: [DESCRIBE SITUATION]. Tone: Warm but professional. Lead with empathy for their situation, then clearly explain next steps. Include: timeline expectations, what they need to do (if anything), and who to contact for questions. Use Australian English. Do NOT include any specific dollar amounts or binding commitments.",
    "use_case": "Responding to claims enquiries or providing claim updates",
    "tips": "Always review the draft for accuracy before sending. Replace all placeholders. Check the member's name is correct.",
    "governance_notes": "Human review required before sending. No binding financial commitments.",
    "created_by": "Claims Team Lead",
    "created_date": "2025-02-15",
    "usage_count": 189
  },
  {
    "id": "PRM-003",
    "title": "Case Note Generator",
    "category": "Documentation",
    "department": "All",
    "status": "Approved",
    "prompt": "Write a concise case note for this member interaction. Include: Date, member name/ID, reason for contact, key discussion points, actions taken, agreed next steps, and any follow-up required. Keep it factual and under 150 words. Interaction details: [DESCRIBE WHAT HAPPENED]",
    "use_case": "After any member call or interaction",
    "tips": "Be specific about agreed timelines. If you promised a callback, include the date and time.",
    "governance_notes": "Standard use. Ensure accuracy of all recorded facts.",
    "created_by": "AI Transformation Team",
    "created_date": "2025-01-10",
    "usage_count": 567
  },
  {
    "id": "PRM-004",
    "title": "Policy Lookup Assistant",
    "category": "Knowledge",
    "department": "All",
    "status": "Approved",
    "prompt": "I need to understand the RACV policy or process for: [DESCRIBE SITUATION]. Please explain: 1) What policy applies, 2) What the member is entitled to, 3) What steps I should follow, 4) Any exceptions or escalation triggers. Keep the language simple and actionable.",
    "use_case": "When unsure about correct policy or process during member interaction",
    "tips": "Be specific about the member's product type and situation. The more context you give, the better the answer.",
    "governance_notes": "AI guidance only. Verify with official policy documents for complex or high-value decisions.",
    "created_by": "AI Transformation Team",
    "created_date": "2025-01-20",
    "usage_count": 423
  },
  {
    "id": "PRM-005",
    "title": "Shift Handover Summary",
    "category": "Documentation",
    "department": "Member Contact Centre",
    "status": "Approved",
    "prompt": "Create a shift handover summary for the incoming team. Include: 1) Open/unresolved member cases with brief status, 2) Any escalations or urgent follow-ups needed, 3) Scheduled callbacks with times, 4) Anything unusual from this shift. Here are the details: [LIST OPEN ITEMS]",
    "use_case": "End of shift handover between contact centre teams",
    "tips": "Prioritise items by urgency. Put callbacks with specific times at the top.",
    "governance_notes": "Internal use only. Do not include sensitive member data unnecessarily.",
    "created_by": "Contact Centre Manager",
    "created_date": "2025-03-01",
    "usage_count": 98
  },
  {
    "id": "PRM-006",
    "title": "Meeting Action Items Extractor",
    "category": "Productivity",
    "department": "Corporate Services",
    "status": "Approved",
    "prompt": "Extract all action items from these meeting notes. For each action item, list: 1) What needs to be done, 2) Who is responsible, 3) Due date (if mentioned), 4) Priority (High/Medium/Low based on context). Meeting notes: [PASTE NOTES]",
    "use_case": "After team meetings or stakeholder workshops",
    "tips": "Works best with detailed notes. If recording a Teams meeting, use the transcript.",
    "governance_notes": "Do not paste confidential board or executive meeting content.",
    "created_by": "AI Transformation Team",
    "created_date": "2025-02-20",
    "usage_count": 156
  },
  {
    "id": "PRM-007",
    "title": "Competitor Offer Comparison",
    "category": "Retention",
    "department": "Member Contact Centre",
    "status": "Under Review",
    "prompt": "A member has received a competitor offer for [PRODUCT TYPE] at [PRICE/FEATURE]. Help me understand: 1) How our product compares on key features, 2) What unique value RACV provides (e.g., bundled benefits, member discounts, service quality), 3) Talking points I can use in the conversation. Do NOT make up specific pricing — only reference features and benefits.",
    "use_case": "When a member mentions considering a competitor",
    "tips": "Never promise to match a competitor's price unless authorised. Focus on value, not just cost.",
    "governance_notes": "Under review — needs validation that outputs don't contain inaccurate product claims.",
    "created_by": "Retention Team",
    "created_date": "2025-03-20",
    "usage_count": 12
  }
]
```

### `data/training_modules.json`

```json
[
  {
    "id": "TRN-001",
    "title": "AI Fundamentals for RACV Teams",
    "level": "Beginner",
    "duration_minutes": 30,
    "description": "What AI is, what it can and can't do, and how RACV is using it. No technical background needed.",
    "topics": [
      "What is generative AI?",
      "How does Microsoft Copilot work?",
      "What RACV uses AI for today",
      "What AI should NOT be used for",
      "Your role in responsible AI use"
    ],
    "target_audience": "All RACV employees",
    "status": "Active"
  },
  {
    "id": "TRN-002",
    "title": "Prompt Engineering 101",
    "level": "Beginner",
    "duration_minutes": 45,
    "description": "How to write effective prompts that get useful results from AI tools.",
    "topics": [
      "What makes a good prompt?",
      "The CRAFT framework: Context, Role, Action, Format, Tone",
      "Common prompting mistakes",
      "Hands-on practice with approved prompts",
      "When to use templates vs custom prompts"
    ],
    "target_audience": "All AI users",
    "status": "Active"
  },
  {
    "id": "TRN-003",
    "title": "Responsible AI at RACV",
    "level": "Beginner",
    "duration_minutes": 30,
    "description": "RACV's AI policy, Australian regulatory context, and your responsibilities when using AI.",
    "topics": [
      "RACV AI Policy overview",
      "Australian AI governance landscape",
      "Privacy Act 1988 and AI",
      "What data can and can't go into AI tools",
      "How to report AI concerns",
      "The human-in-the-loop principle"
    ],
    "target_audience": "All RACV employees",
    "status": "Active"
  },
  {
    "id": "TRN-004",
    "title": "Copilot for Team Leaders",
    "level": "Intermediate",
    "duration_minutes": 60,
    "description": "How to lead AI adoption in your team: coaching, measuring, and scaling responsibly.",
    "topics": [
      "Your role as an AI champion",
      "Identifying use cases in your team",
      "How to measure AI impact on your KPIs",
      "Coaching your team on effective AI use",
      "Handling resistance and building trust",
      "Submitting new experiment proposals"
    ],
    "target_audience": "Team Leaders, Managers",
    "status": "Active"
  },
  {
    "id": "TRN-005",
    "title": "Building Custom Copilot Agents",
    "level": "Advanced",
    "duration_minutes": 90,
    "description": "Hands-on workshop for building task-specific Copilot agents in Copilot Studio.",
    "topics": [
      "Copilot Studio overview",
      "Designing agent conversations",
      "Adding knowledge sources",
      "Connecting to business data",
      "Testing and publishing agents",
      "Governance requirements for custom agents"
    ],
    "target_audience": "AI Champions, IT Team, Power Users",
    "status": "Active"
  }
]
```

---

## 6. Streamlit Sayfaları

### `app.py` — Ana giriş noktası

```python
import streamlit as st

st.set_page_config(
    page_title="Moments That Matter — Copilot Command Centre",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #003366;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: -10px;
    }
    .metric-card {
        background: linear-gradient(135deg, #003366 0%, #004d99 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="main-header">🏢 Moments That Matter</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Copilot Command Centre — AI Adoption Platform for Member-Centric Organisations</p>',
    unsafe_allow_html=True,
)

st.divider()

# Ana sayfa içeriği
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Active Experiments", value="4", delta="+2 this month")
with col2:
    st.metric(label="Copilot Agents", value="5", delta="2 in pilot")
with col3:
    st.metric(label="Approved Prompts", value="6", delta="+3 new")
with col4:
    st.metric(label="Trained Employees", value="140", delta="+35 this month")

st.divider()

st.markdown("## 🧭 Quick Navigation")

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.markdown(
        """
        ### 🤖 Copilot Agents
        Test the five bespoke Copilot agents designed for RACV's 
        critical member moments — from roadside emergencies to 
        insurance claims.
        """
    )

with nav_col2:
    st.markdown(
        """
        ### 🧪 Experiment Registry
        Track all AI experiments from pipeline through to scale. 
        See what's working, what's stopped, and what's ready 
        to scale organisation-wide.
        """
    )

with nav_col3:
    st.markdown(
        """
        ### 🛡️ Governance & Compliance
        Every AI use case assessed against Australia's AI Safety 
        Standard and Privacy Act 1988. Risk matrix, compliance 
        checks, and audit trail built in.
        """
    )

st.divider()

st.markdown(
    """
    ### About This Project
    
    **Moments That Matter Copilot Command Centre** is a demonstration of how a 
    member-centric organisation like RACV can adopt AI safely, effectively, and at scale.
    
    This platform addresses the full AI adoption lifecycle:
    
    - **Copilot Agents** — Task-specific AI assistants for frontline teams
    - **Experiment Registry** — Systematic tracking of AI initiatives from idea to scale  
    - **ROI Calculator** — Measurable business impact tied to real KPIs
    - **Prompt Library** — Curated, approved prompts with governance controls
    - **Governance Framework** — Risk assessment aligned with Australian regulations
    - **Training Hub** — Capability building from beginner to advanced
    
    Built as a portfolio project demonstrating AI transformation capability.
    """
)
```

### `pages/1_🏠_Dashboard.py`

```python
import streamlit as st
import pandas as pd
from utils.data_loader import load_experiments, load_prompts, load_risk_assessments
from utils.metrics import generate_sample_kpi_data
from utils.charts import (
    experiment_pipeline_chart,
    department_adoption_chart,
    kpi_trend_chart,
)
from config import Config

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")
st.title("🏠 Command Centre Dashboard")
st.markdown("Real-time overview of AI adoption, experiments, and impact across the organisation.")

st.divider()

# Verileri yükle
experiments = load_experiments()
prompts = load_prompts()

# Üst metrikler
col1, col2, col3, col4, col5 = st.columns(5)

total_exp = len(experiments)
in_flight = len([e for e in experiments if e["stage"] == "In-Flight"])
completed = len([e for e in experiments if e["stage"] == "Completed"])
scaled = len([e for e in experiments if e["stage"] == "Scaled"])
stopped = len([e for e in experiments if e["stage"] == "Stopped"])

with col1:
    st.metric("Total Experiments", total_exp)
with col2:
    st.metric("In-Flight", in_flight, delta=f"{in_flight} active")
with col3:
    st.metric("Completed", completed)
with col4:
    st.metric("Scaled ✅", scaled, delta="Ready for org-wide")
with col5:
    st.metric("Stopped ⛔", stopped)

st.divider()

# Grafik satırı
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if experiments:
        st.plotly_chart(
            experiment_pipeline_chart(experiments), use_container_width=True
        )
    else:
        st.info("No experiments yet. Add some in the Experiment Registry.")

with chart_col2:
    if experiments:
        st.plotly_chart(
            department_adoption_chart(experiments), use_container_width=True
        )

st.divider()

# KPI trend
st.markdown("## 📈 KPI Impact Tracker")
st.markdown("Simulated KPI trends showing the projected impact of AI adoption over 12 months.")

kpi_data = generate_sample_kpi_data(
    Config.DEPARTMENTS[:4], Config.KPI_CATEGORIES[:6]
)

selected_kpi = st.selectbox("Select KPI to visualise:", Config.KPI_CATEGORIES[:6])

st.plotly_chart(kpi_trend_chart(kpi_data, selected_kpi), use_container_width=True)

st.divider()

# Experiment özet tablosu
st.markdown("## 🧪 Experiment Summary")

if experiments:
    df = pd.DataFrame(experiments)[
        ["id", "name", "department", "stage", "risk_level", "governance_status"]
    ]
    
    # Renk kodlaması için stage badge'leri
    stage_colors = {
        "Pipeline": "🔵",
        "In-Flight": "🟡",
        "Completed": "🟢",
        "Scaled": "✅",
        "Stopped": "🔴",
    }
    df["stage"] = df["stage"].map(lambda x: f"{stage_colors.get(x, '')} {x}")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No experiments recorded yet.")
```

### `pages/2_🤖_Copilot_Agents.py`

```python
import streamlit as st
from config import Config
from governance.audit_logger import log_event

st.set_page_config(page_title="Copilot Agents", page_icon="🤖", layout="wide")
st.title("🤖 Copilot Agents — Live Demo")
st.markdown(
    """
    Test the five bespoke Copilot agents designed for RACV's critical member moments.
    Each agent serves a specific function in the employee workflow.
    
    > ⚠️ **Note**: These are internal employee tools — they support decision-making, 
    > they don't make decisions. Human review is always required.
    """
)

st.divider()

agent_choice = st.selectbox(
    "Select a Copilot Agent to test:",
    [
        "👤 Member Context Copilot",
        "📋 Policy & Process Navigator",
        "✅ Next Best Action Assistant",
        "✉️ Communication Drafter",
        "🎯 Prompt Coach",
    ],
)

st.divider()

# --------- MEMBER CONTEXT COPILOT ---------
if agent_choice == "👤 Member Context Copilot":
    from agents.member_context_agent import get_member_context, DEMO_SCENARIOS

    st.markdown("### 👤 Member Context Copilot")
    st.markdown(
        "Generates a quick context brief about a member so frontline agents can "
        "understand the situation before or during an interaction."
    )

    tab1, tab2 = st.tabs(["🎬 Demo Scenarios", "✏️ Custom Input"])

    with tab1:
        scenario_key = st.selectbox(
            "Choose a demo scenario:",
            list(DEMO_SCENARIOS.keys()),
            format_func=lambda x: DEMO_SCENARIOS[x]["title"],
        )
        scenario = DEMO_SCENARIOS[scenario_key]

        with st.expander("📄 View Input Data", expanded=False):
            st.text(scenario["input"])

        if st.button("🚀 Generate Member Context Brief", key="demo_context"):
            if not Config.OPENAI_API_KEY:
                st.error("Please set OPENAI_API_KEY in your .env file.")
            else:
                with st.spinner("Generating context brief..."):
                    result = get_member_context(scenario["input"])
                    log_event(
                        event_type="agent_query",
                        agent_name="Member Context Copilot",
                        user="demo_user",
                        department="Demo",
                        details=f"Scenario: {scenario_key}",
                    )
                st.markdown(result)
                st.info(
                    "⚠️ This is AI-generated decision support. Always verify key details "
                    "against member records before acting."
                )

    with tab2:
        custom_input = st.text_area(
            "Paste member context details:",
            height=200,
            placeholder="Member name, ID, products, current situation, recent history...",
        )
        if st.button("🚀 Generate Context Brief", key="custom_context"):
            if custom_input and Config.OPENAI_API_KEY:
                with st.spinner("Generating..."):
                    result = get_member_context(custom_input)
                    log_event(
                        event_type="agent_query",
                        agent_name="Member Context Copilot",
                        user="demo_user",
                        department="Custom",
                        details="Custom input",
                    )
                st.markdown(result)

# --------- POLICY NAVIGATOR ---------
elif agent_choice == "📋 Policy & Process Navigator":
    from agents.policy_navigator_agent import navigate_policy, DEMO_SCENARIOS

    st.markdown("### 📋 Policy & Process Navigator")
    st.markdown(
        "Helps employees quickly find the correct policy, procedure, or entitlement "
        "relevant to a member's situation."
    )

    tab1, tab2 = st.tabs(["🎬 Demo Scenarios", "✏️ Custom Query"])

    with tab1:
        scenario_key = st.selectbox(
            "Choose a demo scenario:",
            list(DEMO_SCENARIOS.keys()),
            format_func=lambda x: DEMO_SCENARIOS[x]["title"],
        )
        scenario = DEMO_SCENARIOS[scenario_key]

        with st.expander("📄 View Query", expanded=False):
            st.text(scenario["input"])

        if st.button("🚀 Find Policy Guidance", key="demo_policy"):
            if not Config.OPENAI_API_KEY:
                st.error("Please set OPENAI_API_KEY in your .env file.")
            else:
                with st.spinner("Searching policies..."):
                    result = navigate_policy(scenario["input"])
                    log_event(
                        event_type="agent_query",
                        agent_name="Policy Navigator",
                        user="demo_user",
                        department="Demo",
                        details=f"Scenario: {scenario_key}",
                    )
                st.markdown(result)
                st.warning(
                    "📋 AI guidance only — verify against official RACV policy documents "
                    "for complex or high-value decisions."
                )

    with tab2:
        custom_query = st.text_area(
            "Describe the situation you need policy guidance for:",
            height=150,
            placeholder="A member is asking about...",
        )
        if st.button("🚀 Find Guidance", key="custom_policy"):
            if custom_query and Config.OPENAI_API_KEY:
                with st.spinner("Searching..."):
                    result = navigate_policy(custom_query)
                st.markdown(result)

# --------- NEXT BEST ACTION ---------
elif agent_choice == "✅ Next Best Action Assistant":
    from agents.next_best_action_agent import get_next_best_action

    st.markdown("### ✅ Next Best Action Assistant")
    st.markdown(
        "Recommends the most appropriate next steps based on the current member interaction context."
    )

    context_input = st.text_area(
        "Describe the current interaction context:",
        height=200,
        placeholder="""Example: Sarah Chen called about her car breaking down on the Princes 
Freeway at 7:42 PM. She has two young children in the car, it's 9°C outside. 
She's a Premium Roadside member. Her car is a 2021 Toyota RAV4. 
The engine warning light came on and the car won't restart. 
I've confirmed her identity and membership status. What should I do next?""",
    )

    if st.button("🚀 Get Recommended Actions"):
        if context_input and Config.OPENAI_API_KEY:
            with st.spinner("Analysing situation..."):
                result = get_next_best_action(context_input)
                log_event(
                    event_type="agent_query",
                    agent_name="Next Best Action",
                    user="demo_user",
                    department="Demo",
                    details="Custom context query",
                )
            st.markdown(result)
            st.info("💡 These are recommendations only. You make the final decision.")

# --------- COMMUNICATION DRAFTER ---------
elif agent_choice == "✉️ Communication Drafter":
    from agents.communication_drafter_agent import draft_communication, DEMO_SCENARIOS

    st.markdown("### ✉️ Communication Drafter")
    st.markdown(
        "Drafts professional, empathetic communications for review before sending."
    )

    tab1, tab2 = st.tabs(["🎬 Demo Scenarios", "✏️ Custom Request"])

    with tab1:
        scenario_key = st.selectbox(
            "Choose a demo scenario:",
            list(DEMO_SCENARIOS.keys()),
            format_func=lambda x: DEMO_SCENARIOS[x]["title"],
        )
        scenario = DEMO_SCENARIOS[scenario_key]

        with st.expander("📄 View Brief", expanded=False):
            st.text(scenario["input"])

        if st.button("🚀 Generate Draft", key="demo_draft"):
            if not Config.OPENAI_API_KEY:
                st.error("Please set OPENAI_API_KEY.")
            else:
                with st.spinner("Drafting communication..."):
                    result = draft_communication(scenario["input"])
                    log_event(
                        event_type="agent_query",
                        agent_name="Communication Drafter",
                        user="demo_user",
                        department="Demo",
                        details=f"Scenario: {scenario_key}",
                    )
                st.markdown(result)
                st.error(
                    "🛑 DRAFT ONLY — You MUST review and personalise before sending. "
                    "Check all placeholders, verify facts, and ensure appropriate tone."
                )

    with tab2:
        custom_request = st.text_area(
            "What communication do you need drafted?",
            height=150,
            placeholder="Draft an email to... / Write a case note for... / Create an SMS to...",
        )
        if st.button("🚀 Generate Draft", key="custom_draft"):
            if custom_request and Config.OPENAI_API_KEY:
                with st.spinner("Drafting..."):
                    result = draft_communication(custom_request)
                st.markdown(result)

# --------- PROMPT COACH ---------
elif agent_choice == "🎯 Prompt Coach":
    from agents.prompt_coach_agent import coach_prompt, suggest_prompt_template

    st.markdown("### 🎯 Prompt Coach")
    st.markdown(
        "Helps you write better prompts and use AI tools more effectively and responsibly."
    )

    tab1, tab2 = st.tabs(["📝 Review My Prompt", "💡 Suggest a Template"])

    with tab1:
        user_prompt = st.text_area(
            "Paste the prompt you want reviewed:",
            height=150,
            placeholder="Example: Tell me about this member's claim...",
        )
        if st.button("🚀 Review & Improve", key="review_prompt"):
            if user_prompt and Config.OPENAI_API_KEY:
                with st.spinner("Reviewing your prompt..."):
                    result = coach_prompt(user_prompt)
                    log_event(
                        event_type="prompt_coaching",
                        agent_name="Prompt Coach",
                        user="demo_user",
                        department="Demo",
                        details="Prompt review request",
                    )
                st.markdown(result)

    with tab2:
        task_desc = st.text_area(
            "Describe the task you need a prompt for:",
            height=100,
            placeholder="I need to summarise a member's complaint history...",
        )
        if st.button("🚀 Suggest Template", key="suggest_template"):
            if task_desc and Config.OPENAI_API_KEY:
                with st.spinner("Creating template..."):
                    result = suggest_prompt_template(task_desc)
                st.markdown(result)
```

### `pages/3_🧪_Experiment_Registry.py`

```python
import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from utils.data_loader import load_experiments, save_experiments
from utils.charts import experiment_pipeline_chart, department_adoption_chart
from config import Config

st.set_page_config(page_title="Experiment Registry", page_icon="🧪", layout="wide")
st.title("🧪 AI Experiment Registry")
st.markdown(
    """
    Central register of all AI experiments — from initial idea through to 
    organisation-wide scaling. Track progress, measure impact, and make 
    evidence-based decisions about what to scale.
    """
)

st.divider()

experiments = load_experiments()

# --- Üst metrikler ---
col1, col2, col3, col4, col5 = st.columns(5)

stage_counts = {}
for exp in experiments:
    s = exp.get("stage", "Pipeline")
    stage_counts[s] = stage_counts.get(s, 0) + 1

with col1:
    st.metric("🔵 Pipeline", stage_counts.get("Pipeline", 0))
with col2:
    st.metric("🟡 In-Flight", stage_counts.get("In-Flight", 0))
with col3:
    st.metric("🟢 Completed", stage_counts.get("Completed", 0))
with col4:
    st.metric("✅ Scaled", stage_counts.get("Scaled", 0))
with col5:
    st.metric("🔴 Stopped", stage_counts.get("Stopped", 0))

st.divider()

# --- Grafikler ---
tab_view, tab_add, tab_detail = st.tabs(
    ["📊 Overview", "➕ Add Experiment", "🔍 Experiment Details"]
)

with tab_view:
    if experiments:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.plotly_chart(
                experiment_pipeline_chart(experiments), use_container_width=True
            )
        with chart_col2:
            st.plotly_chart(
                department_adoption_chart(experiments), use_container_width=True
            )

        st.divider()

        # Filtreler
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            filter_stage = st.multiselect(
                "Filter by Stage:",
                Config.EXPERIMENT_STAGES,
                default=Config.EXPERIMENT_STAGES,
            )
        with filter_col2:
            filter_dept = st.multiselect(
                "Filter by Department:",
                Config.DEPARTMENTS,
                default=Config.DEPARTMENTS,
            )

        filtered = [
            e
            for e in experiments
            if e.get("stage") in filter_stage
            and e.get("department") in filter_dept
        ]

        if filtered:
            df = pd.DataFrame(filtered)
            display_cols = [
                "id", "name", "department", "stage", "risk_level",
                "governance_status", "owner", "participants",
            ]
            available_cols = [c for c in display_cols if c in df.columns]
            st.dataframe(df[available_cols], use_container_width=True, hide_index=True)
        else:
            st.info("No experiments match your filters.")
    else:
        st.info("No experiments yet. Use the 'Add Experiment' tab to create one.")

with tab_add:
    st.markdown("### ➕ Register a New AI Experiment")

    with st.form("new_experiment"):
        form_col1, form_col2 = st.columns(2)

        with form_col1:
            exp_name = st.text_input("Experiment Name *")
            exp_dept = st.selectbox("Department *", Config.DEPARTMENTS)
            exp_owner = st.text_input("Owner / Sponsor *")
            exp_stage = st.selectbox("Current Stage", Config.EXPERIMENT_STAGES)

        with form_col2:
            exp_risk = st.selectbox("Risk Level", Config.RISK_LEVELS)
            exp_tool = st.text_input(
                "AI Tool",
                placeholder="e.g., Microsoft Copilot + Custom Agent",
            )
            exp_participants = st.number_input(
                "Pilot Participants", min_value=0, value=0
            )
            exp_governance = st.selectbox(
                "Governance Status",
                ["Not Started", "Under Review", "Approved", "Suspended"],
            )

        exp_description = st.text_area("Description *", height=100)
        exp_baseline = st.text_input(
            "Baseline Metric",
            placeholder="e.g., Average 8.5 min handling time",
        )
        exp_target = st.text_input(
            "Target Metric",
            placeholder="e.g., Reduce to 5.5 min",
        )
        exp_notes = st.text_area("Notes", height=80)

        submitted = st.form_submit_button("📝 Register Experiment")

        if submitted and exp_name and exp_description and exp_owner:
            new_exp = {
                "id": f"EXP-{str(uuid.uuid4())[:3].upper()}",
                "name": exp_name,
                "department": exp_dept,
                "description": exp_description,
                "stage": exp_stage,
                "owner": exp_owner,
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "risk_level": exp_risk,
                "baseline_metric": exp_baseline,
                "target_metric": exp_target,
                "current_result": "Not yet started",
                "ai_tool": exp_tool,
                "participants": exp_participants,
                "governance_status": exp_governance,
                "notes": exp_notes,
            }
            experiments.append(new_exp)
            save_experiments(experiments)
            st.success(f"✅ Experiment '{exp_name}' registered as {new_exp['id']}")
            st.rerun()

with tab_detail:
    if experiments:
        exp_names = {e["id"]: f"{e['id']} — {e['name']}" for e in experiments}
        selected_id = st.selectbox(
            "Select an experiment:",
            list(exp_names.keys()),
            format_func=lambda x: exp_names[x],
        )

        selected_exp = next((e for e in experiments if e["id"] == selected_id), None)

        if selected_exp:
            st.markdown(f"### {selected_exp['name']}")

            detail_col1, detail_col2 = st.columns(2)

            with detail_col1:
                st.markdown(f"**ID**: `{selected_exp['id']}`")
                st.markdown(f"**Department**: {selected_exp['department']}")
                st.markdown(f"**Owner**: {selected_exp['owner']}")
                st.markdown(f"**Stage**: {selected_exp['stage']}")
                st.markdown(f"**Risk Level**: {selected_exp['risk_level']}")

            with detail_col2:
                st.markdown(f"**AI Tool**: {selected_exp.get('ai_tool', 'N/A')}")
                st.markdown(f"**Participants**: {selected_exp.get('participants', 0)}")
                st.markdown(f"**Governance**: {selected_exp.get('governance_status', 'N/A')}")
                st.markdown(f"**Start Date**: {selected_exp.get('start_date', 'N/A')}")

            st.divider()
            st.markdown(f"**Description**: {selected_exp['description']}")
            st.markdown(f"**Baseline**: {selected_exp.get('baseline_metric', 'N/A')}")
            st.markdown(f"**Target**: {selected_exp.get('target_metric', 'N/A')}")
            st.markdown(f"**Current Result**: {selected_exp.get('current_result', 'N/A')}")
            st.markdown(f"**Notes**: {selected_exp.get('notes', '')}")
    else:
        st.info("No experiments to display.")
```

### `pages/4_📊_ROI_Calculator.py`

```python
import streamlit as st
from utils.metrics import calculate_roi
from config import Config

st.set_page_config(page_title="ROI Calculator", page_icon="📊", layout="wide")
st.title("📊 AI ROI Calculator")
st.markdown(
    """
    Calculate the projected return on investment for AI experiments.
    Tie AI adoption directly to business outcomes and cost savings.
    """
)

st.divider()

st.markdown("### 💰 Calculate Projected Savings")

col1, col2 = st.columns(2)

with col1:
    time_saved = st.slider(
        "Average time saved per employee per week (hours)",
        min_value=0.5,
        max_value=10.0,
        value=2.5,
        step=0.5,
    )
    num_employees = st.number_input(
        "Number of employees using AI tools",
        min_value=1,
        max_value=5000,
        value=50,
    )

with col2:
    hourly_cost = st.number_input(
        "Average fully-loaded hourly cost (AUD)",
        min_value=20.0,
        max_value=150.0,
        value=45.0,
        step=5.0,
    )
    weeks = st.number_input(
        "Number of working weeks per year",
        min_value=40,
        max_value=52,
        value=48,
    )

st.divider()

roi = calculate_roi(time_saved, num_employees, hourly_cost, weeks)

# Sonuç kartları
st.markdown("### 📈 Projected Annual Impact")

res_col1, res_col2, res_col3, res_col4 = st.columns(4)

with res_col1:
    st.metric(
        "Annual Hours Saved",
        f"{roi['annual_hours_saved']:,}",
        delta="across all employees",
    )

with res_col2:
    st.metric(
        "Annual Cost Saving",
        f"AUD {roi['annual_cost_saving_aud']:,}",
        delta="projected",
    )

with res_col3:
    st.metric(
        "Monthly Saving",
        f"AUD {roi['monthly_cost_saving_aud']:,}",
    )

with res_col4:
    st.metric(
        "Hours Saved / Employee / Year",
        f"{roi['per_employee_hours_saved']}",
    )

st.divider()

# Senaryo karşılaştırması
st.markdown("### 🔄 Scenario Comparison")
st.markdown(
    "Compare different AI adoption scales to understand the impact trajectory."
)

scenarios = [
    {"label": "Pilot (10 employees)", "employees": 10, "hours": 2.0},
    {"label": "Department (50 employees)", "employees": 50, "hours": 2.5},
    {"label": "Division (200 employees)", "employees": 200, "hours": 3.0},
    {"label": "Organisation (500 employees)", "employees": 500, "hours": 3.5},
]

scenario_data = []
for s in scenarios:
    r = calculate_roi(s["hours"], s["employees"], hourly_cost, weeks)
    scenario_data.append(
        {
            "Scale": s["label"],
            "Employees": s["employees"],
            "Avg Hours Saved/Week": s["hours"],
            "Annual Hours Saved": f"{r['annual_hours_saved']:,}",
            "Annual Saving (AUD)": f"{r['annual_cost_saving_aud']:,}",
        }
    )

import pandas as pd

st.dataframe(pd.DataFrame(scenario_data), use_container_width=True, hide_index=True)

st.divider()

st.markdown(
    """
    ### 📋 Methodology Notes
    
    - **Time saved** is estimated per-employee based on pilot measurements
    - **Fully-loaded hourly cost** includes salary, benefits, overhead, and facilities
    - **Conservative estimate** — does not include secondary benefits like improved 
      member satisfaction, reduced errors, or faster onboarding
    - ROI should be validated with actual pilot data before scaling decisions
    - All figures in Australian Dollars (AUD)
    """
)
```

### `pages/5_📚_Prompt_Library.py`

```python
import streamlit as st
import pandas as pd
from utils.data_loader import load_prompts, save_prompts
from config import Config
import uuid
from datetime import datetime

st.set_page_config(page_title="Prompt Library", page_icon="📚", layout="wide")
st.title("📚 Prompt Library")
st.markdown(
    """
    Curated, approved prompts for RACV teams. Every prompt is reviewed for 
    effectiveness, safety, and governance compliance before approval.
    """
)

st.divider()

prompts = load_prompts()

# Üst metrikler
approved = len([p for p in prompts if p.get("status") == "Approved"])
under_review = len([p for p in prompts if p.get("status") == "Under Review"])
total_usage = sum(p.get("usage_count", 0) for p in prompts)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Approved Prompts", approved)
with col2:
    st.metric("Under Review", under_review)
with col3:
    st.metric("Total Uses", f"{total_usage:,}")

st.divider()

tab_browse, tab_add = st.tabs(["📖 Browse Prompts", "➕ Submit New Prompt"])

with tab_browse:
    # Filtreler
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    categories = list(set(p.get("category", "Other") for p in prompts))
    departments = list(set(p.get("department", "All") for p in prompts))
    statuses = list(set(p.get("status", "Approved") for p in prompts))

    with filter_col1:
        filter_cat = st.multiselect("Category:", categories, default=categories)
    with filter_col2:
        filter_dept = st.multiselect("Department:", departments, default=departments)
    with filter_col3:
        filter_status = st.multiselect("Status:", statuses, default=statuses)

    filtered = [
        p
        for p in prompts
        if p.get("category") in filter_cat
        and p.get("department") in filter_dept
        and p.get("status") in filter_status
    ]

    for prompt in filtered:
        status_icon = "✅" if prompt.get("status") == "Approved" else "🔄"
        with st.expander(
            f"{status_icon} **{prompt['title']}** — {prompt.get('category', '')} | "
            f"Uses: {prompt.get('usage_count', 0)}"
        ):
            st.markdown(f"**ID**: `{prompt['id']}`")
            st.markdown(f"**Department**: {prompt.get('department', 'All')}")
            st.markdown(f"**Status**: {prompt.get('status', 'N/A')}")
            st.markdown(f"**Use Case**: {prompt.get('use_case', '')}")

            st.divider()

            st.markdown("**📝 Prompt:**")
            st.code(prompt.get("prompt", ""), language="text")

            if prompt.get("tips"):
                st.markdown(f"**💡 Tips**: {prompt['tips']}")
            if prompt.get("governance_notes"):
                st.markdown(f"**🛡️ Governance**: {prompt['governance_notes']}")

            st.caption(
                f"Created by: {prompt.get('created_by', 'Unknown')} | "
                f"Date: {prompt.get('created_date', 'N/A')}"
            )

with tab_add:
    st.markdown("### ➕ Submit a New Prompt for Review")
    st.markdown(
        "All new prompts go through a review process before being approved "
        "for organisation-wide use."
    )

    with st.form("new_prompt"):
        p_title = st.text_input("Prompt Title *")
        p_col1, p_col2 = st.columns(2)

        with p_col1:
            p_category = st.selectbox(
                "Category",
                [
                    "Member Service",
                    "Communication",
                    "Documentation",
                    "Knowledge",
                    "Productivity",
                    "Retention",
                    "Analysis",
                    "Other",
                ],
            )
        with p_col2:
            p_department = st.selectbox("Department", ["All"] + Config.DEPARTMENTS)

        p_prompt = st.text_area("Prompt Text *", height=150)
        p_use_case = st.text_input("Use Case — when should this prompt be used?")
        p_tips = st.text_input("Tips for users")
        p_created_by = st.text_input("Your Name")

        submitted = st.form_submit_button("📤 Submit for Review")

        if submitted and p_title and p_prompt:
            new_prompt = {
                "id": f"PRM-{str(uuid.uuid4())[:3].upper()}",
                "title": p_title,
                "category": p_category,
                "department": p_department,
                "status": "Under Review",
                "prompt": p_prompt,
                "use_case": p_use_case,
                "tips": p_tips,
                "governance_notes": "Pending review",
                "created_by": p_created_by or "Anonymous",
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "usage_count": 0,
            }
            prompts.append(new_prompt)
            save_prompts(prompts)
            st.success(
                f"✅ Prompt '{p_title}' submitted for review as {new_prompt['id']}"
            )
            st.rerun()
```

### `pages/6_🛡️_Governance.py`

```python
import streamlit as st
import pandas as pd
from governance.risk_matrix import create_assessment, COMPLIANCE_CHECKLIST
from governance.compliance_checker import check_compliance
from governance.audit_logger import get_recent_events
from utils.data_loader import load_risk_assessments, save_risk_assessments, load_experiments
from utils.charts import risk_distribution_chart
from config import Config

st.set_page_config(page_title="Governance", page_icon="🛡️", layout="wide")
st.title("🛡️ Responsible AI Governance")
st.markdown(
    """
    Every AI use case at RACV is assessed for risk, compliance, and alignment with 
    Australian AI governance standards before deployment.
    """
)

st.divider()

tab_assess, tab_comply, tab_audit, tab_framework = st.tabs(
    ["⚖️ Risk Assessment", "✅ Compliance Check", "📋 Audit Log", "📜 Framework"]
)

# ---- RISK ASSESSMENT ----
with tab_assess:
    st.markdown("### ⚖️ AI Use Case Risk Assessment")
    st.markdown(
        "Rate each dimension from 1 (lowest risk) to 5 (highest risk). "
        "The system calculates the overall risk level automatically."
    )

    assessments = load_risk_assessments()
    experiments = load_experiments()

    with st.form("risk_assessment"):
        ra_col1, ra_col2 = st.columns(2)

        with ra_col1:
            exp_options = {e["id"]: f"{e['id']} — {e['name']}" for e in experiments}
            ra_experiment = st.selectbox(
                "Experiment *",
                list(exp_options.keys()),
                format_func=lambda x: exp_options.get(x, x),
            ) if experiments else st.text_input("Experiment ID *")

            ra_department = st.selectbox("Department", Config.DEPARTMENTS)
            ra_assessed_by = st.text_input("Assessed By *", value="AI Governance Team")

        with ra_col2:
            st.markdown("**Risk Dimensions** (1 = Low, 5 = High)")
            data_sensitivity = st.slider("Data Sensitivity", 1, 5, 2)
            decision_impact = st.slider("Decision Impact", 1, 5, 2)
            automation_level = st.slider("Automation Level (inverse of human control)", 1, 5, 1)

        ra_col3, ra_col4 = st.columns(2)
        with ra_col3:
            member_facing = st.slider("Member-Facing Exposure", 1, 5, 1)
            reversibility = st.slider("Irreversibility (1=easy to undo, 5=permanent)", 1, 5, 2)
        with ra_col4:
            regulatory_exposure = st.slider("Regulatory Exposure", 1, 5, 2)

        mitigation = st.text_area("Mitigation Notes", height=80)

        submitted = st.form_submit_button("📊 Calculate Risk")

        if submitted:
            exp_name = ""
            if experiments:
                exp_obj = next((e for e in experiments if e["id"] == ra_experiment), None)
                exp_name = exp_obj["name"] if exp_obj else ra_experiment
            else:
                exp_name = ra_experiment

            assessment = create_assessment(
                experiment_id=ra_experiment if isinstance(ra_experiment, str) else "",
                experiment_name=exp_name,
                department=ra_department,
                assessed_by=ra_assessed_by,
                scores={
                    "data_sensitivity": data_sensitivity,
                    "decision_impact": decision_impact,
                    "automation_level": automation_level,
                    "member_facing": member_facing,
                    "reversibility": reversibility,
                    "regulatory_exposure": regulatory_exposure,
                },
                mitigation_notes=mitigation,
            )

            # Sonuç göster
            risk_colors = {
                "Low": "🟢",
                "Medium": "🟡",
                "High": "🟠",
                "Critical": "🔴",
            }

            st.divider()
            st.markdown(f"### Result: {risk_colors[assessment.risk_level]} {assessment.risk_level} Risk")
            st.markdown(f"**Total Score**: {assessment.total_score} / 30")
            st.markdown(f"**Requires Governance Review**: {'Yes ⚠️' if assessment.requires_review else 'No ✅'}")

            # Kaydet
            assessments.append(assessment.to_dict())
            save_risk_assessments(assessments)
            st.success("Assessment saved.")

    # Mevcut değerlendirmeler
    if assessments:
        st.divider()
        st.markdown("### Previous Assessments")
        st.plotly_chart(risk_distribution_chart(assessments), use_container_width=True)

        df = pd.DataFrame(assessments)
        display_cols = [
            "experiment_name", "department", "total_score",
            "risk_level", "requires_review", "assessed_date",
        ]
        available = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available], use_container_width=True, hide_index=True)

# ---- COMPLIANCE CHECK ----
with tab_comply:
    st.markdown("### ✅ Governance Compliance Checklist")
    st.markdown(
        "Check each item that has been completed for your AI use case. "
        "Requirements vary by risk level."
    )

    compliance_risk = st.selectbox(
        "Risk Level of the Use Case:",
        Config.RISK_LEVELS,
    )

    st.divider()

    completed_checks = {}
    for check_id, check_info in COMPLIANCE_CHECKLIST.items():
        if compliance_risk in check_info["required_for"]:
            completed_checks[check_id] = st.checkbox(
                f"**{check_info['label']}** — {check_info['question']}",
                key=f"compliance_{check_id}",
            )

    if st.button("🔍 Check Compliance"):
        result = check_compliance(compliance_risk, completed_checks)

        st.divider()
        st.markdown(f"### {result['status']}")
        st.markdown(f"**Compliance**: {result['compliance_percentage']}%")
        st.markdown(
            f"**Passed**: {result['total_passed']} / {result['total_required']} required checks"
        )

        if result["failed_details"]:
            st.markdown("### ❌ Outstanding Items")
            for item in result["failed_details"]:
                st.warning(f"**{item['label']}**: {item['question']}")

# ---- AUDIT LOG ----
with tab_audit:
    st.markdown("### 📋 AI Usage Audit Log")
    st.markdown("All AI agent interactions are logged for accountability and review.")

    events = get_recent_events(100)

    if events:
        df = pd.DataFrame(events)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No audit events recorded yet. Use the Copilot Agents to generate entries.")

# ---- FRAMEWORK ----
with tab_framework:
    st.markdown("### 📜 Australian AI Governance Framework")
    st.markdown(
        """
        This platform's governance approach is aligned with Australia's regulatory 
        and ethical AI landscape.
        """
    )

    st.markdown("#### Key Regulatory References")
    st.markdown(f"- **{Config.AU_GOVERNANCE['framework']}**")
    st.markdown(f"- **{Config.AU_GOVERNANCE['privacy']}**")
    st.markdown(f"- **{Config.AU_GOVERNANCE['consumer']}**")

    st.divider()

    st.markdown("#### Australia's Eight AI Ethics Principles")
    for i, principle in enumerate(Config.AU_GOVERNANCE["principles"], 1):
        st.markdown(f"{i}. **{principle}**")

    st.divider()

    st.markdown(
        """
        #### How This Platform Implements Responsible AI
        
        | Principle | Implementation |
        |-----------|---------------|
        | Human oversight | All agent outputs are decision support, not decisions |
        | Transparency | Confidence levels shown, sources referenced |
        | Fairness | Use cases tested across member demographics |
        | Privacy | Data minimisation, no unnecessary personal data in prompts |
        | Reliability | Pilot → measure → scale methodology |
        | Contestability | Members can request human review of any AI-influenced decision |
        | Accountability | Full audit trail of all AI interactions |
        | Security | Role-based access, approved prompts, governance reviews |
        """
    )
```

### `pages/7_🎓_Training_Hub.py`

```python
import streamlit as st
from utils.data_loader import load_training_modules

st.set_page_config(page_title="Training Hub", page_icon="🎓", layout="wide")
st.title("🎓 AI Training Hub")
st.markdown(
    """
    Build AI capability across the organisation — from fundamentals to 
    advanced agent building. Every RACV employee can find their learning path here.
    """
)

st.divider()

modules = load_training_modules()

# Seviye filtresi
levels = list(set(m.get("level", "Beginner") for m in modules))
selected_level = st.selectbox("Filter by level:", ["All"] + sorted(levels))

filtered = modules if selected_level == "All" else [
    m for m in modules if m.get("level") == selected_level
]

# Modüller
for module in filtered:
    level_icons = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}
    icon = level_icons.get(module.get("level", ""), "⚪")

    with st.expander(
        f"{icon} **{module['title']}** — {module.get('level', '')} | "
        f"⏱️ {module.get('duration_minutes', 0)} min"
    ):
        st.markdown(f"**{module['description']}**")
        st.markdown(f"**Target Audience**: {module.get('target_audience', 'All')}")
        st.markdown(f"**Status**: {module.get('status', 'Active')}")

        st.divider()

        st.markdown("**Topics Covered:**")
        for topic in module.get("topics", []):
            st.markdown(f"- {topic}")

st.divider()

# CRAFT Framework
st.markdown(
    """
    ## 🎯 The CRAFT Prompting Framework
    
    RACV's recommended approach to writing effective AI prompts:
    
    | Letter | Element | Description | Example |
    |--------|---------|-------------|---------|
    | **C** | Context | Background information about your situation | "I'm a roadside assistance operator..." |
    | **R** | Role | What role you want the AI to play | "Act as a member service expert..." |
    | **A** | Action | What specifically you want done | "Summarise the member's situation..." |
    | **F** | Format | How you want the output structured | "Use bullet points, keep under 100 words..." |
    | **T** | Tone | The voice and style of the output | "Professional and empathetic, Australian English..." |
    
    ### Example Using CRAFT
    
    ```
    CONTEXT: I'm a claims handler processing a home insurance claim for storm damage.
    ROLE: Act as an experienced claims process advisor.
    ACTION: Explain the correct process steps for a storm damage claim with urgent 
    temporary accommodation needs.
    FORMAT: Numbered steps, with required approvals highlighted in bold.
    TONE: Clear, direct, and practical for a busy frontline team member.
    ```
    """
)

st.divider()

# AI kullanımı rehberi
st.markdown(
    """
    ## ✅ When to Use AI / ❌ When Not to Use AI
    
    ### ✅ Good Use Cases
    - Summarising member history before a call
    - Drafting routine email responses (with human review)
    - Finding relevant policy or process information
    - Generating case notes from interaction details
    - Brainstorming approaches to member problems
    - Creating meeting summaries and action items
    
    ### ❌ Do Not Use AI For
    - Making binding financial commitments to members
    - Approving or denying insurance claims
    - Sending communications without human review
    - Processing sensitive personal data unnecessarily
    - Making legal or regulatory interpretations
    - Replacing professional judgement in high-stakes decisions
    
    ### 🤔 Use With Caution (Needs Review)
    - Retention offers or discount recommendations
    - Complex multi-product member advice
    - Anything involving vulnerable members
    - Communications about complaints or disputes
    """
)
```

---

## 7. README.md

```markdown
# 🏢 Moments That Matter — Copilot Command Centre

**AI Adoption Platform for Member-Centric Organisations**

A comprehensive demonstration of how organisations like RACV can adopt 
Microsoft Copilot safely, effectively, and at scale — covering the full 
AI adoption lifecycle from agent development through governance and training.

---

## 🎯 What This Project Demonstrates

This project addresses a real enterprise challenge: how do you move AI adoption 
from individual experimentation to a governed, measured, and scalable programme?

| Capability | What It Shows |
|------------|--------------|
| **Copilot Agents** | 5 task-specific agents for frontline teams |
| **Experiment Registry** | Pipeline → In-Flight → Completed → Scaled tracking |
| **ROI Calculator** | Measurable business impact tied to real KPIs |
| **Prompt Library** | Curated, approved prompts with governance controls |
| **Governance Framework** | Risk assessment aligned with Australian regulations |
| **Training Hub** | Capability building from beginner to advanced |
| **Audit Trail** | Full logging of AI interactions for accountability |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- An OpenAI API key (for agent demos)

### Installation

```bash
git clone https://github.com/yourusername/moments-that-matter.git
cd moments-that-matter
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Run

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
moments-that-matter/
├── app.py                     # Main entry point
├── pages/                     # Streamlit multi-page app
│   ├── Dashboard              # Real-time overview
│   ├── Copilot Agents         # 5 live agent demos
│   ├── Experiment Registry    # AI experiment tracking
│   ├── ROI Calculator         # Business impact calculator
│   ├── Prompt Library         # Curated prompt repository
│   ├── Governance             # Risk assessment & compliance
│   └── Training Hub           # Learning modules & frameworks
├── agents/                    # Copilot agent implementations
├── governance/                # Risk matrix, compliance, audit
├── utils/                     # Shared utilities
└── data/                      # JSON data stores
```

---

## 🤖 Copilot Agents

Five bespoke agents designed for critical member moments:

1. **Member Context Copilot** — Instant member situation briefs
2. **Policy & Process Navigator** — Find the right policy fast
3. **Next Best Action Assistant** — Recommended next steps
4. **Communication Drafter** — Empathetic, on-brand drafts
5. **Prompt Coach** — Help employees use AI better

All agents follow responsible AI principles:
- Outputs are decision **support**, not decisions
- Human review required before action
- Confidence levels indicated
- Sources referenced where possible

---

## 🛡️ Governance Approach

Aligned with Australian AI governance:
- **Australia's Voluntary AI Safety Standard**
- **Privacy Act 1988 (Cth)**
- **Australian Consumer Law**

Features:
- 6-dimension risk assessment matrix
- 8-point compliance checklist
- Full audit trail
- Human-in-the-loop controls
- Data minimisation principles

---

## 📊 Metrics & Measurement

The platform tracks:
- Average Handling Time reduction
- First Contact Resolution improvement
- AI Adoption Rate across teams
- Prompt Reuse Rate
- Compliance Exception Count
- Employee Confidence Score
- Projected ROI at multiple scales

---

## 🎓 Training Framework

**CRAFT Prompting Framework**: Context, Role, Action, Format, Tone

5 training modules from Beginner to Advanced:
1. AI Fundamentals for RACV Teams
2. Prompt Engineering 101
3. Responsible AI at RACV
4. Copilot for Team Leaders
5. Building Custom Copilot Agents

---

## 🏗️ Technology Stack

- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4o (simulating Microsoft Copilot capabilities)
- **Visualisation**: Plotly
- **Data**: JSON (production would use Dataverse/SharePoint)
- **Agent Framework**: Custom Python (maps to Copilot Studio patterns)

---

## 📝 Note

This is a portfolio project demonstrating AI transformation capability. 
In a production RACV environment, these agents would be built in 
**Microsoft Copilot Studio** with **Dataverse** backends, **SharePoint** 
knowledge sources, and full **Microsoft 365** integration.

---

Built by [Your Name] | 2025
```

---

## Projeyi çalıştırmak için

```bash
# 1. Repo'yu oluştur
mkdir moments-that-matter && cd moments-that-matter

# 2. Tüm dosyaları yukarıdaki yapıya göre oluştur

# 3. Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Paketleri kur
pip install -r requirements.txt

# 5. .env dosyasını ayarla
cp .env.example .env
# OPENAI_API_KEY'ini ekle

# 6. data klasörünü oluştur ve JSON dosyalarını koy
mkdir -p data

# 7. Çalıştır
streamlit run app.py
```

---

## Bu proje RACV hiring manager'ına ne söyler?

| İlandaki beklenti | Bu projede karşılığı |
| --- | --- |
| Build bespoke Copilot agents | 5 çalışan agent, gerçek senaryolarla |
| Coach and train employees | Training Hub + CRAFT Framework + Prompt Coach |
| Curate Copilot knowledge repository | Prompt Library + governance kontrollü asset yönetimi |
| Maintain AI experiment register | Pipeline → Scale arası tam experiment tracking |
| Comply with AI policy & regulations | Avustralya'ya özel risk matrix + compliance checklist |
| Support integration into KPIs | ROI Calculator + 10 KPI metrik takibi |
| Internal AI ambassador | Eğitim modülleri + kullanım rehberleri + audit trail |
| Stakeholder engagement | Departman bazlı senaryo tasarımı + çoklu kullanıcı profili |

Bu projeyi GitHub'a koy, Streamlit Cloud'a deploy et, ve 5 dakikalık bir video walkthrough çek. Videoda kod değil, **"bunu bir organizasyonda nasıl hayata geçirirsiniz"** hikayesini anlat. RACV hiring manager'ı teknik detay değil, dönüşüm vizyonu görmek istiyor.