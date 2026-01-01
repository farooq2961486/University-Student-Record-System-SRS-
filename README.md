===============================
University Student Management System
===============================

Project Name: University LMS (Student Registration System)
Developer: Farooq Murad
Date: January 2026
Language: Python 3
GUI Library: Tkinter (Pure - No External GUI Libraries)
Database: SQLite (File: university_lms.db)

--- Description ---
Yeh ek complete desktop application hai jo university ya college mein students ka record manage karne ke liye banaya gaya hai.
Sab features pure Tkinter se banaye gaye hain, koi extra library (jaise PySimpleGUI) use nahi ki gayi.

--- Features ---
1. Secure Admin Login
   - Username: Farooq
   - Password: farooq123
   - Advanced Math reCAPTCHA (robot check)
   - Skip Login (Guest Mode) button bhi hai demo ke liye

2. Stylish & Modern Interface
   - Beautiful dark login page
   - Purple header wala dashboard
   - Welcome message with admin name

3. Student Management
   - Naya student add karo
   - Existing student edit/update karo
   - Student delete karo
   - Live search bar (naam, ID, email se search)
   - Double-click kar ke form mein details load karo

4. Data Validation
   - Email format check
   - Phone (11 digits), CNIC (13 digits) check
   - Required fields warning

5. Print Slip Feature
   - Koi student select karo
   - "Print Selected Student Slip" button dabao
   - Official looking slip khulegi
   - Slip par Ctrl+P press kar ke print kar sakte ho

6. Database
   - SQLite database (university_lms.db)
   - Sab data permanently save hota hai
   - App band hone par bhi data safe rahta hai

--- How to Run ---
1. Python 3 installed hona chahiye (3.8 ya above)
2. Code file (university_lms.py) aur database file (university_lms.db) same folder mein rakho
3. Command prompt ya terminal kholo
4. Command run karo:
   python university_lms.py

   (agar python3 use karte ho toh: python3 university_lms.py)

5. Login page aayega
   - Admin login: Farooq / farooq123
   - Ya "Skip Login" button dabao demo ke liye

--- Database Note ---
- Pehli baar run karne par database automatically ban jayegi
- Agar purana data hai toh safe rahega (delete nahi hoga)
- Table name: Students
- Columns: StudentID, FullName, UniversityID, Email, Gender, Age, Phone, CNIC, Address, EnrollmentDate

--- Future Improvements (Optional) ---
- Student photo upload
- Export data to Excel/PDF
- Multiple admin accounts
- Backup database option
- Dark/Light theme toggle

--- Contact ---
Agar koi issue aaye ya new feature chahiye toh contact karo!

Project by: Farooq Murad
For: Final Year Project / Personal Use
+923078113098

Enjoy the application! 🎓✨
