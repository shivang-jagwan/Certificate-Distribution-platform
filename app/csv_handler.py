"""
CSV Handler Module
Handles reading and searching student data from workshop attendance CSV file
"""

import csv
import os
from pathlib import Path
from typing import Optional, List, Dict


class CSVHandler:
    """Handle CSV operations for student data"""
    
    def __init__(self, csv_path: str = "data/Workshop-I Attendance Form (Responses).csv"):
        """
        Initialize CSV handler
        
        Args:
            csv_path: Path to the CSV file containing student data
        """
        project_root = Path(__file__).resolve().parents[1]
        candidate = Path(csv_path)
        if not candidate.is_absolute():
            candidate = project_root / candidate

        self.csv_path = str(candidate)
        
    def get_all_students(self) -> List[Dict[str, str]]:
        """
        Read all students from CSV file
        
        Returns:
            List of dictionaries containing student data
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        students = []
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
        
        return students
    
    def find_student_by_name_and_id(self, name: str, student_id: str) -> Optional[Dict[str, str]]:
        """
        Find a student by their name and student ID
        
        Args:
            name: The student's name to search for
            student_id: The student ID to search for
            
        Returns:
            Dictionary containing student data if found, None otherwise
        """
        students = self.get_all_students()
        
        # Normalize inputs for comparison (case-insensitive, strip whitespace)
        name_normalized = name.strip().lower()
        student_id_normalized = student_id.strip()
        
        for student in students:
            student_name = student.get('Name', '').strip().lower()
            student_sid = student.get('Student_Id', '').strip()
            
            # Match both name and student ID
            if student_name == name_normalized and student_sid == student_id_normalized:
                return student
        
        return None
    
    def generate_certificate_id(self, student_id: str) -> str:
        """
        Generate a certificate ID from student ID
        
        Args:
            student_id: The student's ID
            
        Returns:
            Certificate ID in format CERT-WORKSHOP1-{student_id}
        """
        return f"CERT-WORKSHOP1-{student_id}"
    
    def validate_csv_structure(self) -> bool:
        """
        Validate that CSV has required columns
        
        Returns:
            True if CSV structure is valid, False otherwise
        """
        required_columns = {'Name', 'Email_id', 'Student_Id', 'Course', 'Code'}
        
        try:
            students = self.get_all_students()
            if not students:
                return False
            
            # Check if all required columns exist
            first_row_keys = set(students[0].keys())
            return required_columns.issubset(first_row_keys)
            
        except Exception:
            return False

