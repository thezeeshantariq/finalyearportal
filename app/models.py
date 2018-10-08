from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


class User(AbstractUser):
    """
    Model of User
    It extends the existing/built-in user model of
    django and being customized in backends.py
    for different authentications
    """
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)


# **************************************** #
#                                          #
#  G E N E R A L  I N F OR M A T I O N     #
#                                          #
# **************************************** #
class Department(models.Model):
    """
    Representing the Departments for Programs e.g
    Computer Science, Electrical Engineering, Bio etc.
    """
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    """
    Represents Program regarded to department e.g
    BSE, BCS, BTY, BBA etc.
    """
    name = models.CharField(max_length=4, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ": " + self.department.name


class Batch(models.Model):
    """
    Represents the year of university batch e.g
    FA11, SP14, SP15 etc.
    """
    name = models.CharField(max_length=4, unique=True)
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ": " + str(self.year)


# **************************************** #
#                                          #
#              F A C U L T Y               #
#                                          #
# **************************************** #
class Faculty(models.Model):
    """
    Major information like name, email and password is contained
    within the existing USER model of django and this model is
    extension of existing model.

    This model represents a Faculty member in data base which
    has One-To-One relationship with existing User
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_supervisor = models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)
    is_committee_member = models.BooleanField(default=False)
    is_committee_head = models.BooleanField(default=False)
    is_evaluation_committee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="faculty/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def get_current_notification_count(self):
        return self.faculty_receiver.filter(is_seen=False).count()


class FacultyNotifications(models.Model):
    """
    This model contains Notification for any faculty
    member with provided title, msg, and sender.

    It also maintain state of notification if notification
    is seen or not
    """

    title = models.CharField(max_length=30)
    text = models.CharField(max_length=255)
    receiver = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_receiver")
    sender = models.ForeignKey(Faculty, on_delete=models.CASCADE, blank=True, null=True, related_name="faculty_sender")
    expiry = models.DateTimeField(blank=True, null=True)
    is_viewed = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.receiver.get_name() + ": " + self.title


# **************************************** #
#                                          #
#             P R O J E C T                #
#                                          #
# **************************************** #
class Project(models.Model):
    """
    It represents project entity in project in
    database
    """
    supervisor = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=300)
    proposal = models.FileField(upload_to="projects/proposals/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.supervisor.user.first_name + ": " + self.title


class ProjectRequest(models.Model):
    """
    A project request is created when new project is
    created
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    reject_reason = models.CharField(max_length=500, blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    is_forwarded = models.BooleanField(default=False)
    is_need_changes = models.BooleanField(default=False)
    changes_required = models.CharField(max_length=500, blank=True, null=True)
    comments = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# **************************************** #
#                                          #
#             S T U D E N T                #
#                                          #
# **************************************** #
class Student(models.Model):
    """
    Major information like name, email and password is contained
    within the existing USER model of django and this model is
    extension of existing model.

    This model represents a Student in database which
    has One-To-One relationship with existing User
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    number = models.CharField(max_length=3)
    image = models.ImageField(upload_to="students/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def regno(self):
        return "{0}-{1}-{2}".format(self.batch.name, self.program.name, self.number)

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def get_notification_count(self):
        return self.receiver.filter(is_seen=False).count()


class StudentNotifications(models.Model):
    """
        This model contains Notification for any Student
        member with provided title, msg, and sender.

        It also maintain state of notification if notification
        is seen or not
        """
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=255)
    receiver = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="receiver")
    sender = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True, related_name="sender")
    is_viewed = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)
    expiry = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.receiver.get_name() + ": " + self.title


class StudentGroup(models.Model):
    """
    Represents group of student in database, contain
    information of project and students
    """
    name = models.CharField(max_length=30)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ": " + self.project.title


class StudentInGroup(models.Model):
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
