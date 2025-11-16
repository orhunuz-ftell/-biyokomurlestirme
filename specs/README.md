# Project Specifications

This folder contains detailed specifications and implementation plans for the Reverse ML Bio-oil project.

---

## 📚 Documents

### 1. **IMPLEMENTATION_PLAN_DB_AND_ASPEN.md** (Main Document)
**150+ pages | Comprehensive technical specification**

Complete implementation plan covering:
- Phase 1: Database Extension (5 new tables, views, indexes)
- Phase 2: Reference Data Preparation (DOE matrix, data extraction)
- Phase 3: Aspen Automation & Data Collection (1,350 simulations)

Includes:
- Detailed SQL schemas
- Python code templates
- Validation procedures
- Risk assessment
- 3-week timeline
- Full deliverables checklist

**When to use**: Before starting implementation, for detailed technical reference

---

### 2. **QUICK_REFERENCE.md** (Quick Guide)
**10 pages | Executive summary**

Fast reference with:
- Phase summaries
- Key commands
- File structure
- Common issues & solutions
- Execution sequence
- Pre-flight checklist

**When to use**: During implementation, for quick lookups

---

## 🎯 Project Overview

**Objective**: Build reverse ML system where:
- **Input**: H₂ product properties from Aspen simulation
- **Output**: Required bio-oil composition (to predict)

**Approach**:
1. Extend database with simulation result tables
2. Extract 30 bio-oil compositions, create 1,350 simulation scenarios
3. Automate Aspen to generate training data
4. Train ML models (Phase 4 - future)

---

## 📊 Scope of This Specification

**Covered (Phases 1-3)**:
- ✅ Database schema design
- ✅ Data preparation methodology
- ✅ Aspen automation workflow
- ✅ Quality validation procedures

**Not Covered (Phase 4)**:
- ❌ ML model training
- ❌ Model evaluation
- ❌ Prediction tool development

---

## 🚀 Next Steps

1. **Review** both documents thoroughly
2. **Approve** implementation plan
3. **Begin Phase 1**: Database extension
4. **Track progress** against milestones in implementation plan

---

## 📁 Related Files

Main implementation plan references these locations:

```
C:\@biyokomurlestirme\
├── specs/                                    ← Current location
│   ├── README.md
│   ├── IMPLEMENTATION_PLAN_DB_AND_ASPEN.md  ← Main spec
│   └── QUICK_REFERENCE.md                    ← Quick guide
│
├── reverse_ml_biooil_to_product/
│   ├── docs/                                 ← Process documentation
│   │   ├── steam_reforming_process_description.md
│   │   ├── steam_reforming_simple_summary.md
│   │   ├── process_flowsheet_diagram.txt
│   │   ├── PROCESS_SELECTION_EVALUATION.md
│   │   └── process_selection_template.md
│   │
│   ├── PROJECT_SPECIFICATION.md              ← Original project spec
│   ├── README.md                             ← Project readme
│   └── QUICK_START_GUIDE.md                 ← Getting started
│
└── .claude.md                                ← Database connection info
```

---

## 📝 Document Status

| Document | Version | Status | Last Updated |
|----------|---------|--------|--------------|
| IMPLEMENTATION_PLAN_DB_AND_ASPEN.md | 1.0 | Draft | 2025-11-16 |
| QUICK_REFERENCE.md | 1.0 | Draft | 2025-11-16 |

**Approval Status**: ⏳ Pending

---

## ✉️ Contact

**Project Lead**: Orhun Uzdiyem
**Advisor**: Prof. Dr. Hayati OLGUN
**Institution**: Ege University - Solar Energy Institute

For questions or clarifications about these specifications, contact the project team.

---

**Last Updated**: 2025-11-16
