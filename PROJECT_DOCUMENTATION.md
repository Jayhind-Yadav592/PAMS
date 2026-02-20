# PASSPORT TRACKING SYSTEM - PROJECT DOCUMENTATION

## 📋 TABLE OF CONTENTS
1. Introduction
2. System Requirements
3. Installation Guide
4. Features & Functionality
5. Database Schema
6. User Roles
7. Screenshots Guide
8. Testing Instructions
9. Troubleshooting
10. Future Enhancements

---

## 1. INTRODUCTION

### Project Title
**Automated Passport Tracking and Processing Time Prediction System for Government Services**

### Problem Statement
Current passport application systems lack transparency and citizens have no way to track their application status in real-time. Processing times are uncertain and there's no reliable way to predict when a passport will be delivered.

### Solution
A comprehensive web-based system that:
- Automates passport application tracking
- Predicts processing time using Machine Learning
- Provides role-based access for Citizens, Officers, and Admins
- Sends real-time notifications on status changes
- Generates analytics for government officials

### Technology Stack
- **Backend**: Django 4.2 (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (Development) / MySQL (Production)
- **Machine Learning**: Scikit-learn, Random Forest Algorithm
- **Data Processing**: Pandas, NumPy

---

## 2. SYSTEM REQUIREMENTS

### Hardware Requirements
- **Processor**: Intel Core i3 or equivalent (minimum)
- **RAM**: 4GB (minimum), 8GB (recommended)
- **Storage**: 500MB free space
- **Internet Connection**: Required for package installation

### Software Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **MySQL**: Version 8.0+ (optional, for production)
- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest version)

---

## 3. INSTALLATION GUIDE

### Step 1: Extract Project
```bash
# Extract the ZIP file to your desired location
# Example: C:\Projects\passport_tracking_system
```

### Step 2: Create Virtual Environment
```bash
# Navigate to project directory
cd passport_tracking_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install django
pip install Pillow
pip install pandas
pip install scikit-learn
pip install numpy

# OR install from requirements.txt
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Train ML Model
```bash
# Train the machine learning model
python ml_prediction/train_model.py
```

### Step 6: Create Admin User
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (choose a secure password)
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

### Step 8: Access Application
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 4. FEATURES & FUNCTIONALITY

### For Citizens
1. **User Registration**
   - Create account with email/phone verification
   - Secure password storage

2. **Application Submission**
   - Fill passport application form
   - Upload required documents (Photo, ID, Address proof)
   - Receive unique application number

3. **Real-time Tracking**
   - View current status of application
   - See predicted completion time
   - Track each stage of processing

4. **Dashboard**
   - View all applications
   - Check statistics (pending, completed)
   - Quick access to common actions

### For Officers (Police/RPO)
1. **Verification Portal**
   - View assigned applications
   - Verify documents
   - Approve/reject applications
   - Add remarks

2. **Task Management**
   - See pending verifications
   - Update status
   - Track workload

### For Administrators
1. **Analytics Dashboard**
   - Total applications statistics
   - Processing time trends
   - Officer performance metrics
   - Monthly/yearly reports

2. **User Management**
   - Create officer accounts
   - Assign roles
   - Monitor activity

3. **System Configuration**
   - Manage application settings
   - Configure notifications
   - View system logs

---

## 5. DATABASE SCHEMA

### Tables Overview

#### User Table
- id (PK)
- username
- email
- password
- role (citizen/police/rpo/admin)
- phone
- address, city, state, pincode
- date_of_birth

#### Application Table
- id (PK)
- user_id (FK)
- application_number (Unique)
- application_type (new/renewal/reissue)
- full_name, dob, gender
- email, phone
- address, city, state, pincode
- current_status
- submission_date
- predicted_completion_days
- expected_completion_date
- actual_completion_date

#### ApplicationStage Table
- id (PK)
- application_id (FK)
- stage_name
- status (pending/in_progress/completed/rejected)
- assigned_officer_id (FK)
- start_time, end_time
- remarks

#### Document Table
- id (PK)
- application_id (FK)
- document_type
- file_path
- uploaded_at
- verified (Boolean)

#### ProcessingHistory Table
- id (PK)
- application_id (FK)
- actual_processing_days
- application_type, city, state
- submission_month
- workload_at_submission
- completion_date

#### Prediction Table
- id (PK)
- application_id (FK)
- predicted_days
- confidence_score
- prediction_date
- model_version

---

## 6. USER ROLES

### Creating Test Users

After running migrations, create test users from admin panel:

1. **Login to Admin**: http://127.0.0.1:8000/admin/
2. **Go to Users section**
3. **Add User** and set the role field:

**Test Citizen**
- Username: citizen1
- Password: test123
- Role: citizen
- Email: citizen1@test.com

**Test Police Officer**
- Username: police1
- Password: test123
- Role: police
- Email: police1@test.com

**Test RPO Officer**
- Username: rpo1
- Password: test123
- Role: rpo
- Email: rpo1@test.com

---

## 7. SCREENSHOTS GUIDE

For project documentation, capture these screenshots:

### Essential Screenshots

1. **Login Page**
   - URL: /accounts/login/
   - Shows: Login form

2. **Registration Page**
   - URL: /accounts/register/
   - Shows: Registration form

3. **Citizen Dashboard**
   - URL: /application/dashboard/
   - Shows: Application statistics and list

4. **Submit Application Form**
   - URL: /application/submit/
   - Shows: Complete application form

5. **Application Tracking**
   - URL: /application/track/{app_number}/
   - Shows: Timeline with stages and predicted time

6. **Officer Dashboard**
   - URL: /officer/dashboard/
   - Shows: Pending verifications

7. **Verification Form**
   - URL: /officer/verify/{stage_id}/
   - Shows: Verification interface

8. **Admin Dashboard**
   - URL: /admin-panel/dashboard/
   - Shows: Analytics and statistics

9. **Admin Panel (Django)**
   - URL: /admin/
   - Shows: Built-in Django admin interface

---

## 8. TESTING INSTRUCTIONS

### Unit Testing
```python
# Run Django tests
python manage.py test

# Test specific app
python manage.py test applications
```

### Manual Testing Checklist

**User Registration & Login**
- [ ] New user can register
- [ ] Login with correct credentials works
- [ ] Login with incorrect credentials fails
- [ ] Logout functionality works

**Application Submission**
- [ ] Form validation works
- [ ] All required fields are mandatory
- [ ] Application number is generated
- [ ] ML prediction works
- [ ] Application appears in dashboard

**Application Tracking**
- [ ] Can track application by number
- [ ] Stages display correctly
- [ ] Status updates reflect properly

**Officer Portal**
- [ ] Officers can see assigned tasks
- [ ] Verification form works
- [ ] Status updates cascade correctly

**Admin Dashboard**
- [ ] Statistics display correctly
- [ ] Reports are accurate
- [ ] User management works

---

## 9. TROUBLESHOOTING

### Common Issues

**Issue 1: "No module named 'django'"**
```bash
Solution: Install Django
pip install django
```

**Issue 2: Database errors during migration**
```bash
Solution: Delete db.sqlite3 and migrate again
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

**Issue 3: ML model not found**
```bash
Solution: Train the model
python ml_prediction/train_model.py
```

**Issue 4: Static files not loading**
```bash
Solution: Collect static files
python manage.py collectstatic
```

**Issue 5: Permission denied errors**
```bash
Solution: Run as administrator/sudo
# Windows: Run CMD as Administrator
# Linux/Mac: Use sudo
```

---

## 10. FUTURE ENHANCEMENTS

### Phase 2 Features
1. **Mobile Application**
   - Android and iOS apps
   - Push notifications
   - QR code scanning

2. **Advanced ML Features**
   - Bottleneck prediction
   - Resource optimization
   - Demand forecasting

3. **Biometric Integration**
   - Fingerprint verification
   - Face recognition for document verification

4. **Payment Gateway**
   - Online fee payment
   - Multiple payment options
   - Receipt generation

5. **Multi-language Support**
   - Hindi, regional languages
   - RTL support for specific languages

6. **Advanced Analytics**
   - Predictive analytics dashboard
   - AI-powered insights
   - Performance benchmarking

7. **Blockchain Integration**
   - Tamper-proof records
   - Document verification on blockchain
   - Smart contracts for workflow

8. **Chatbot Integration**
   - 24/7 query resolution
   - AI-powered assistance
   - Multi-lingual support

---

## 📞 SUPPORT

For technical issues:
1. Check SETUP_GUIDE.txt
2. Refer to this documentation
3. Check inline code comments
4. Review Django documentation: https://docs.djangoproject.com/

---

## 📜 LICENSE

This is an academic project created for educational purposes.

---

## ✅ PROJECT COMPLETION CHECKLIST

- [x] Django project setup
- [x] User authentication system
- [x] Passport application models
- [x] ML prediction engine
- [x] Citizen dashboard
- [x] Officer portal
- [x] Admin analytics
- [x] Responsive UI with Bootstrap
- [x] Complete documentation
- [x] Setup guides
- [x] Testing instructions

---

**Project Status**: ✅ COMPLETE & READY FOR SUBMISSION

**Last Updated**: 2024

**Good Luck with your Project! 🎓**
