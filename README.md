# DEBIS-API
## Description
Debis API is a part of Debis project. DEBIS project is a student management system for universities. This repository contains backend services and operations for the DEBIS project. I am adding new properties and developing this project every day. Stay tuned :)
## About Project
I am student at Dokuz Eylul University Computer Science Department. My fundamental mission fix my university's student system's errors and bugs and improving new features. Different by other student management systems, I am goaling statistical features adding about teachers and students performance analysis to this system for combining data analysis, data visualization and web development. I will continue to develop the project for this purpose.
## Database
I use PostgreSQL for database operations. I am adding a schema diagram of database the designed by me below this title.
![Database Diagram](images/Database.png)
## Endpoints
| Endpoint | Method | Description |
| -------- | -------- | -------- |
| /auth/login | POST | Basic login function based JWT  |
| /auth/save_student | POST | Create new student account  |
| /auth/save_teacher | POST | Create new teacher account  |
| /auth/me | GET  | Get user information |
| /lesson/ | GET | Get all lessons data |
| /lesson/{lesson_id} | GET | Get lessons data by id |
| /lesson/student_all_lesson/{student_id} | GET | Get specific student all lessons data |
| /lesson/student_semester_lesson/{student_id} | GET | Get specific student lessons data by semester |
| /lesson/create | POST | Create new lesson |
| /lesson/assign-teacher | PUT | Assign lesson to teacher |
| /lesson/assign-student | POST | Assign lesson to students |
| /lesson/add_note | PUT | Add note data to students |
| /lesson/options/{student_id}  | GET | Get semester and year data for student user |
| /announcement/ | GET | Get all announcements |
| /announcement/create | POST | Create new announcement |
| /announcement/get_lesson_announcement | GET  | Get all announcements for specific lesson |
## Installation

Install this repository to your local environment
```bash
git clone https://github.com/er4y-c/DEBIS-API.git
```

Install required libraries
```bash
pip install -r requirements.txt
```

Create your local database for project
```bash
python init_db
```

You can use Alembic for database migration.
Start the project on your local environment

```bash
uvicorn main:app --reload
```

## Contact
<p>I am open to all suggestions, so you can contact me at the following addresses.</p>
<div style="display:flex;">
  <img src="https://i.stack.imgur.com/gVE0j.png" alt="LinkedIn Logo" width="25px" height="25px">
  <a href="https://www.linkedin.com/in/eray-aynaci/">https://www.linkedin.com/in/eray-aynaci/</a>
</div>
<div style="display:flex;">
  <img src="https://i.imgur.com/LfXxQHq.jpeg" alt="Gmail Logo" width="25px" height="25px">
  <a href="mailto:erayaynaci1@gmail.com">erayaynaci1@gmail.com</a>
</div>
