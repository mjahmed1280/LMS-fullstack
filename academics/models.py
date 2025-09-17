from django.db import models
from core.models import Institute, Student, Faculty


class Program(models.Model):
    """Represents an academic program (e.g., B.Tech, M.Tech, MBA)"""
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    duration_years = models.PositiveIntegerField(help_text="Duration in years")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['institute', 'code']

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.institute.name}"


class Branch(models.Model):
    """Represents a branch/specialization within a program"""
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['program', 'code']

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.program.name}"


class AcademicYear(models.Model):
    """Represents an academic year within a program"""
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='academic_years')
    year_number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['program', 'year_number']

    def __str__(self):
        return f"{self.name} - {self.program.name}"


class Semester(models.Model):
    """Represents a semester within an academic year"""
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='semesters')
    semester_number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['academic_year', 'semester_number']

    def __str__(self):
        return f"{self.name} - {self.academic_year.name}"


class Subject(models.Model):
    """Represents a subject/course in the curriculum"""
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subjects')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='dependent_subjects')
    subject_type_choices = [
        ('core', 'Core'),
        ('elective', 'Elective'),
        ('practical', 'Practical'),
        ('project', 'Project'),
    ]
    subject_type = models.CharField(max_length=20, choices=subject_type_choices, default='core')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['branch', 'semester', 'code']

    def __str__(self):
        return f"{self.name} ({self.code})"


class StudentEnrollment(models.Model):
    """Links students to their program/branch/current semester"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='student_enrollments')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='student_enrollments')
    current_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrolled_students')
    enrollment_date = models.DateField()
    is_active = models.BooleanField(default=True)
    graduation_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'program', 'branch']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.branch.name}"
