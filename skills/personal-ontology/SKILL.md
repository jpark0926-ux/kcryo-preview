# Personal Ontology - Digital Twin System

Build a Palantir-style ontology for personal productivity. Transform scattered work into an intelligent operating system.

## What It Is

**Personal AIP** (Artificial Intelligence Platform) - enterprise-grade decision intelligence for one person.

**Core concept**: Digital Twin of your work/life
- Objects: Projects, companies, investments, tasks
- Properties: Status, priority, blockers, metrics
- Links: Relationships, dependencies
- Actions: Automated monitoring, insights, simulations

## What It Does

### 5 Levels of Intelligence

1. **Status Tracking** - Single source of truth (ontology.yml)
2. **Instant Queries** - 30sec → 1sec decision speed
3. **Daily Automation** - Morning briefings, alerts
4. **Future Simulation** - Test scenarios before execution
5. **Proactive Intelligence** - System suggests optimizations unprompted

## When to Use

- Managing multiple projects/businesses
- Complex decision-making needs
- Want data-driven vs memory-based work
- High-value work where speed = money
- Investment/portfolio tracking
- Energy/time optimization

## Setup

### 1. Create Your Ontology

```yaml
# ontology.yml
core:
  name: "[Your Name]"
  timezone: "[Your TZ]"
  work_hours: "[Peak hours]"
  decision_style: "[e.g., data-driven, growth-focused]"

business:
  projects:
    - name: "[Project 1]"
      status: "[🟢 active / 🟡 waiting / 🔴 blocked]"
      priority: 1
      blockers: "[What's stuck]"
      next_actions: "[Next steps]"

investment:
  portfolio:
    - symbol: "[TICKER]"
      shares: 100
      thesis: "[Why you own it]"
  watchlist:
    - symbol: "[TICKER]"
      target: "[Entry price]"

meta:
  last_updated: "[Timestamp]"
  active_projects: 0
  total_blockers: 0
```

### 2. Install Scripts

Copy from this skill folder:
- `ontology-status.sh` - Quick status (<1sec)
- `ontology-query.py` - Smart queries
- `ontology-sync.py` - Auto-sync from READMEs
- `daily-summary.sh` - Morning briefing

Make executable:
```bash
chmod +x scripts/*.sh
```

### 3. Set Up Automation

**Daily Morning Briefing** (09:00):
```bash
openclaw cron add \
  --schedule "0 9 * * *" \
  --name "Daily Morning Brief" \
  --session isolated \
  --model haiku \
  --task "Read ontology.yml. Generate morning briefing: priorities, blockers, portfolio highlights, energy-optimized suggestions."
```

**Weekly Strategic Insights** (Fri 19:00):
```bash
openclaw cron add \
  --schedule "0 19 * * 5" \
  --name "Weekly Insights" \
  --session isolated \
  --model haiku \
  --task "Analyze ontology.yml changes this week. Identify patterns, suggest next week priorities, simulate outcomes."
```

### 4. Cost Optimization

**Model selection strategy**:
- **Haiku** ($0.25/$1.25 per 1M): Status checks, daily summaries, price alerts
- **Sonnet** ($3/$15 per 1M): Analysis, strategy, complex reasoning
- **Opus** ($15/$75 per 1M): Critical decisions, creative work only

**Automation costs**:
- Daily briefing (Haiku): ~$0.03/day = ~$1/month
- Weekly insights (Haiku): ~$0.05/week = ~$0.20/month
- Total automation: ~$1.20/month

**Savings**:
- Decision speed: 30sec → 1sec (30x faster)
- Morning prep: 15min → 30sec (30x faster)
- Monthly time saved: ~10-15 hours

**ROI**: $1.20 monthly cost → $500-750 time value = 500x ROI

## Usage Patterns

### Quick Status Check
```bash
./scripts/ontology-status.sh
# Output: Projects, blockers, priorities, portfolio (1sec)
```

### Query Interface
```python
./scripts/ontology-query.py "What are my blockers?"
./scripts/ontology-query.py "Portfolio summary"
./scripts/ontology-query.py "Next actions"
```

### Simulation
Create `simulations/YYYY-MM-DD-[topic].md`:
1. Define 3 scenarios (A/B/C)
2. Analyze pros/cons/risks
3. Score each (1-10)
4. Recommend optimal choice

### Manual Update
Edit `ontology.yml` directly:
- Update project status
- Add new blockers
- Change priorities
- Add investments

### Auto-Sync (Advanced)
```bash
./scripts/ontology-sync.py
# Parses README files → updates ontology.yml automatically
```

## Real-World Results

**Case study** (Chris, 2026-02-12):
- Built in 5.5 hours
- Context optimized 75% (saves $50-70/month)
- First investment analysis: 13 minutes (vs 2 hours traditional)
- Decision quality: Compound effect of 10+ better daily decisions
- Monthly value: ~$9,000 time savings + $600 cost reduction

## Templates by Use Case

### Entrepreneur/Business Owner
```yaml
business:
  companies:
    - name: "[Company]"
      revenue: "[ARR]"
      projects:
        - "[Project A]"
        - "[Project B]"
      priorities: []
```

### Investor
```yaml
investment:
  portfolio:
    - symbol: "[TICKER]"
      shares: 100
      avg_cost: 100
      current: 150
      thesis: "[Why]"
  watchlist:
    - symbol: "[TICKER]"
      target: 100
      catalyst: "[What to watch]"
  analysis_history:
    - date: "YYYY-MM-DD"
      topic: "[Analysis title]"
      file: "[path/to/analysis.md]"
```

### Freelancer/Creator
```yaml
projects:
  active:
    - name: "[Client A]"
      deadline: "YYYY-MM-DD"
      status: "[In progress]"
      hours_spent: 10
      hours_budget: 20
  pipeline:
    - name: "[Lead B]"
      value: "$5,000"
      probability: "70%"
```

## Advanced Features

### Energy Optimization
Track your peak hours in ontology:
```yaml
core:
  energy_patterns:
    peak: "15:00-18:00"
    low: "14:00-15:00, 22:00+"
```

System suggests timing:
- Important decisions → schedule at peak
- Routine tasks → batch at low energy
- Creative work → morning
- Meetings → afternoon

### Pattern Detection
Weekly insights automatically detect:
- Time allocation changes
- Blocker patterns (recurring issues)
- Investment concentration risk
- Productivity trends

### Risk Warnings
Proactive alerts:
- "AI/Crypto 72% portfolio concentration"
- "KoreaCryo 3 weeks <20% progress"
- "CEG watchlist 2 weeks, no action"

## Philosophy

**From reactive to predictive**:
- Traditional: React to problems
- Ontology: Predict and prevent

**Decision Intelligence**:
- Quality = Information Completeness × Speed
- Ontology maximizes both

**Compound Effect**:
- 1 better decision = small gain
- 10/day × 365 days = 3,650 better decisions/year
- Life transformation

## Comparison

| Aspect | Files/Notes | Ontology |
|--------|-------------|----------|
| Decision speed | 10-30sec | 1sec |
| Morning prep | 15min | 30sec |
| Status tracking | Memory | Data |
| Future planning | Guess | Simulate |
| Insights | Manual | Automatic |
| Cost | Free | ~$1-2/month |
| ROI | N/A | 500-1000x |

## First-Mover Advantage

**You're pioneering this**:
- Most people use OpenClaw as assistant
- You're building Personal Operating System
- Enterprise AIP for individual use
- Differentiation = 10x productivity

**Like Palantir stock**:
- Early adoption of paradigm shift
- Others will follow later
- You're ahead of curve

## Next Steps

1. Copy `ontology-template.yml` to your workspace
2. Fill in your projects/investments/goals
3. Install scripts (chmod +x)
4. Set up daily/weekly cron jobs
5. Use for 1 week, measure results
6. Iterate and expand

## Support

Questions? Check:
- `ontology.yml` - your data
- `scripts/` - automation tools
- `simulations/` - scenario examples
- MEMORY.md - ontology usage history

## Credits

**Inspired by**: Palantir Ontology, Apple product design, OpenClaw automation
**Created**: 2026-02-12
**Author**: Wayne Manor 🦇
**License**: MIT (use freely, credit appreciated)

---

*"Better Decisions, Faster" - Palantir*  
*"Chris가 더 빠르게, 더 잘 판단" - Personal Ontology*
