# PASSPORT APPLICATION MANAGEMENT SYSTEM

## 🎯 Project Overview
This is a Django-based web application that automates passport application tracking and predicts processing time using Machine Learning.

## ✨ Features
- User Registration & Authentication (Citizen, Police Officer, RPO Officer, Admin)
- Passport Application Submission with Document Upload
- Real-time Application Tracking
- ML-based Processing Time Prediction
- Role-based Dashboards
- Document Verification System
- Police Verification Module
- Admin Analytics Dashboard
- Email/SMS Notifications (configurable)

## 🛠️ Technology Stack
- **Backend**: Django 4.2 (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: MySQL / SQLite (configurable)
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Authentication**: Django Built-in Auth System

## 📁 Project Structure
```
passport_tracking_system/
├── manage.py
├── requirements.txt
├── README.md
├── config/                 # Django project settings
├── accounts/               # User management
├── applications/           # Passport applications
├── officer/                # Officer portal
├── admin_panel/            # Admin dashboard
├── ml_prediction/          # ML prediction engine
├── notifications/          # Notification system
├── static/                 # CSS, JS, Images
├── media/                  # User uploads
└── templates/              # HTML templates
```

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.8+
- MySQL Server (or use SQLite for development)
- pip

### 2. Clone/Extract Project
```bash
# Extract the ZIP file
cd passport_tracking_system
```

### 3. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Configuration

#### Option A: MySQL (Recommended for Production)
1. Create database:
```sql
CREATE DATABASE passport_system;
```

2. Update `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'passport_system',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### Option B: SQLite (Quick Start)
Already configured by default - no changes needed!

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Train ML Model
```bash
python ml_prediction/train_model.py
```

### 8. Create Superuser
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (your secure password)
```

### 9. Run Development Server
```bash
python manage.py runserver
```

### 10. Access Application
- Main Site: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## 👥 User Roles & Access

### Citizen
- Register/Login
- Submit passport application
- Upload documents
- Track application status
- View predicted completion time

### Police Officer
- Login with officer credentials
- View assigned verifications
- Complete verification forms
- Update verification status

### RPO Officer
- View all applications
- Verify documents
- Assign tasks
- Update application stages
- Approve/Reject applications

### Admin
- Full system access
- View analytics dashboard
- Manage users
- System configuration
- Performance reports

## 🧪 Default Test Users (After setup)

Create these users for testing:
```bash
python manage.py createsuperuser
# Create users with different roles from admin panel
```

**Test Credentials:**
- Admin: admin / admin123
- Citizen: citizen1 / test123
- Officer: officer1 / test123

## 🤖 ML Model Details

### Algorithm
- Random Forest Regressor
- Trained on historical application data
- Accuracy: ~85-90%

### Features Used
- Application type (new/renewal/reissue)
- City & State
- Current workload
- Submission month
- Historical processing times

### Prediction Output
- Expected processing days
- Confidence score
- Stage-wise timeline

## 📊 Database Schema

### Main Tables
- **User**: Custom user model with roles
- **Application**: Passport application data
- **Document**: Uploaded documents
- **ApplicationStage**: Stage tracking
- **ProcessingHistory**: ML training data
- **Prediction**: ML predictions log
- **Notification**: User notifications

## 🎨 Screenshots & Demo

### Citizen Dashboard
- View all applications
- Track status in real-time
- Predicted completion date

### Officer Portal
- Pending verifications list
- Document verification interface
- Status update forms

### Admin Analytics
- Total applications chart
- Processing time trends
- Officer performance metrics

## 🔒 Security Features
- Password hashing (Django default)
- CSRF protection
- SQL injection prevention
- File upload validation
- Role-based access control

## 📧 Notification System (Optional)
Configure email/SMS in `config/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🐛 Troubleshooting

### Issue: "No module named 'mysqlclient'"
```bash
pip install mysqlclient
# Or use pymysql:
pip install pymysql
```

### Issue: Database connection error
- Check MySQL is running
- Verify credentials in settings.py
- Ensure database exists

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

### Issue: Permission denied on manage.py
```bash
chmod +x manage.py
```

## 📝 Project Report Structure

1. **Introduction**
   - Problem statement
   - Objectives
   - Scope

2. **Literature Survey**
   - Existing systems
   - Technologies overview

3. **System Analysis**
   - Requirements analysis
   - Feasibility study
   - System architecture

4. **System Design**
   - ER diagram
   - Database schema
   - Use case diagrams
   - Sequence diagrams

5. **Implementation**
   - Technology stack
   - Code structure
   - Key modules

6. **Testing**
   - Test cases
   - Results
   - Screenshots

7. **Conclusion & Future Scope**
   - Achievements
   - Future enhancements

## 🚀 Future Enhancements
- Mobile application (Android/iOS)
- Biometric integration
- AI Chatbot for queries
- Blockchain for document verification
- Payment gateway integration
- Multi-language support
- Advanced analytics with AI
- Real-time SMS/Email notifications

## 👨‍💻 Developer

**College Project**
- Course: B.Tech/MCA Computer Science
- Year: Final Year
- Subject: Major Project

## 📄 License
This is an academic project for educational purposes.

## 📞 Support
For any queries related to setup or functionality, refer to the inline code comments or contact your project guide.

