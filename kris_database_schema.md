# Kisombwa Ranch Intelligence System (KRIS)
## Complete Database Schema - Event-Based Architecture

**Strategic Shift:** Record Keeping First → Analytics → Automation Later

---

## 🎯 DESIGN PRINCIPLES

1. **Event-Based Data Model** - All changes are events, not properties
2. **Species-Agnostic** - Supports cattle, goats, sheep without schema changes
3. **Natural Primary Keys** - Use ranch's existing tag numbering system
4. **Offline-First Ready** - Structure supports local storage + sync
5. **Accountability Built-In** - Track who recorded what
6. **Extensible** - Easy to add feed, weight, finance tracking later

---

## 📊 DATABASE SCHEMA

### **App Structure:**
```
apps/
├── core/           # Users, Staff, Ranch
├── animals/        # Animal registry
├── breeding/       # Breeding & reproduction events
├── health/         # Vaccinations, treatments, mortality
├── operations/     # Daily logs, counting, movements
└── analytics/      # Reports, dashboards, insights
```

---

## 🗂️ CORE TABLES

### Table: `users`
**Purpose:** System authentication & authorization  
**Django App:** `apps/core/models.py` → `User`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal system ID |
| username | VARCHAR(150) | UNIQUE, NOT NULL | Login username |
| email | VARCHAR(254) | UNIQUE | Email address |
| password | VARCHAR(128) | NOT NULL | Hashed password |
| role | VARCHAR(20) | NOT NULL | manager/vet/herdsman/admin |
| phone_number | VARCHAR(20) | - | Mobile contact |
| is_active | BOOLEAN | DEFAULT true | Account active |
| created_at | TIMESTAMP | NOT NULL | Account creation |
| updated_at | TIMESTAMP | NOT NULL | Last update |

**Indexes:**
- PRIMARY KEY: `id`
- UNIQUE: `username`, `email`

**Notes:**
- Extends Django's AbstractUser
- Role choices: `manager`, `vet`, `herdsman`, `admin`
- `is_active` for soft account deactivation

---

### Table: `ranches`
**Purpose:** Multi-ranch support (future-proof)  
**Django App:** `apps/core/models.py` → `Ranch`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal system ID |
| name | VARCHAR(200) | NOT NULL | Ranch name |
| location | VARCHAR(200) | - | Physical location |
| size_hectares | DECIMAL(10,2) | - | Ranch size |
| owner_id | UUID | FOREIGN KEY → users.id | Ranch owner |
| created_at | TIMESTAMP | NOT NULL | Record creation |
| updated_at | TIMESTAMP | NOT NULL | Last update |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `owner_id` → `users(id)` ON DELETE CASCADE

---

### Table: `staff`
**Purpose:** Herdsmen, workers (accountability tracking)  
**Django App:** `apps/core/models.py` → `Staff`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal system ID |
| user_id | UUID | FOREIGN KEY → users.id, NULL | Linked user account (optional) |
| ranch_id | UUID | FOREIGN KEY → ranches.id | Associated ranch |
| name | VARCHAR(200) | NOT NULL | Full name |
| role | VARCHAR(50) | NOT NULL | herdsman/vet/supervisor |
| phone_number | VARCHAR(20) | - | Contact number |
| is_active | BOOLEAN | DEFAULT true | Currently employed |
| hire_date | DATE | - | Employment start |
| created_at | TIMESTAMP | NOT NULL | Record creation |
| updated_at | TIMESTAMP | NOT NULL | Last update |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `user_id` → `users(id)` ON DELETE SET NULL
- FOREIGN KEY: `ranch_id` → `ranches(id)` ON DELETE CASCADE

**Notes:**
- Not all staff need user accounts (herdsmen might just be recorded)
- `user_id` nullable allows tracking staff who don't log in to system

---

## 🐄 ANIMAL REGISTRY

### Table: `animals`
**Purpose:** Single source of truth for animal identity (STATIC DATA ONLY)  
**Django App:** `apps/animals/models.py` → `Animal`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| tag_number | VARCHAR(50) | PRIMARY KEY | Ranch's ear tag number (e.g., BORAN001) |
| rfid_code | VARCHAR(100) | UNIQUE, INDEXED, NULL | RFID/EID chip code |
| qr_code | VARCHAR(100) | UNIQUE, NULL | Optional QR code |
| ranch_id | UUID | FOREIGN KEY → ranches.id | Associated ranch |
| species | VARCHAR(20) | NOT NULL | cattle/goat/sheep |
| breed | VARCHAR(100) | - | Breed name |
| sex | VARCHAR(10) | NOT NULL | male/female |
| date_of_birth | DATE | - | Birth date (or estimated) |
| source | VARCHAR(20) | NOT NULL | born/purchased/imported |
| dam_tag | VARCHAR(50) | FOREIGN KEY → animals.tag_number, NULL | Mother's tag |
| sire_tag | VARCHAR(50) | FOREIGN KEY → animals.tag_number, NULL | Father's tag |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'active' | active/sold/dead/missing |
| photo | VARCHAR(255) | - | Path to animal photo |
| purchase_price | DECIMAL(10,2) | - | Purchase cost (if bought) |
| purchase_date | DATE | - | Date acquired |
| notes | TEXT | - | Additional notes |
| created_at | TIMESTAMP | NOT NULL | Record creation |
| updated_at | TIMESTAMP | NOT NULL | Last update |

**Indexes:**
- PRIMARY KEY: `tag_number`
- UNIQUE INDEX: `rfid_code`
- FOREIGN KEY: `ranch_id` → `ranches(id)` ON DELETE CASCADE
- FOREIGN KEY: `dam_tag` → `animals(tag_number)` ON DELETE SET NULL
- FOREIGN KEY: `sire_tag` → `animals(tag_number)` ON DELETE SET NULL
- INDEX: `species`, `status`

**Critical Design Decisions:**

✅ **Primary Key = `tag_number`** (Natural key, ranch's naming convention)  
✅ **RFID separate from tag** (Some animals tagged but not RFID'd)  
✅ **Species-agnostic** (One table for cattle/goats/sheep)  
✅ **Self-referencing** (Dam/Sire point to same table)  
✅ **Status field** (Never delete animals, mark as sold/dead)  

**IMPORTANT:** This table contains ONLY static/slowly-changing data. NO pregnancy status, NO vaccination dates, NO treatment history.

---

## 🔬 HEALTH MANAGEMENT

### Table: `vaccinations`
**Purpose:** Every vaccination event  
**Django App:** `apps/health/models.py` → `Vaccination`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| animal_tag | VARCHAR(50) | FOREIGN KEY → animals.tag_number | Animal vaccinated |
| vaccine_type | VARCHAR(100) | NOT NULL | Vaccine name |
| disease_targeted | VARCHAR(100) | - | Disease prevented |
| date_administered | DATE | NOT NULL, INDEXED | Vaccination date |
| administered_by_id | UUID | FOREIGN KEY → staff.id, NULL | Who gave vaccine |
| next_due_date | DATE | INDEXED | Next dose due |
| batch_number | VARCHAR(50) | - | Vaccine batch |
| location | VARCHAR(50) | - | Injection site |
| cost | DECIMAL(10,2) | - | Cost per dose |
| notes | TEXT | - | Additional notes |
| recorded_by_id | UUID | FOREIGN KEY → users.id | Who logged this |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `animal_tag` → `animals(tag_number)` ON DELETE CASCADE
- FOREIGN KEY: `administered_by_id` → `staff(id)` ON DELETE SET NULL
- FOREIGN KEY: `recorded_by_id` → `users(id)` ON DELETE SET NULL
- COMPOSITE INDEX: `(animal_tag, date_administered DESC)`
- INDEX: `next_due_date` (for alert generation)

**Analytics Enabled:**
- Vaccination coverage % by vaccine type
- Missed vaccinations (next_due_date < today)
- Vaccination cost tracking
- Correlation with breeding/health outcomes

---

### Table: `treatments`
**Purpose:** Disease diagnosis & treatment events  
**Django App:** `apps/health/models.py` → `Treatment`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| animal_tag | VARCHAR(50) | FOREIGN KEY → animals.tag_number | Animal treated |
| diagnosis | VARCHAR(200) | - | Disease/condition |
| symptoms | TEXT | - | Observed symptoms |
| medication_given | VARCHAR(200) | - | Medication name |
| dosage | VARCHAR(100) | - | Dosage administered |
| treatment_date | DATE | NOT NULL, INDEXED | Treatment date |
| treated_by_id | UUID | FOREIGN KEY → staff.id, NULL | Vet/herdsman who treated |
| follow_up_required | BOOLEAN | DEFAULT false | Needs follow-up? |
| follow_up_date | DATE | - | Scheduled follow-up |
| cost | DECIMAL(10,2) | - | Treatment cost |
| notes | TEXT | - | Additional notes |
| recorded_by_id | UUID | FOREIGN KEY → users.id | Who logged this |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `animal_tag` → `animals(tag_number)` ON DELETE CASCADE
- FOREIGN KEY: `treated_by_id` → `staff(id)` ON DELETE SET NULL
- FOREIGN KEY: `recorded_by_id` → `users(id)` ON DELETE SET NULL
- COMPOSITE INDEX: `(animal_tag, treatment_date DESC)`

**Analytics Enabled:**
- Disease frequency analysis
- Treatment cost per animal
- Correlation: Disease history → Breeding performance
- Common illnesses by season/breed

---

### Table: `mortality`
**Purpose:** Death events (CRITICAL for loss tracking)  
**Django App:** `apps/health/models.py` → `Mortality`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| animal_tag | VARCHAR(50) | FOREIGN KEY → animals.tag_number | Deceased animal |
| death_date | DATE | NOT NULL, INDEXED | Date of death |
| age_at_death_months | INTEGER | - | Auto-calculated from DOB |
| cause | VARCHAR(200) | - | Known cause or "Unknown" |
| vet_confirmed | BOOLEAN | DEFAULT false | Vet autopsy done? |
| carcass_disposed | BOOLEAN | DEFAULT false | Disposed safely? |
| estimated_value | DECIMAL(10,2) | - | Financial loss |
| notes | TEXT | - | Circumstances |
| recorded_by_id | UUID | FOREIGN KEY → users.id | Who logged this |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `animal_tag` → `animals(tag_number)` ON DELETE CASCADE
- FOREIGN KEY: `recorded_by_id` → `users(id)` ON DELETE SET NULL
- INDEX: `death_date`

**Trigger:**
When mortality record created → Update `animals.status = 'dead'`

**Analytics Enabled:**
- Overall mortality rate %
- Calf mortality rate (age < 12 months)
- Adult mortality rate
- Cause distribution (pie chart)
- Financial loss estimation

---

## 👶 BREEDING & REPRODUCTION

### Table: `breeding_events`
**Purpose:** Track every breeding attempt (SOLVES MANAGER'S PROBLEM)  
**Django App:** `apps/breeding/models.py` → `BreedingEvent`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| female_tag | VARCHAR(50) | FOREIGN KEY → animals.tag_number | Dam |
| male_tag | VARCHAR(50) | FOREIGN KEY → animals.tag_number, NULL | Sire (if natural) |
| semen_batch_id | VARCHAR(100) | - | AI semen batch |
| heat_detected_date | DATE | - | Estrus observed |
| service_date | DATE | NOT NULL, INDEXED | Breeding/AI date |
| method | VARCHAR(20) | NOT NULL | natural/artificial_insemination |
| pregnancy_confirmed | VARCHAR(20) | DEFAULT 'pending' | yes/no/pending |
| pregnancy_check_date | DATE | - | Confirmation date |
| expected_delivery_date | DATE | INDEXED | Auto-calculated from species gestation |
| actual_delivery_date | DATE | - | Actual calving date |
| outcome | VARCHAR(30) | - | live_birth/stillbirth/abortion/failed_conception |
| number_of_offspring | INTEGER | DEFAULT 1 | Important for goats (twins/triplets) |
| offspring_tags | TEXT | - | Comma-separated tag numbers |
| notes | TEXT | - | Breeding notes |
| recorded_by_id | UUID | FOREIGN KEY → users.id | Who logged this |
| created_at | TIMESTAMP | NOT NULL | Record creation |
| updated_at | TIMESTAMP | NOT NULL | Last update |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `female_tag` → `animals(tag_number)` ON DELETE CASCADE
- FOREIGN KEY: `male_tag` → `animals(tag_number)` ON DELETE SET NULL
- FOREIGN KEY: `recorded_by_id` → `users(id)` ON DELETE SET NULL
- COMPOSITE INDEX: `(female_tag, service_date DESC)`
- INDEX: `expected_delivery_date`

**Gestation Periods (Auto-calculate expected_delivery_date):**
- Cattle: 283 days (9 months)
- Goats: 150 days (5 months)
- Sheep: 147 days (5 months)

**Analytics Enabled (CRITICAL FOR MANAGER):**
- **Conception Rate:** % of breedings resulting in pregnancy
- **Calving Rate:** % of pregnancies resulting in live birth
- **Stillbirth Rate:** % of deliveries that are stillborn
- **Abortion Rate:** % of pregnancies ending in abortion
- **Average Calving Interval:** Days between successive calvings
- **Performance by Breed:** Imported vs. Local comparison
- **Performance by Bull:** Which sires most productive
- **Correlation Analysis:** Vaccination status vs. conception rate

---

## 📍 OPERATIONS & COUNTING

### Table: `herd_counts`
**Purpose:** Daily/periodic herd counting (detect missing/stolen animals)  
**Django App:** `apps/operations/models.py` → `HerdCount`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| ranch_id | UUID | FOREIGN KEY → ranches.id | Ranch counted |
| count_date | DATE | NOT NULL, INDEXED | Count date |
| species | VARCHAR(20) | NOT NULL | cattle/goat/sheep |
| expected_count | INTEGER | NOT NULL | System-calculated active animals |
| actual_count | INTEGER | NOT NULL | Physical count |
| difference | INTEGER | - | Auto-calculated (actual - expected) |
| grazing_zone | VARCHAR(100) | - | Where counted |
| notes | TEXT | - | Discrepancies noted |
| counted_by_id | UUID | FOREIGN KEY → staff.id, NULL | Who counted |
| recorded_by_id | UUID | FOREIGN KEY → users.id | Who logged this |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `ranch_id` → `ranches(id)` ON DELETE CASCADE
- FOREIGN KEY: `counted_by_id` → `staff(id)` ON DELETE SET NULL
- FOREIGN KEY: `recorded_by_id` → `users(id)` ON DELETE SET NULL
- COMPOSITE INDEX: `(ranch_id, count_date DESC)`

**Alerts Triggered:**
- If `difference < 0` → Animals missing
- If `|difference| > 5` → Major discrepancy

**Analytics Enabled:**
- Count accuracy over time
- Missing animal trends
- Theft detection

---

### Table: `rfid_scan_logs`
**Purpose:** RFID gate scanner events (automated counting)  
**Django App:** `apps/operations/models.py` → `RFIDScanLog`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| rfid_code | VARCHAR(100) | INDEXED, NOT NULL | RFID chip code scanned |
| animal_tag | VARCHAR(50) | FOREIGN KEY → animals.tag_number, NULL | Resolved animal |
| gate_id | VARCHAR(50) | - | Gate/scanner identifier |
| scan_timestamp | TIMESTAMP | NOT NULL, INDEXED | Exact scan time |
| direction | VARCHAR(10) | - | in/out (if gate has direction detection) |
| signal_strength | INTEGER | - | RFID signal quality |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `animal_tag` → `animals(tag_number)` ON DELETE SET NULL
- INDEX: `rfid_code`
- COMPOSITE INDEX: `(gate_id, scan_timestamp DESC)`

**How It Works:**
1. RFID gate scanner reads chip
2. Sends data to system (via API or local sync)
3. System matches `rfid_code` → `animals.rfid_code` → resolves `tag_number`
4. Log created with timestamp
5. Daily aggregation generates automated herd counts

**Analytics Enabled:**
- Automated daily count (unique animals scanned)
- Animal movement patterns
- Gate usage statistics
- Identify animals not scanned (potentially missing)

---

### Table: `movement_logs`
**Purpose:** Manual pasture movement tracking  
**Django App:** `apps/operations/models.py` → `MovementLog`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| animal_tag | VARCHAR(50) | FOREIGN KEY → animals.tag_number, NULL | Animal moved (null if group move) |
| group_name | VARCHAR(100) | - | Group identifier if moving multiple |
| from_zone | VARCHAR(100) | - | Origin pasture/zone |
| to_zone | VARCHAR(100) | NOT NULL | Destination pasture/zone |
| movement_date | DATE | NOT NULL, INDEXED | Movement date |
| reason | VARCHAR(200) | - | Why moved (rotation, treatment, etc.) |
| moved_by_id | UUID | FOREIGN KEY → staff.id, NULL | Who moved them |
| recorded_by_id | UUID | FOREIGN KEY → users.id | Who logged this |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `animal_tag` → `animals(tag_number)` ON DELETE CASCADE
- FOREIGN KEY: `moved_by_id` → `staff(id)` ON DELETE SET NULL
- FOREIGN KEY: `recorded_by_id` → `users(id)` ON DELETE SET NULL
- INDEX: `movement_date`

**Use Cases:**
- Pasture rotation tracking
- Quarantine movements
- Treatment pen movements

---

## 📊 ANALYTICS & INSIGHTS

### Table: `system_metrics`
**Purpose:** Pre-calculated metrics for dashboard (performance optimization)  
**Django App:** `apps/analytics/models.py` → `SystemMetric`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| ranch_id | UUID | FOREIGN KEY → ranches.id | Ranch |
| metric_type | VARCHAR(100) | NOT NULL | E.g., "conception_rate_imported" |
| metric_value | DECIMAL(10,2) | NOT NULL | Calculated value |
| calculation_date | DATE | NOT NULL | When calculated |
| metadata | JSONB | - | Additional context |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `ranch_id` → `ranches(id)` ON DELETE CASCADE
- COMPOSITE INDEX: `(ranch_id, metric_type, calculation_date DESC)`

**Metric Types:**
- `conception_rate_overall`
- `conception_rate_imported`
- `conception_rate_local`
- `mortality_rate_overall`
- `mortality_rate_calf`
- `vaccination_coverage`
- `active_animal_count`

**How It Works:**
- Celery scheduled task runs nightly
- Calculates expensive aggregations
- Stores results in this table
- Dashboard reads pre-calculated values (fast)

---

## 🔄 SYNC INFRASTRUCTURE (Offline-First Support)

### Table: `sync_queue`
**Purpose:** Track pending offline operations  
**Django App:** `apps/core/models.py` → `SyncQueue`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| device_id | VARCHAR(100) | NOT NULL | Device identifier |
| user_id | UUID | FOREIGN KEY → users.id | User who created record |
| operation | VARCHAR(20) | NOT NULL | create/update/delete |
| table_name | VARCHAR(100) | NOT NULL | Target table |
| record_data | JSONB | NOT NULL | Serialized record |
| timestamp | TIMESTAMP | NOT NULL | When operation created |
| synced | BOOLEAN | DEFAULT false | Successfully synced? |
| synced_at | TIMESTAMP | - | When synced |
| error_message | TEXT | - | Sync error if failed |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Indexes:**
- PRIMARY KEY: `id`
- FOREIGN KEY: `user_id` → `users(id)` ON DELETE CASCADE
- COMPOSITE INDEX: `(device_id, synced, timestamp)`

**How Flutter Uses This:**
1. User records breeding event offline
2. Flutter saves to local SQLite
3. Creates entry in local `sync_queue`
4. When internet available, Flutter sends queued operations to Django API
5. Django processes, creates real records
6. Marks `sync_queue.synced = true`
7. Flutter deletes from local queue

---

## 🎯 COMPLETE DJANGO MODELS CODE

### File: `apps/core/models.py`

```python
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Ranch Manager'),
        ('vet', 'Veterinarian'),
        ('herdsman', 'Herdsman'),
        ('admin', 'System Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='herdsman')
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'

class Ranch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    size_hectares = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_ranches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ranches'
        verbose_name_plural = 'Ranches'
    
    def __str__(self):
        return self.name

class Staff(models.Model):
    ROLE_CHOICES = [
        ('herdsman', 'Herdsman'),
        ('vet', 'Veterinarian'),
        ('supervisor', 'Supervisor'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_profile')
    ranch = models.ForeignKey(Ranch, on_delete=models.CASCADE, related_name='staff')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    hire_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'staff'
    
    def __str__(self):
        return f"{self.name} ({self.role})"

class SyncQueue(models.Model):
    OPERATION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sync_operations')
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    table_name = models.CharField(max_length=100)
    record_data = models.JSONField()
    timestamp = models.DateTimeField()
    synced = models.BooleanField(default=False)
    synced_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sync_queue'
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['device_id', 'synced', 'timestamp']),
        ]
```

### File: `apps/animals/models.py`

```python
import uuid
from django.db import models
from apps.core.models import Ranch

class Animal(models.Model):
    SPECIES_CHOICES = [
        ('cattle', 'Cattle'),
        ('goat', 'Goat'),
        ('sheep', 'Sheep'),
    ]
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    SOURCE_CHOICES = [
        ('born', 'Born on Ranch'),
        ('purchased', 'Purchased'),
        ('imported', 'Imported'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('dead', 'Dead'),
        ('missing', 'Missing'),
    ]
    
    # NATURAL PRIMARY KEY - Ranch's tag number
    tag_number = models.CharField(max_length=50, primary_key=True)
    
    # Optional identification methods
    rfid_code = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    qr_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    # Core attributes
    ranch = models.ForeignKey(Ranch, on_delete=models.CASCADE, related_name='animals')
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    
    # Lineage (self-referencing)
    dam_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='offspring_as_dam')
    sire_tag = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='offspring_as_sire')
    
    # Status & metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    photo = models.ImageField(upload_to='animals/', blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'animals'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['species', 'status']),
        ]
    
    def __str__(self):
        return f"{self.tag_number} ({self.species})"
    
    @property
    def age_months(self):
        if not self.date_of_birth:
            return None
        from datetime import date
        today = date.today()
        return (today.year - self.date_of_birth.year) * 12 + today.month - self.date_of_birth.month
```

### File: `apps/health/models.py`

```python
import uuid
from django.db import models
from apps.animals.models import Animal
from apps.core.models import User, Staff

class Vaccination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    animal_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', related_name='vaccinations')
    vaccine_type = models.CharField(max_length=100)
    disease_targeted = models.CharField(max_length=100, blank=True)
    date_administered = models.DateField(db_index=True)
    administered_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='vaccinations_administered')
    next_due_date = models.DateField(null=True, blank=True, db_index=True)
    batch_number = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='vaccination_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vaccinations'
        ordering = ['-date_administered']
        indexes = [
            models.Index(fields=['animal_tag', '-date_administered']),
        ]

class Treatment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    animal_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', related_name='treatments')
    diagnosis = models.CharField(max_length=200, blank=True)
    symptoms = models.TextField(blank=True)
    medication_given = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=100, blank=True)
    treatment_date = models.DateField(db_index=True)
    treated_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='treatments_administered')
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='treatment_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'treatments'
        ordering = ['-treatment_date']
        indexes = [
            models.Index(fields=['animal_tag', '-treatment_date']),
        ]

class Mortality(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    animal_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', related_name='mortality_record')
    death_date = models.DateField(db_index=True)
    age_at_death_months = models.IntegerField(null=True, blank=True)
    cause = models.CharField(max_length=200, blank=True)
    vet_confirmed = models.BooleanField(default=False)
    carcass_disposed = models.BooleanField(default=False)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mortality_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'mortality'
        ordering = ['-death_date']
    
    def save(self, *args, **kwargs):
        # Auto-calculate age at death
        if self.animal_tag.date_of_birth:
            from dateutil.relativedelta import relativedelta
            delta = relativedelta(self.death_date, self.animal_tag.date_of_birth)
            self.age_at_death_months = delta.years * 12 + delta.months
        
        # Update animal status
        self.animal_tag.status = 'dead'
        self.animal_tag.save()
        
        super().save(*args, **kwargs)
```

### File: `apps/breeding/models.py`

```python
import uuid
from django.db import models
from datetime import timedelta
from apps.animals.models import Animal
from apps.core.models import User

class BreedingEvent(models.Model):
    METHOD_CHOICES = [
        ('natural', 'Natural Service'),
        ('artificial_insemination', 'Artificial Insemination'),
    ]
    PREGNANCY_CHOICES = [
        ('pending', 'Pending'),
        ('yes', 'Confirmed Pregnant'),
        ('no', 'Not Pregnant'),
    ]
    OUTCOME_CHOICES = [
        ('live_birth', 'Live Birth'),
        ('stillbirth', 'Stillbirth'),
        ('abortion', 'Abortion'),
        ('failed_conception', 'Failed Conception'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    female_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', related_name='breeding_as_dam')
    male_tag = models.ForeignKey(Animal, on_delete=models.SET_NULL, to_field='tag_number', null=True, blank=True, related_name='breeding_as_sire')
    semen_batch_id = models.CharField(max_length=100, blank=True)
    
    # Breeding timeline
    heat_detected_date = models.DateField(null=True, blank=True)
    service_date = models.DateField(db_index=True)
    method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    
    # Pregnancy tracking
    pregnancy_confirmed = models.CharField(max_length=20, choices=PREGNANCY_CHOICES, default='pending')
    pregnancy_check_date = models.DateField(null=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True, db_index=True)
    
    # Outcome tracking
    actual_delivery_date = models.DateField(null=True, blank=True)
    outcome = models.CharField(max_length=30, choices=OUTCOME_CHOICES, blank=True)
    number_of_offspring = models.IntegerField(default=1)
    offspring_tags = models.TextField(blank=True)  # Comma-separated
    
    # Metadata
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='breeding_records')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'breeding_events'
        ordering = ['-service_date']
        indexes = [
            models.Index(fields=['female_tag', '-service_date']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-calculate expected delivery date based on species
        if self.service_date and not self.expected_delivery_date:
            gestation_days = {
                'cattle': 283,
                'goat': 150,
                'sheep': 147,
            }
            days = gestation_days.get(self.female_tag.species, 283)
            self.expected_delivery_date = self.service_date + timedelta(days=days)
        
        super().save(*args, **kwargs)
```

### File: `apps/operations/models.py`

```python
import uuid
from django.db import models
from apps.core.models import Ranch, User, Staff
from apps.animals.models import Animal

class HerdCount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ranch = models.ForeignKey(Ranch, on_delete=models.CASCADE, related_name='herd_counts')
    count_date = models.DateField(db_index=True)
    species = models.CharField(max_length=20)
    expected_count = models.IntegerField()
    actual_count = models.IntegerField()
    difference = models.IntegerField()
    grazing_zone = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    counted_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='counts_performed')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='count_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'herd_counts'
        ordering = ['-count_date']
        indexes = [
            models.Index(fields=['ranch', '-count_date']),
        ]
    
    def save(self, *args, **kwargs):
        self.difference = self.actual_count - self.expected_count
        super().save(*args, **kwargs)

class RFIDScanLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfid_code = models.CharField(max_length=100, db_index=True)
    animal_tag = models.ForeignKey(Animal, on_delete=models.SET_NULL, to_field='tag_number', null=True, blank=True, related_name='rfid_scans')
    gate_id = models.CharField(max_length=50, blank=True)
    scan_timestamp = models.DateTimeField(db_index=True)
    direction = models.CharField(max_length=10, blank=True)  # in/out
    signal_strength = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rfid_scan_logs'
        ordering = ['-scan_timestamp']
        indexes = [
            models.Index(fields=['gate_id', '-scan_timestamp']),
        ]

class MovementLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    animal_tag = models.ForeignKey(Animal, on_delete=models.CASCADE, to_field='tag_number', null=True, blank=True, related_name='movements')
    group_name = models.CharField(max_length=100, blank=True)
    from_zone = models.CharField(max_length=100, blank=True)
    to_zone = models.CharField(max_length=100)
    movement_date = models.DateField(db_index=True)
    reason = models.CharField(max_length=200, blank=True)
    moved_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='movements_performed')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='movement_records')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'movement_logs'
        ordering = ['-movement_date']
```

### File: `apps/analytics/models.py`

```python
import uuid
from django.db import models
from apps.core.models import Ranch

class SystemMetric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ranch = models.ForeignKey(Ranch, on_delete=models.CASCADE, related_name='metrics')
    metric_type = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=10, decimal_places=2)
    calculation_date = models.DateField()
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'system_metrics'
        ordering = ['-calculation_date']
        indexes = [
            models.Index(fields=['ranch', 'metric_type', '-calculation_date']),
        ]
```

---

## 🚀 SETUP GUIDE FOR MEMBER 5

### Step 1: Update Django Settings

**File: `config/settings/base.py`**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'apps.core',
    'apps.animals',
    'apps.health',
    'apps.breeding',
    'apps.operations',
    'apps.analytics',
]

AUTH_USER_MODEL = 'core.User'

# CORS (for Flutter app)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Flutter web dev
    "http://127.0.0.1:3000",
]

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',  # For Flutter
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

### Step 2: Create Migrations

```bash
# Create migrations for each app
python manage.py makemigrations core
python manage.py makemigrations animals
python manage.py makemigrations health
python manage.py makemigrations breeding
python manage.py makemigrations operations
python manage.py makemigrations analytics

# Apply migrations
python manage.py migrate
```

### Step 3: Create Superuser & Test Data

```bash
# Create admin account
python manage.py createsuperuser

# Create seed data script
python manage.py seed_data
```

**File: `apps/core/management/commands/seed_data.py`**

```python
from django.core.management.base import BaseCommand
from apps.core.models import User, Ranch, Staff
from apps.animals.models import Animal
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seed database with Kisombwa Ranch data'

    def handle(self, *args, **kwargs):
        # Create users
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@kisombwa.com',
            password='admin123',
            role='admin'
        )
        
        manager = User.objects.create_user(
            username='manager',
            email='manager@kisombwa.com',
            password='manager123',
            role='manager'
        )
        
        # Create ranch
        ranch = Ranch.objects.create(
            name='Kisombwa Ranching Scheme',
            location='Kitenga Sub County, Mubende District, Uganda',
            size_hectares=2400,
            owner=admin
        )
        
        # Create staff
        herdsman = Staff.objects.create(
            ranch=ranch,
            name='John Mugisha',
            role='herdsman',
            phone_number='+256700123456'
        )
        
        # Create 20 animals
        for i in range(1, 21):
            Animal.objects.create(
                tag_number=f"BORAN{i:03d}",
                ranch=ranch,
                species='cattle',
                breed='Boran',
                sex=random.choice(['male', 'female']),
                date_of_birth=date.today() - timedelta(days=random.randint(365, 1825)),
                source=random.choice(['born', 'imported']),
                status='active'
            )
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
```

### Step 4: Configure API for Flutter

```bash
pip install djangorestframework django-cors-headers
```

Update `requirements.txt`:
```
Django==4.2.9
djangorestframework==3.14.0
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
Pillow==10.2.0
python-decouple==3.8
```

---

## 📱 FLUTTER INTEGRATION GUIDE

### SQLite Schema (Mirror Django)

**File: `lib/database/database.dart`**

```dart
// Flutter local database schema
final String createAnimalsTable = '''
  CREATE TABLE animals (
    tag_number TEXT PRIMARY KEY,
    rfid_code TEXT,
    species TEXT NOT NULL,
    breed TEXT,
    sex TEXT NOT NULL,
    date_of_birth TEXT,
    source TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    synced INTEGER DEFAULT 0
  )
''';

final String createBreedingEventsTable = '''
  CREATE TABLE breeding_events (
    id TEXT PRIMARY KEY,
    female_tag TEXT NOT NULL,
    male_tag TEXT,
    service_date TEXT NOT NULL,
    method TEXT NOT NULL,
    pregnancy_confirmed TEXT DEFAULT 'pending',
    synced INTEGER DEFAULT 0,
    FOREIGN KEY (female_tag) REFERENCES animals(tag_number)
  )
''';

// Sync queue table
final String createSyncQueueTable = '''
  CREATE TABLE sync_queue (
    id TEXT PRIMARY KEY,
    operation TEXT NOT NULL,
    table_name TEXT NOT NULL,
    record_data TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    synced INTEGER DEFAULT 0
  )
''';
```

### Offline-First Data Flow

```dart
// Example: Recording breeding event offline
Future<void> recordBreeding(BreedingEvent event) async {
  // Save to local SQLite
  await db.insert('breeding_events', event.toMap());
  
  // Add to sync queue
  await db.insert('sync_queue', {
    'id': uuid.v4(),
    'operation': 'create',
    'table_name': 'breeding_events',
    'record_data': jsonEncode(event.toJson()),
    'timestamp': DateTime.now().toIso8601String(),
    'synced': 0,
  });
  
  // Attempt sync if online
  if (await isOnline()) {
    await syncToServer();
  }
}
```

---

## ✅ MIGRATION CHECKLIST

- [ ] Copy all model files to Django apps
- [ ] Update `settings.py` with AUTH_USER_MODEL
- [ ] Run `makemigrations` for each app
- [ ] Run `migrate`
- [ ] Create superuser
- [ ] Run seed_data command
- [ ] Test admin panel (animals, breeding, health records)
- [ ] Create API endpoints for Flutter
- [ ] Test CRUD operations
- [ ] Document API for team

---

**This database schema solves the manager's problem: It tracks EVERYTHING needed to analyze why breeding is failing, without expensive IoT hardware!** 🚀
