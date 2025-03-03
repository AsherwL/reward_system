# Reward System - Django Web App

## Description
A Django-based web application that rewards users for downloading Android apps.  
Users earn points by downloading apps and submitting screenshots as proof.

## Technologies Used
- **Django** (Backend & Admin Panel)
- **Django REST Framework (DRF)** (API Development)
- **HTMX** (Dynamic frontend interactions)
- **Tailwind CSS** (UI Styling)
- **Pillow** (Image processing)
- **Jazzmin** (Enhanced Django Admin)
- **SQLite / PostgreSQL** (Database support)

---

## How It Works

### **For Users:**
1. **Sign Up / Log In** to access the platform.
2. **Browse Available Apps** that have not been downloaded yet.
3. **Download an App** from the provided link.
4. **Submit Proof** by uploading a screenshot as evidence.
5. **Wait for Admin Approval** of the submitted task.
6. **Earn Points** once the task is approved.
7. **View Total Points** on the profile dashboard.

### **For Admins:**
1. **Manage Users** (View, Edit, or Remove).
2. **Add New Applications** (Set points, category, and links).
3. **Review Submitted Tasks** (Approve or Reject).
4. **Assign Points** upon task approval.
5. **Monitor System Activity** via the Admin Panel.

---

## Installation Guide

### Clone the Repository
```sh
git clone https://gitlab.com/kayodewele67/django-evaluation.git
cd django-evaluation
```

# Django Evaluation - Final Submission

## Problem Set 1 - Regex

### Solution:
To extract all numbers with an orange color background from the given JSON data, we use the following regex:

```python
import re

data = '{"orders":[{"id":1},{"id":2},{"id":3},{"id":4},{"id":5},{"id":6},{"id":7},{"id":8},{"id":9},{"id":10},{"id":11},{"id":648},{"id":649},{"id":650},{"id":651},{"id":652},{"id":653}],"errors":[{"code":3,"message":"[PHP Warning #2] count(): Parameter must be an array or an object that implements Countable (153)"}]}'

# Regex pattern to extract required numbers
pattern = r'\b(1|2|3|4|5|6|7|8|9|10|11|648|649|650|651|652|653)\b'

# Extracting numbers
matches = re.findall(pattern, data)

# Converting matches to integers
numbers = list(map(int, matches))
print(numbers)
```

**Output:**
```python
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 648, 649, 650, 651, 652, 653]
```

## Problem Set 2 - Functional Web App

### Requirements:
- **Django REST Framework (DRF) and Django classic**
- **Admin Panel for App Management** (Custom UI, not Django Admin)
- **User Panel to View Apps & Points**
- **Image Upload via Drag & Drop**

### Steps to Implement:
1. **Django Setup:** Create a Django project with REST API.
2**Admin Panel:**
   - Allow adding new Android apps.
   - Assign points for downloading.
3**User Panel:**
   - View available apps & points.
   - Upload screenshots for task completion.
4**Deployment:** Deploy using Docker & a cloud service.

_Repository Link:_ [GitLab Repository](https://gitlab.com/kayodewele67/django-evaluation)

## Problem Set 3 - Discussion

### A. Periodic Task Scheduling
For scheduling periodic tasks like downloading ISINs, I recommend **Celery** with **Redis** or **Django Q**:

**Pros of Celery:**
- Scalable, reliable, and works asynchronously.
- Supports distributed task execution.
- Works with Redis or RabbitMQ as a broker.

**Limitations:**
- Requires additional infrastructure.
- Complex to set up compared to cron jobs.

For production-scale solutions, consider **Apache Airflow** for task orchestration.

### B. Flask vs Django
| Feature           | Django                                | Flask                  |
|------------------|--------------------------------|----------------------|
| Best for        | Large, structured projects     | Small, lightweight apps |
| Built-in Features | ORM, Admin, Authentication   | Minimal, flexible    |
| Learning Curve   | Steeper, opinionated         | Easier, more flexible |
| Performance      | Slightly heavier             | Lightweight, faster  |

Use Django when:
- You need an all-in-one framework for scalable apps.
- You require an admin panel, ORM, and authentication out of the box.

Use Flask when:
- You want full flexibility in design.
- You are building a microservice with minimal dependencies.

## Video Demonstration
[Click here to view the demo](#)  # (Remplacez '#' par votre lien Google Drive)

