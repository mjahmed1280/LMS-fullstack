from django.db import models
from core.models import Faculty, Student
from academics.models import Subject, Semester


class CourseOffering(models.Model):
    """Represents an instance of a subject being taught in a specific semester"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='offerings')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='course_offerings')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course_offerings')
    section = models.CharField(max_length=10, default='A')
    max_enrollment = models.PositiveIntegerField(default=60)
    room_number = models.CharField(max_length=20, blank=True)
    schedule = models.JSONField(default=dict, help_text="Class schedule as JSON")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['subject', 'semester', 'section']

    def __str__(self):
        return f"{self.subject.name} - {self.section} ({self.semester.name})"

    @property
    def current_enrollment(self):
        return self.enrollments.filter(status='enrolled').count()


class Enrollment(models.Model):
    """Student enrollment in a course offering"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_enrollments')
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='enrolled')
    final_grade = models.CharField(max_length=5, blank=True)
    final_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'course_offering']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course_offering.subject.name}"


class Assignment(models.Model):
    """Assignments for a course offering"""
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_marks = models.PositiveIntegerField()
    assignment_type_choices = [
        ('homework', 'Homework'),
        ('project', 'Project'),
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
        ('lab', 'Lab Work'),
    ]
    assignment_type = models.CharField(max_length=20, choices=assignment_type_choices, default='homework')
    is_published = models.BooleanField(default=False)
    allow_late_submission = models.BooleanField(default=False)
    late_penalty_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    submission_format = models.JSONField(default=dict, help_text="Allowed file types and constraints")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.course_offering.subject.name}"


class AssignmentSubmission(models.Model):
    """Student submissions for assignments"""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignment_submissions')
    submission_text = models.TextField(blank=True)
    submission_file = models.FileField(upload_to='assignments/', blank=True, null=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_late = models.BooleanField(default=False)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True)
    graded_date = models.DateTimeField(blank=True, null=True)
    graded_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='graded_submissions')
    status_choices = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('returned', 'Returned'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='submitted')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assignment.title}"


class AttendanceSession(models.Model):
    """Attendance sessions for course offerings"""
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='attendance_sessions')
    session_date = models.DateField()
    session_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    topic_covered = models.CharField(max_length=200)
    session_type_choices = [
        ('lecture', 'Lecture'),
        ('lab', 'Lab'),
        ('tutorial', 'Tutorial'),
        ('seminar', 'Seminar'),
    ]
    session_type = models.CharField(max_length=20, choices=session_type_choices, default='lecture')
    is_mandatory = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course_offering', 'session_date', 'session_time']

    def __str__(self):
        return f"{self.course_offering.subject.name} - {self.session_date}"


class AttendanceRecord(models.Model):
    """Individual attendance records for students"""
    attendance_session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    status_choices = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='absent')
    marked_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='marked_attendance')
    marked_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['attendance_session', 'student']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.attendance_session.session_date} ({self.status})"
