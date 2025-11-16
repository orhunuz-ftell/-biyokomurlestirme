# Documentation Directory

This folder contains all technical documentation for the Reverse ML Bio-oil to Product project.

---

## Process Documentation

### Steam Reforming Process

1. **steam_reforming_process_description.md** (16 pages)
   - Complete technical specification of steam reforming
   - Equipment details, reactions, operating conditions
   - Mass and energy balance calculations
   - Use: Understand the process before modeling

2. **steam_reforming_simple_summary.md** (5 pages)
   - Simplified overview of steam reforming
   - Key concepts in plain language
   - Use: Quick introduction to the process

3. **process_flowsheet_diagram.txt**
   - ASCII flowsheet diagram
   - Stream names and connections
   - Use: Visual reference while building simulation

4. **PROCESS_SELECTION_EVALUATION.md**
   - Evaluation of 5 bio-oil utilization processes
   - Grading criteria and selection rationale
   - Why steam reforming was chosen
   - Use: Background on process selection decision

---

## Aspen Simulation Guides

### **NEW: ASPEN_SIMULATION_GUIDE.md** (Complete Guide)
**95+ pages | Step-by-step instructions**

**Contents**:
- Process flowsheet design
- Component selection and property methods
- Block-by-block construction instructions
- Stream specifications
- Python COM automation code
- Database integration
- Troubleshooting guide

**Use**: Follow this guide to build the Aspen simulation from scratch and automate it

**Key Sections**:
1. Overview and objectives
2. Flowsheet design (9 blocks, 13 streams)
3. Step-by-step construction
4. Testing & validation procedures
5. Python automation setup
6. Aspen tree paths reference
7. Troubleshooting common issues
8. Full automation workflow with database

### **NEW: ASPEN_QUICK_REFERENCE.md** (Quick Card)
**5 pages | Essential info at a glance**

**Contents**:
- Process flowsheet summary
- Block configuration table
- Typical operating conditions
- Expected results
- Essential Python code snippets
- Common tree paths
- Database storage mapping
- Quick troubleshooting fixes

**Use**: Keep this open while building/automating the simulation for quick reference

---

## When to Use Each Document

### Starting the Project?
1. Read `steam_reforming_simple_summary.md` (overview)
2. Read `steam_reforming_process_description.md` (details)
3. Review `PROCESS_SELECTION_EVALUATION.md` (why this process)

### Building Aspen Simulation?
1. Open `ASPEN_SIMULATION_GUIDE.md` (follow step-by-step)
2. Keep `ASPEN_QUICK_REFERENCE.md` handy (quick lookups)
3. Refer to `process_flowsheet_diagram.txt` (visual reference)

### Automating with Python?
1. Start with automation section in `ASPEN_SIMULATION_GUIDE.md`
2. Use code snippets from `ASPEN_QUICK_REFERENCE.md`
3. Integrate with database using examples provided

### Troubleshooting?
1. Check troubleshooting section in `ASPEN_SIMULATION_GUIDE.md`
2. Use quick fixes table in `ASPEN_QUICK_REFERENCE.md`

---

## Document Status

| Document | Status | Date | Pages |
|----------|--------|------|-------|
| steam_reforming_process_description.md | Complete | 2025-11-16 | 16 |
| steam_reforming_simple_summary.md | Complete | 2025-11-16 | 5 |
| process_flowsheet_diagram.txt | Complete | 2025-11-16 | 1 |
| PROCESS_SELECTION_EVALUATION.md | Complete | 2025-11-16 | 8 |
| ASPEN_SIMULATION_GUIDE.md | **NEW** | 2025-11-16 | 95+ |
| ASPEN_QUICK_REFERENCE.md | **NEW** | 2025-11-16 | 5 |

---

## Related Documentation

### Project Root
- `PROJECT_SPECIFICATION.md` - Overall project methodology
- `README.md` - Project overview
- `QUICK_START_GUIDE.md` - 10-step getting started guide

### Specs Folder (`../specs/`)
- `IMPLEMENTATION_PLAN_DB_AND_ASPEN.md` - Phases 1-3 implementation plan (150+ pages)
- `QUICK_REFERENCE.md` - Implementation quick guide
- `README.md` - Specs folder index

### Database Folder (`../database/`)
- `01_create_tables.sql` - Database schema for 5 new tables
- `02_create_indexes.sql` - 21 indexes for performance
- `03_create_views.sql` - 4 views for ML and monitoring
- `04_test_schema.sql` - Test and validation script

### Scripts Folder (`../scripts/phase2_data_prep/`)
- `extract_biooil_data.py` - Extract 26 bio-oil compositions
- `analyze_biooil_statistics.py` - Statistical analysis
- `generate_doe_matrix.py` - Create 45 process conditions
- `create_simulation_matrix.py` - Generate 1,170 simulation scenarios

---

## Quick Navigation

**Need to understand the process?**
→ Start with `steam_reforming_simple_summary.md`

**Ready to build Aspen simulation?**
→ Follow `ASPEN_SIMULATION_GUIDE.md`

**Working on automation?**
→ Keep `ASPEN_QUICK_REFERENCE.md` open

**Need troubleshooting help?**
→ Check both guides (detailed + quick fixes)

**Looking for implementation plan?**
→ See `../specs/IMPLEMENTATION_PLAN_DB_AND_ASPEN.md`

---

**Last Updated**: 2025-11-16
**Project Status**: Phase 1 & 2 Complete | Phase 3 Ready (Aspen guides created)

