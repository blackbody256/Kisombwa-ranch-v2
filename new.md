# KRIS Technical Brief - Team Implementation Guide
**Kisombwa Ranch Intelligence System**

---

## 🎯 STRATEGIC PIVOT

**Changed:** IoT Hardware (ESP32 collars) → Record-Keeping + RFID Automation  
**Reason:** No baseline data exists. Need structured records before predictions.  
**Timeline:** 48 hours

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌──────────────────────────────────────────────────────┐
│         FLUTTER MOBILE APP (Herdsmen)                │
│  • Offline-first SQLite storage                      │
│  • Forms: Animal, Breeding, Vaccination, Treatment   │
│  • Auto-sync when online                             │
└───────────────────┬──────────────────────────────────┘
                    │ REST API
┌───────────────────▼──────────────────────────────────┐
│            DJANGO BACKEND (Python)                    │
│  • PostgreSQL (event-based schema)                   │
│  • REST API (DRF)                                     │
│  • Business logic & analytics                        │
└───────────────────┬──────────────────────────────────┘
                    │ Queries
┌───────────────────▼──────────────────────────────────┐
│         WEB DASHBOARD (Manager)                       │
│  • Breeding Performance Analyzer                     │
│  • Health vs. Breeding Correlations                  │
│  • Financial ROI Tracking                            │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│      RFID GATE SCANNER (Optional Hardware)           │
│  • Raspberry Pi + RFID Reader                        │
│  • Automated counting                                │
│  • POST to /api/rfid/scan/                           │
└──────────────────────────────────────────────────────┘
```

---

## 📊 DATABASE SCHEMA (13 Tables)

### **Core Tables**
1. `users` - Authentication (extends AbstractUser)
2. `ranches` - Multi-ranch support
3. `staff` - Herdsmen/vets (accountability)
4. `animals` - **PRIMARY KEY = `tag_number`** (ranch's natural ID)
5. `sync_queue` - Offline operation tracking

### **Event Tables** (Event-based architecture)
6. `vaccinations` - Every vaccination event
7. `treatments` - Every treatment event
8. `mortality` - Death events
9. `breeding_events` - Every breeding attempt & outcome
10. `herd_counts` - Manual counting logs
11. `rfid_scan_logs` - Automated RFID scans
12. `movement_logs` - Pasture movements

### **Analytics**
13. `system_metrics` - Pre-calculated dashboard metrics

### **Key Design Decisions**
- Natural primary keys (ranch's tag numbering: BORAN001, etc.)
- Species-agnostic (cattle/goat/sheep in one table)
- Self-referencing animals (dam/sire foreign keys)
- Offline-first ready (sync_queue table)

---

## 👥 TEAM ROLES & DELIVERABLES

### **MEMBER 5 (Backend Lead) - DevOps**

**Responsibilities:**
- Django project setup
- PostgreSQL configuration
- All 13 models implemented
- Migrations executed
- REST API endpoints
- Deployment

**Deliverables:**
```
✓ Django apps structure:
  - apps/core/
  - apps/animals/
  - apps/health/
  - apps/breeding/
  - apps/operations/
  - apps/analytics/

✓ API Endpoints:
  POST /api/animals/
  GET  /api/animals/{tag}/
  POST /api/breeding/
  POST /api/vaccinations/
  POST /api/treatments/
  POST /api/mortality/
  POST /api/sync/
  POST /api/rfid/scan/

✓ Admin panel configured
✓ Seed data (20+ animals, breeding events, health records)
✓ Deployed backend (Heroku/Railway)
✓ API documentation (Postman collection)
```

**Tech Stack:**
- Django 4.2+
- Django REST Framework
- PostgreSQL 14+
- django-cors-headers
- Token authentication

---

### **MEMBER 1 (Mobile Developer) - Flutter App**

**Responsibilities:**
- Offline-first mobile application
- Local SQLite database
- REST API integration
- Sync management

**Deliverables:**
```
✓ 4 Core Forms:
  1. Animal Registration
     - Input: tag_number, species, breed, sex, date_of_birth
     - Photo upload
     - Offline save
  
  2. Breeding Event
     - Search female by tag
     - Select male
     - Service date, method
     - Pregnancy status update
  
  3. Vaccination
     - Animal lookup
     - Vaccine type, date
     - Next due date
  
  4. Treatment
     - Animal lookup
     - Diagnosis, medication
     - Treatment date

✓ Features:
  - Local SQLite storage
  - Offline queue management
  - Auto-sync when online
  - Search animals by tag
  - Form validation

✓ Deliverable: APK file for Android
```

**Tech Stack:**
- Flutter 3.x
- sqflite (local database)
- http package (REST API)
- Provider/Riverpod (state management)

**SQLite Schema (Mirror Django):**
```sql
CREATE TABLE animals (
    tag_number TEXT PRIMARY KEY,
    species TEXT NOT NULL,
    breed TEXT,
    sex TEXT NOT NULL,
    date_of_birth TEXT,
    synced INTEGER DEFAULT 0
);

CREATE TABLE breeding_events (
    id TEXT PRIMARY KEY,
    female_tag TEXT NOT NULL,
    male_tag TEXT,
    service_date TEXT NOT NULL,
    synced INTEGER DEFAULT 0
);

CREATE TABLE sync_queue (
    id TEXT PRIMARY KEY,
    operation TEXT NOT NULL,
    table_name TEXT NOT NULL,
    record_data TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    synced INTEGER DEFAULT 0
);
```

---

### **MEMBER 3 (Frontend Developer) - Analytics Dashboard**

**Responsibilities:**
- Web dashboard for manager
- Data visualization
- Breeding performance analyzer
- Financial ROI tracking

**Deliverables:**
```
✓ Dashboard Pages:

  1. Breeding Performance Analyzer (CRITICAL)
     ┌─────────────────────────────────────────────┐
     │ Comparison: Imported vs. Local              │
     ├─────────────────────────────────────────────┤
     │ Metric              | Imported | Local      │
     │ Conception Rate     | 35%      | 75%        │
     │ Stillbirth Rate     | 12%      | 4%         │
     │ Calf Survival       | 85%      | 95%        │
     ├─────────────────────────────────────────────┤
     │ Root Cause: 5/8 bulls incomplete vacc       │
     │ Correlation: -85% conception rate           │
     │ Recommendation: Complete vaccination series │
     └─────────────────────────────────────────────┘
  
  2. Health Correlation Charts
     - Vaccination compliance % vs. Conception rate
     - Disease events vs. Breeding success
     - Chart.js line/bar charts
  
  3. Herd Overview KPIs
     - Total animals by species
     - Active alerts count
     - Recent mortality
     - Vaccination overdue count
  
  4. Financial Performance
     - Cost per animal
     - Revenue per animal (calves × value)
     - ROI calculation

✓ Features:
  - Responsive design (desktop focus)
  - Real-time data from Django API
  - Export reports (PDF optional)
  - Alert notifications UI
```

**Tech Stack:**
- Django Templates + Bootstrap 5 OR
- React/Vue + Chart.js/Plotly
- Tailwind CSS (optional)

**Key Queries:**
```python
# Breeding performance by source
Animal.objects.filter(source='imported').annotate(
    conception_rate=Count('breeding_as_dam', filter=Q(breeding_as_dam__pregnancy_confirmed='yes')) / Count('breeding_as_dam')
)

# Vaccination correlation
animals_with_complete_vacc = subquery
animals_with_incomplete_vacc = subquery
Compare conception rates
```

---

### **MEMBER 4 (Data Analyst) - Analytics Engine**

**Responsibilities:**
- Correlation analysis
- Automated insights generation
- Alert logic
- Report generation

**Deliverables:**
```
✓ Analytics Scripts:

  1. Correlation Finder
     def analyze_breeding_factors():
         return {
             'vaccination_impact': {
                 'complete': 0.75,  # 75% conception
                 'incomplete': 0.12  # 12% conception
             },
             'health_impact': {...},
             'weight_impact': {...}
         }
  
  2. Alert Generator (Celery Task)
     - Check overdue vaccinations
     - Check pending pregnancy confirmations
     - Check count discrepancies
     - Create Alert records
  
  3. Metric Calculator (Nightly Job)
     - Calculate conception rates
     - Calculate mortality rates
     - Store in system_metrics table
  
  4. Report Generator
     - PDF: Breeding performance report
     - Excel: Herd inventory
     - CSV: Vaccination schedule

✓ Management Commands:
  - python manage.py calculate_metrics
  - python manage.py generate_alerts
  - python manage.py export_report --type=breeding
```

**Tech Stack:**
- Python (pandas, numpy)
- Django management commands
- Celery + Redis (scheduled tasks)
- ReportLab (PDF) or WeasyPrint

**Key Algorithms:**
```python
# Vaccination vs. Conception Correlation
complete_vacc_animals = get_animals_with_complete_vaccination()
incomplete_vacc_animals = get_animals_with_incomplete_vaccination()

complete_conception_rate = calculate_conception_rate(complete_vacc_animals)
incomplete_conception_rate = calculate_conception_rate(incomplete_vacc_animals)

correlation_strength = complete_conception_rate - incomplete_conception_rate
# Result: 0.63 (63% difference = strong correlation)
```

---

### **MEMBER 2 (Hardware/IoT) - RFID System**

**Responsibilities:**
- RFID gate scanner implementation
- Automated counting system
- API integration

**Deliverables:**
```
✓ RFID System:

  Option A: Raspberry Pi Prototype
    - Raspberry Pi 4
    - 134.2kHz RFID reader
    - Python script to read tags
    - POST to /api/rfid/scan/
  
  Option B: Simulation
    - Python script generating fake scans
    - Demo video explaining system
    - Cost-benefit analysis document

✓ API Integration:
  POST /api/rfid/scan/
  {
      "rfid_code": "123456789012",
      "gate_id": "GATE_MAIN",
      "scan_timestamp": "2025-02-18T14:30:00Z",
      "signal_strength": 85
  }

✓ Daily Count Aggregation:
  - Query unique rfid_codes scanned per day
  - Compare to expected active animal count
  - Generate alert if difference > threshold

✓ Documentation:
  - Hardware recommendation (with costs)
  - Installation guide
  - Maintenance plan
```

**Tech Stack:**
- Raspberry Pi 4 + RFID reader OR
- Arduino + RFID shield
- Python (RPi.GPIO, serial)
- requests library (API calls)

**Hardware Options:**
```
Option 1: DIY ($200)
  - Raspberry Pi 4: $50
  - RFID reader module: $80
  - 4G USB modem: $40
  - Power supply: $20
  - Weatherproof case: $10

Option 2: Commercial ($500-800)
  - Allflex RS420 or similar
  - Pre-built, rugged
```

---

## 🔗 API SPECIFICATION

### **Authentication**
```
POST /api/auth/login/
{
    "username": "herdsman",
    "password": "password123"
}

Response:
{
    "token": "abc123...",
    "user": {
        "id": "uuid",
        "username": "herdsman",
        "role": "herdsman"
    }
}
```

### **Animal CRUD**
```
POST /api/animals/
{
    "tag_number": "BORAN001",
    "species": "cattle",
    "breed": "Boran",
    "sex": "female",
    "date_of_birth": "2022-03-15",
    "source": "born"
}

GET /api/animals/BORAN001/
Response:
{
    "tag_number": "BORAN001",
    "species": "cattle",
    "breed": "Boran",
    "sex": "female",
    "date_of_birth": "2022-03-15",
    "source": "born",
    "status": "active",
    "age_months": 23,
    "dam_tag": "BORAN_DAM_001",
    "sire_tag": "BORAN_SIRE_001"
}
```

### **Breeding Event**
```
POST /api/breeding/
{
    "female_tag": "BORAN001",
    "male_tag": "BORAN_BULL_002",
    "service_date": "2025-01-15",
    "method": "natural",
    "pregnancy_confirmed": "pending"
}
```

### **Vaccination**
```
POST /api/vaccinations/
{
    "animal_tag": "BORAN001",
    "vaccine_type": "FMD",
    "date_administered": "2025-02-01",
    "next_due_date": "2025-08-01",
    "administered_by_id": "staff_uuid"
}
```

### **Sync Offline Data**
```
POST /api/sync/
{
    "device_id": "flutter_device_001",
    "operations": [
        {
            "operation": "create",
            "table_name": "breeding_events",
            "record_data": {...},
            "timestamp": "2025-02-18T10:00:00Z"
        },
        {
            "operation": "create",
            "table_name": "vaccinations",
            "record_data": {...},
            "timestamp": "2025-02-18T10:05:00Z"
        }
    ]
}

Response:
{
    "synced": 2,
    "failed": 0,
    "errors": []
}
```

---

## 📅 48-HOUR TIMELINE

### **Day 1: Hours 0-24**

**H0-4: Setup**
- Member 5: Django models, migrations
- Member 1: Flutter project + SQLite
- Member 3: Dashboard wireframes
- Member 4: Data analysis plan
- Member 2: RFID research

**H4-12: Core Development**
- Member 5: API endpoints functional
- Member 1: Animal registration form working
- Member 3: Basic dashboard + KPIs
- Member 4: Correlation analysis script
- Member 2: RFID prototype/simulation

**H12-24: Integration**
- Member 1: Flutter → Django API integration
- Member 3: Dashboard connected to real data
- Member 4: First insights generated
- Member 5: Deployment to staging
- Member 2: RFID demo working

### **Day 2: Hours 24-48**

**H24-36: Feature Completion**
- Member 1: All 4 forms + offline sync
- Member 3: Breeding analyzer complete
- Member 4: Automated alerts
- Member 2: RFID counting demo
- Member 5: Production deployment

**H36-42: Testing & Polish**
- Integration testing
- Bug fixes
- UI/UX improvements
- Load realistic demo data

**H42-48: Demo Preparation**
- Demo script
- Presentation slides
- Practice run
- Backup video

---

## 🎯 DEMO FLOW (5 Minutes)

**1. Problem (30s)**
- Manager's quote: "$40,000 investment not breeding"
- No data = Guesswork decisions

**2. Mobile App (90s)**
- Record breeding event offline
- Record vaccination
- Auto-sync when online

**3. Dashboard (120s)**
- Show breeding analyzer
- Reveal: "Imported 35% vs Local 75%"
- Show root cause: "Incomplete vaccinations"
- Show recommendation: "Complete series → Recover $15,000"

**4. RFID Automation (60s)**
- Gate scanner demo
- Automated counting
- Missing animal detection

**5. Impact (30s)**
- Financial recovery calculation
- Differentiation vs. CattleMax

---

## ✅ PRIORITY MATRIX

### **MUST HAVE (P0)**
- [ ] Flutter app with 4 forms working
- [ ] Django backend with all tables
- [ ] Breeding analyzer dashboard
- [ ] Offline sync functional
- [ ] Demo data loaded

### **SHOULD HAVE (P1)**
- [ ] RFID system (prototype or simulation)
- [ ] Automated alerts
- [ ] Health correlation charts
- [ ] Financial ROI display

### **NICE TO HAVE (P2)**
- [ ] PDF reports
- [ ] Advanced charts
- [ ] User management
- [ ] Email/SMS notifications

### **CAN SKIP**
- [ ] Complex permissions
- [ ] Advanced UI animations
- [ ] Multi-language support
- [ ] Mobile iOS version

---

## 🔧 TECH STACK SUMMARY

### **Backend**
```
Django 4.2+
Django REST Framework 3.14+
PostgreSQL 14+
Celery + Redis (optional for scheduled tasks)
django-cors-headers
```

### **Frontend (Dashboard)**
```
Django Templates + Bootstrap 5 OR
React 18+ + Tailwind CSS
Chart.js or Plotly
Axios (if React)
```

### **Mobile**
```
Flutter 3.x
sqflite (local database)
http package
provider/riverpod (state management)
```

### **Hardware**
```
Raspberry Pi 4 OR Arduino
RFID Reader (134.2kHz)
Python (RPi.GPIO, serial, requests)
```

### **DevOps**
```
Git + GitHub
Heroku or Railway (deployment)
Postman (API testing)
```

---

## 📊 SUCCESS METRICS

Judges should see:
1. ✓ Working mobile app (offline-first)
2. ✓ Breeding analyzer showing correlation
3. ✓ Root cause insight: "Incomplete vacc = 85% lower"
4. ✓ Financial impact: "$15,000 recovery opportunity"
5. ✓ RFID automation demo

---

## 🚨 CRITICAL INTEGRATION POINTS

**Flutter ↔ Django:**
- API contract (Member 1 + Member 5)
- Test with Postman first
- Handle offline queue sync

**Dashboard ↔ Django:**
- SQL queries (Member 3 + Member 5)
- Chart data format
- Real-time updates (polling or WebSocket)

**Analytics ↔ Dashboard:**
- Insights JSON format (Member 4 + Member 3)
- Store in system_metrics table
- Display on dashboard

**RFID ↔ Django:**
- API endpoint contract (Member 2 + Member 5)
- RFID scan format
- Daily aggregation logic

---

## 📝 COMMUNICATION PROTOCOL

**Daily Standups:**
- Morning (9 AM): Plan
- Evening (6 PM): Progress + Blockers

**Tools:**
- Slack/Discord: Quick communication
- GitHub: Code + Issues
- Postman: API testing
- Google Docs: Shared notes

**Code Review:**
- PRs required for main branch
- At least 1 reviewer
- Merge daily to avoid conflicts

---

## 🎓 KEY DOCUMENTATION

All team members have access to:
- [x] KRIS Database Schema (complete)
- [x] Django Models (copy-paste ready)
- [x] API Endpoint Specifications
- [x] Flutter SQLite Schema
- [x] Demo Script
- [ ] Postman Collection (Member 5 to create)

---

## 🚀 START NOW

**Member 5:** Begin Django setup  
**Member 1:** Initialize Flutter project  
**Member 3:** Design dashboard wireframes  
**Member 4:** Research correlation algorithms  
**Member 2:** Research RFID hardware  

**Timeline starts: NOW**  
**First integration checkpoint: Hour 12**  
**Demo rehearsal: Hour 42**  
**Final presentation: Hour 48**