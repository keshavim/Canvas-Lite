# 361-group-project


---

## 🛠️ Setup Instructions

### 🔧 Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv (recommended)

### ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/keshavim/Canvas-Lite.git
cd Canvas-Lite/canvas_lite

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django

# Run migrations
python manage.py migrate

# Run development server
python manage.py runserver


To create an admin user
python manage.py createsuperuser
Then log in at http://127.0.0.1:8000/admin.
