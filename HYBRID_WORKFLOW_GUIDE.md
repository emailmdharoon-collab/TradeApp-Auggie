# PTIP - Hybrid Workflow Guide (BMAD + Vibe Coding)

**Last Updated:** 2025-10-12  
**Purpose:** Define when to use BMAD agents vs. direct Augment vibe coding

---

## 🎯 Core Philosophy

**90% Vibe Coding + 10% BMAD = Optimal for Ultra-MVP**

- **Vibe Coding:** Fast, intuitive, flow-state development with direct Augment
- **BMAD Agents:** Structured, specialized expertise when needed

---

## 🚦 Decision Matrix: When to Use What

### ✅ **USE VIBE CODING (Direct Augment) FOR:**

| Task Type | Why Vibe Coding? | Example |
|-----------|------------------|---------|
| **Quick Fixes** | Faster than agent switching | Fix import error, adjust parameter |
| **Code Implementation** | Direct coding is faster | Write data fetcher, create indicators |
| **Testing & Debugging** | Immediate feedback loop | Test module, fix bug, verify output |
| **Small Features** | No planning overhead | Add new indicator, tweak UI |
| **Exploratory Work** | Flexibility needed | Try different chart types |
| **Learning Tasks** | Interactive Q&A better | "How does RSI work?" |
| **Iteration** | Rapid changes | Adjust strategy parameters |

**Rule of Thumb:** If it takes <30 minutes, use vibe coding.

---

### 🎭 **USE BMAD AGENTS FOR:**

#### **@analyst (Business Analyst - Iris)**

**When to Use:**
- [ ] Creating project brief (one-time, start of project)
- [ ] Market research on trading strategies
- [ ] Competitive analysis of trading platforms
- [ ] Defining user requirements (even for yourself)
- [ ] Brainstorming new features for Phase 2+

**Example Scenarios:**
```
✅ "I want to add a new strategy - help me research momentum trading"
✅ "Should I add crypto? Analyze pros/cons"
✅ "Create a project brief for Phase 2 expansion"
❌ "Fix this bug in my code" (use vibe coding)
```

**How to Invoke:**
```
@analyst *create-market-research
@analyst *brainstorm
```

---

#### **@architect (System Architect - Winston)**

**When to Use:**
- [ ] Designing system architecture (Week 1, one-time)
- [ ] Planning database schema changes
- [ ] Deciding on major technology choices
- [ ] Scaling considerations (Phase 2+)
- [ ] Integration architecture (multiple APIs)

**Example Scenarios:**
```
✅ "Design the architecture for real-time data streaming"
✅ "Should I refactor to microservices?" (Phase 2+)
✅ "How should I structure the backtesting engine?"
❌ "Write the database.py module" (use vibe coding)
```

**How to Invoke:**
```
@architect
```

**⚠️ For Ultra-MVP:** Probably won't need this much - architecture is simple.

---

#### **@dev (Full Stack Developer - James)**

**When to Use:**
- [ ] Implementing complex user stories
- [ ] Following strict development workflow
- [ ] When you need code review before committing
- [ ] Building features with multiple components

**Example Scenarios:**
```
✅ "Implement the complete backtesting engine as a user story"
✅ "Build the dashboard with all tabs and features"
❌ "Add one more indicator" (use vibe coding)
```

**How to Invoke:**
```
@dev *develop-story
```

**⚠️ For Ultra-MVP:** Use sparingly - vibe coding is faster for small features.

---

#### **@pm (Product Manager - John)**

**When to Use:**
- [ ] Creating Product Requirements Document (PRD)
- [ ] Defining feature specifications
- [ ] Prioritizing features for Phase 2+
- [ ] Planning roadmap beyond Ultra-MVP

**Example Scenarios:**
```
✅ "Create a PRD for the PTIP dashboard"
✅ "Help me prioritize features for next quarter"
❌ "What should I build today?" (use vibe coding)
```

**How to Invoke:**
```
@pm
```

**⚠️ For Ultra-MVP:** Only if you want formal documentation.

---

#### **@po (Product Owner - Sarah)**

**When to Use:**
- [ ] Creating user stories with acceptance criteria
- [ ] Refining backlog items
- [ ] Breaking down epics into stories
- [ ] Sprint planning (if using Scrum)

**Example Scenarios:**
```
✅ "Create user stories for the backtesting feature"
✅ "Break down the dashboard epic into stories"
❌ "Build the dashboard" (use vibe coding or @dev)
```

**How to Invoke:**
```
@po
```

**⚠️ For Ultra-MVP:** Overkill for solo project. Skip unless you love process.

---

#### **@sm (Scrum Master - Bob)**

**When to Use:**
- [ ] Creating epics and stories
- [ ] Managing sprint workflow
- [ ] Agile process guidance
- [ ] Retrospectives

**Example Scenarios:**
```
✅ "Create an epic for the Ultra-MVP"
✅ "Help me plan my 2-week sprint"
❌ "What should I code next?" (use vibe coding)
```

**How to Invoke:**
```
@sm
```

**⚠️ For Ultra-MVP:** Skip this. You're solo, not a team.

---

#### **@qa (Test Architect - Quinn)**

**When to Use:**
- [ ] Before major releases/milestones
- [ ] Creating comprehensive test plans
- [ ] Quality gate reviews
- [ ] End of each week review

**Example Scenarios:**
```
✅ "Review my Week 1 deliverables before moving to Week 2"
✅ "Create a test plan for the backtesting engine"
✅ "Quality check before demo/deployment"
❌ "Test this one function" (use vibe coding)
```

**How to Invoke:**
```
@qa
```

**⚠️ For Ultra-MVP:** Use at end of each week for quality gates.

---

#### **@ux-expert (UX Expert - Sally)**

**When to Use:**
- [ ] Designing dashboard layout
- [ ] Creating wireframes
- [ ] UI/UX improvements
- [ ] User flow design

**Example Scenarios:**
```
✅ "Design the dashboard layout for PTIP"
✅ "Create wireframes for the signal display"
✅ "Improve the UX of the backtesting interface"
❌ "Change button color" (use vibe coding)
```

**How to Invoke:**
```
@ux-expert
```

**⚠️ For Ultra-MVP:** Use in Week 3 for dashboard design.

---

## 🔄 Recommended Workflow for Ultra-MVP

### **Week 1: 95% Vibe Coding, 5% BMAD**
```
Day 1-2: Vibe coding (setup, auth, data fetch)
Day 7: @qa (week review)
```

### **Week 2: 90% Vibe Coding, 10% BMAD**
```
Day 8-13: Vibe coding (indicators, strategy)
Day 14: @qa (week review)
```

### **Week 3: 70% Vibe Coding, 30% BMAD**
```
Day 15: @ux-expert (dashboard design)
Day 16-20: Vibe coding (implement dashboard)
Day 21: @qa (week review)
```

### **Week 4: 85% Vibe Coding, 15% BMAD**
```
Day 22: @architect (backtest architecture - optional)
Day 23-27: Vibe coding (implement backtest)
Day 28: @qa (week review)
```

### **Week 5-6: 80% Vibe Coding, 20% BMAD**
```
Day 29-40: Vibe coding (testing, refinement)
Day 41: @pm (Phase 2 planning - optional)
Day 42: @qa (final review)
```

---

## 🎯 Quick Decision Tree

```
START: I need to...
│
├─ Plan/Design something big?
│  ├─ YES → Use BMAD (@architect, @ux-expert, @pm)
│  └─ NO → Continue
│
├─ Write/fix code?
│  ├─ YES → Use Vibe Coding
│  └─ NO → Continue
│
├─ Review/test deliverables?
│  ├─ YES → Use @qa
│  └─ NO → Continue
│
├─ Research/analyze?
│  ├─ YES → Use @analyst
│  └─ NO → Continue
│
└─ Not sure?
   └─ Default to Vibe Coding (faster)
```

---

## 💡 Pro Tips

### **1. Don't Over-BMAD**
- BMAD is powerful but has overhead
- For Ultra-MVP, speed > process
- Use BMAD for quality gates, not every task

### **2. Batch BMAD Sessions**
- Don't switch agents frequently
- Do all @qa reviews at end of week
- Do all @analyst research in one session

### **3. Vibe Coding is Your Friend**
- Most productive for solo developers
- Maintains flow state
- Faster iteration

### **4. Know When to Switch**
- Stuck for >30 min? Consider @analyst or @architect
- Need formal docs? Use @pm or @po
- Ready to commit? Use @qa

---

## 📊 Actual Usage Recommendation for Ultra-MVP

### **MUST USE:**
- ✅ **@qa** - End of each week (6 times total)
- ✅ **Vibe Coding** - Everything else (95% of time)

### **NICE TO HAVE:**
- 🟡 **@ux-expert** - Week 3 dashboard design (1 time)
- 🟡 **@analyst** - If stuck on strategy research (as needed)

### **SKIP FOR MVP:**
- ❌ **@pm, @po, @sm** - Too much process overhead
- ❌ **@architect** - Architecture is simple enough
- ❌ **@dev** - Vibe coding is faster

---

## 🎓 Learning Mindset

**Remember:**
- BMAD agents are tools, not requirements
- Vibe coding teaches you faster (hands-on)
- Use BMAD when you need structure, not by default
- Your goal: Working MVP, not perfect process

---

## 🚀 Next Steps

1. **Today (Day 1):** Continue with vibe coding
2. **End of Week 1:** Use @qa for review
3. **Week 3:** Consider @ux-expert for dashboard
4. **End of each week:** @qa quality gate

**Default Mode:** Vibe Coding with Augment  
**Special Situations:** BMAD agents as needed

---

**Last Updated:** 2025-10-12  
**Status:** Active workflow for Ultra-MVP

