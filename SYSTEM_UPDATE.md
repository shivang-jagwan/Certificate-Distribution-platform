# System Update Summary - Workshop Certificate System

## Changes Made

### 1. CSV Handler Updated
**File**: `app/csv_handler.py`
- Changed default CSV path to `data/Workshop-I Attendance Form (Responses).csv`
- Replaced `find_student_by_certificate_id()` with `find_student_by_name_and_id()`
- Added case-insensitive name matching
- Added `generate_certificate_id()` method to create IDs in format: `CERT-WORKSHOP1-{student_id}`
- Updated validation to check for workshop CSV columns: Name, Email_id, Student_Id, Course, Code

### 2. API Endpoints Updated
**File**: `app/main.py`

#### `/verify` endpoint
- Changed from `/verify/{certificate_id}` to `/verify?name={name}&student_id={student_id}`
- Now accepts query parameters for name and student ID
- Returns student info including course and generated certificate ID

#### `/certificate` endpoint  
- Changed from `/certificate/{certificate_id}` to `/certificate?name={name}&student_id={student_id}`
- Searches by name and student ID
- Generates certificate ID automatically
- Downloads PDF with generated certificate ID

#### `/generate-all` endpoint
- Updated to work with workshop CSV structure
- Generates certificate IDs automatically for all students
- Uses Student_Id and Name fields from workshop data

### 3. Frontend Updated
**File**: `templates/index.html`
- Changed from single "Certificate ID" input to two inputs:
  - Student Name
  - Student ID
- Updated sample data to show workshop attendees
- Modified JavaScript to send name and student_id as query parameters
- Better error messages for student not found

## How It Works Now

1. **User Input**: Student enters their name and student ID
2. **Verification**: System searches workshop CSV for matching name + ID
3. **Certificate ID Generation**: Creates ID like `CERT-WORKSHOP1-25101280272`
4. **Certificate Generation**: Uses existing template to create PDF
5. **Download**: Returns PDF with generated certificate ID as filename

## Sample Data

From the workshop CSV (175 students):
- **Name**: Aditya singh, **Student_Id**: 25101280272
- **Name**: Sarthak Raiwani, **Student_Id**: 24041452
- **Name**: Saksham Joshi, **Student_Id**: 24011805

## Testing

Access the system at: **http://localhost:8001**

Try entering:
- Name: `Aditya singh`
- Student ID: `25101280272`

The system will:
1. Verify the student exists
2. Generate certificate ID: `CERT-WORKSHOP1-25101280272`
3. Create PDF certificate
4. Download as `CERT-WORKSHOP1-25101280272.pdf`

## Certificate Template

Using the existing template at: `templates/certificate_template.jpg`
- Professional design with gold borders
- Student name centered dynamically
- Certificate ID displayed below name
