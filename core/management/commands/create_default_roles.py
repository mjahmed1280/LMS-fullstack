from django.core.management.base import BaseCommand
from core.models import Role


class Command(BaseCommand):
    help = 'Create default roles for the LMS system'

    def handle(self, *args, **options):
        roles = [
            {
                'name': 'admin',
                'description': 'System administrator with full access',
                'permissions': ['admin_all']
            },
            {
                'name': 'faculty',
                'description': 'Faculty member who can manage courses',
                'permissions': ['course_manage', 'assignment_manage', 'attendance_manage', 'grade_manage']
            },
            {
                'name': 'student',
                'description': 'Student with access to courses and assignments',
                'permissions': ['course_view', 'assignment_submit', 'attendance_view', 'grade_view']
            },
            {
                'name': 'guest',
                'description': 'Guest user with limited access',
                'permissions': ['course_view']
            }
        ]

        for role_data in roles:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'permissions': role_data['permissions']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created role: {role.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Role already exists: {role.name}')
                )