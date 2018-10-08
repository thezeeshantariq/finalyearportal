from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *


# Create your views here.

# Home page
def index(request):
    return render(request, 'app/index.html')


# ******************************************* #
#                                             #
#              L O G I N                      #
#                                             #
# ******************************************* #

# Faculty Login
def login_as_faculty(request):
    """
    Login the faculty with provided email
    or password
    :param request: a must have object, which make this
                    function a "view" and contains every
                    information sent by user
    :return: Render a response based on provided parameters
    """
    if request.method == "POST":
        faculty_email = request.POST['faculty_email']
        faculty_password = request.POST['faculty_password']

        user = authenticate(
            request,
            username=faculty_email,
            password=faculty_password)

        if user is not None:
            login(request, user)
            return redirect('faculty-portal')
        else:
            messages.error(request, "Invalid Email or Password")

    return render(request, 'app/faculty/registration/login.html')


# Student Login
def login_as_student(request):
    """
    Login student with provided Registration number and
    password
    :param request: a must have object, which make this
                    function a "view" and contains every
                    information sent by user
    :return: Render a response based on provided parameters
    """
    context = {
        'program': Program.objects.all(),
        'batch': Batch.objects.all(),
    }

    if request.method == "POST":
        print("POST---------: ", request.POST)
        student_batch = request.POST['student_batch']
        student_program = request.POST['student_program']
        student_number = request.POST['student_number']
        student_password = request.POST['student_password']

        regno = "{}-{}-{}".format(student_batch, student_program, student_number)

        user = authenticate(request, username=regno, password=student_password)
        if user is not None:
            login(request, user)
            return redirect('student-portal')
        else:
            messages.error(request, "Invalid Registration Number or Password")

    return render(request, 'app/students/registration/login.html', context)


# ******************************************* #
#                                             #
#              Registration                   #
#                                             #
# ******************************************* #

# Faculty Registration
def signup_as_faculty(request):
    """
    Register faculty based on provided information
    also log the faculty in if registration is
    successful
    :param request: a must have object, which make this
                    function a "view" and contains every
                    information sent by user
    :return: Render a response based on provided parameters or
             redirect to portal if successfully registered
    """
    if request.method == "POST":
        print(request.POST)
        faculty_name = request.POST['faculty_name']
        faculty_email = request.POST['faculty_email']
        faculty_password = request.POST['faculty_password']
        faculty_password_confirm = request.POST['faculty_password_confirm']

        if faculty_password == faculty_password_confirm:
            user = authenticate(request, username=faculty_email, password=faculty_password)

            if user is not None:
                user.first_name = faculty_name
                user.is_faculty = True
                user.save()

                faculty = Faculty()
                faculty.user = user
                if request.FILES["faculty_image"]:
                    faculty.image = request.FILES["faculty_image"]
                faculty.save()

                login(request, user)
                return redirect('faculty-portal', pk=user.faculty.id)
            else:
                # error about registration
                pass

    return render(request, 'app/faculty/registration/signup.html')


# Student Signup
def signup_as_student(request):
    """
        Register student based on provided information
        also log the faculty in if registration is
        successful
        :param request: a must have object, which make this
                        function a "view" and contains every
                        information sent by user
        :return: Render a response based on provided parameters or
                 redirect to portal if successfully registered
        """
    context = {
        'program': Program.objects.all(),
        'batch': Batch.objects.all(),
    }

    if request.method == "POST":
        print(request.POST)
        student_name = request.POST['student_name']
        student_batch = request.POST['student_batch']
        student_program = request.POST['student_program']
        student_number = request.POST['student_number']
        student_email = request.POST['student_email']
        student_password = request.POST['student_password']
        student_password_confirm = request.POST['student_password_confirm']

        regno = "{}-{}-{}".format(student_batch, student_program, student_number)

        if student_password == student_password_confirm:
            user = authenticate(request, username=regno, password=student_password)
            if user is not None:
                user.first_name = student_name
                user.email = student_email
                user.is_student = True
                user.save()

                student = Student()
                student.user = user
                student.batch = Batch.objects.get(pk=int(student_batch))
                student.program = Program.objects.get(pk=int(student_program))
                student.number = student_number
                if request.FILES["student_image"]:
                    student.image = request.FILES['student_image']
                student.save()

                login(request, user)
                return redirect('student-portal')
            else:
                # error about registration
                pass

    return render(request, 'app/students/registration/signup.html', context)


# Logout any user
def user_logout(request):
    """
    Logout any user Faculty or Student
    :param request:
    :return: Redirect to Home Page
    """
    logout(request)
    return redirect('home')


# ******************************************* #
#                                             #
#              F A C U L T Y                  #
#                                             #
# ******************************************* #
@login_required
def faculty_portal(request):
    """
    Redirect to Faculty portal after successful login
    or registration
    :param request:
    :return:
    """
    return render(request, 'app/faculty/profile.html')


@login_required
def faculty_notifications(request):
    """
    Read notifications for current logged in user
    :param request:
    :return:
    """
    context = {}
    if request.user.is_authenticated:
        try:
            faculty = request.user.faculty
            notifications = faculty.faculty_receiver.all().order_by('is_seen', '-created_at')
            context['notifications'] = notifications
        except FacultyNotifications.DoesNotExist:
            context['notifications'] = None

    return render(request, 'app/faculty/notifications.html', context)


@login_required
def mark_faculty_notification_read(request, pk):
    """
    Mark notification as Read/Seen when "Mark Read" is
    clicked
    :param request:
    :param pk: ID of Notification/Message
    :return:
    """
    notification = FacultyNotifications.objects.get(pk=pk)
    notification.is_seen = True
    notification.save()
    return redirect('faculty-notifications')


@login_required
def make_supervisor(request, pk):
    """
    Create Faculty Member a Supervisor when clicked
    "Make" button
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_supervisor = True
        faculty.save()

        title = "You have been given Supervisor's privileges"
        msg = "Now, you can create groups for student, submit project or proposal requests."
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def remove_supervisor(request, pk):
    """
    Remove a faculty member from Supervisor privilleges
    when clicked "Remove" button
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_supervisor = False
        faculty.save()

        title = "Your Supervisor's privileges has been removed"
        msg = "You can no longer create student groups and manage projects"
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def make_coordinator(request, pk):
    """
    Make faculty member a Coordinator
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_coordinator = True
        faculty.save()

        title = "You have been given Coordinator's privileges"
        msg = "Now, you can manage faculty members and project requests."
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def remove_coordinator(request, pk):
    """
    Remove faculty member from Coordinator privilleges
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_coordinator = False
        faculty.save()

        title = "You Coordinator's privileges has been removed"
        msg = "You can no longer manage faculty or project requests"
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def make_committee_head(request, pk):
    """
    Make faculty member a Comittee Head
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_committee_head = True
        faculty.save()

        title = "You are Committee head now"
        msg = "Now, you can review Projects, member's comments and give feedback to supervisors."
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def remove_committee_head(request, pk):
    """
    Remove faculty member from Committee Head privileges
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_committee_head = False
        faculty.save()

        title = "Your Committee head privileges has been removed."
        msg = "You can't review comments or give feed back to supervisors"
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def make_committee_member(request, pk):
    """
    Make faculty member a Committee Member
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_committee_member = True
        faculty.save()

        title = "You have been given Committee Member's privileges"
        msg = "Now, you can give feedback to students and projects."
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def remove_committee_member(request, pk):
    """
    Remove faculty from Committee Member
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_committee_member = False
        faculty.save()

        title = "Your Committee Member's privileges has been removed"
        msg = "You can no longer give feedback to students and projects."
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def make_evaluation_committee(request, pk):
    """
    Make faculty member an Evaluation Committee
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_evaluation_committee = True
        faculty.save()

        title = "You have been given Evaluation Committee's privileges"
        msg = "Now, you can accept or reject projects."
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def remove_evaluation_committee(request, pk):
    """
    Remove faculty member from evaluation committee privileges
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_evaluation_committee = False
        faculty.save()

        title = "Your Evaluation Committee's privileges has been removed"
        msg = "You can no longer accept or reject projects."
        notify_faculty(title, msg, request.user.faculty, faculty)

    return redirect('coordinator-supervisors')


@login_required
def activate_faculty(request, pk):
    """
    Activate/Unblock faculty member
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_active = True
        faculty.save()

    return redirect('coordinator-supervisors')


@login_required
def deactivate_faculty(request, pk):
    """
    Deactivate/Block faculty member
    :param request:
    :param pk:
    :return:
    """
    if request.user.is_authenticated:
        faculty = Faculty.objects.get(pk=pk)
        faculty.is_active = False
        faculty.save()

    return redirect('coordinator-supervisors')


@login_required
def coordinator_supervisors(request):
    """
    Display all faculty members under coordinator privileges
    :param request:
    :return:
    """
    context = {
        'faculty': Faculty.objects.all()
    }

    return render(request, 'app/faculty/coordinator/supervisors.html', context)


@login_required
def coordinator_projects(request):
    """
    Display all projects under coordinator privileges
    :param request:
    :return:
    """
    context = {
        'projects': Project.objects.all()
    }

    return render(request, 'app/faculty/coordinator/projects.html', context)


@login_required
def coordinator_forward_project(request, pk):
    """
    Forward project requested by supervisor to
    evaluation committee under
    Coordinator privileges
    :param request:
    :param pk:
    :return:
    """
    project_request = ProjectRequest.objects.filter(pk=pk).get()
    project_request.is_forwarded = True
    project_request.save()

    title = "Your project {} is under evaluation".format(project_request.project.title)
    msg = "Your project is forwarded to evaluation committee. You will be notified for further procedure or result"
    notify_faculty(title, msg, request.user.faculty, project_request.project.supervisor)

    title = "{}'s project {} need evaluation".format(project_request.project.supervisor, project_request.project.title)
    msg = "{} has submitted proposal for '{}'. Kindly evaluate it as per required and act accordingly.".format(
        project_request.project.supervisor, project_request.project.title)
    for ec in Faculty.objects.filter(is_evaluation_committee=True).all():
        notify_faculty(title, msg, request.user.faculty, ec)

    return redirect('coordinator-projects')


@login_required
def coordinator_reject_project(request, pk):
    """
    Reject project requested by supervisor under
    Coordinator privileges
    :param request:
    :param pk:
    :return:
    """
    project_request = ProjectRequest.objects.get(pk=pk)
    if request.method == "POST":
        reason = request.POST["reason"]

        project_request.is_active = False
        project_request.is_accepted = False
        project_request.reject_reason = reason
        project_request.save()

        title = "Your project {} was rejected by Coordinator".format(project_request.project.title)
        msg = "The reason for project rejection is: {}".format(reason)
        notify_faculty(title, msg, request.user.faculty, project_request.project.supervisor)

        return redirect("coordinator-projects")

    context = {"project": project_request.project}
    return render(request, 'app/faculty/coordinator/reject_project.html', context)


@login_required
def supervisor_projects(request):
    """
    Display all projects under supervision privileges
    :param request:
    :return:
    """
    try:
        projects = Project.objects.filter(supervisor=request.user.faculty).all()
        context = {'projects': projects}
    except Project.DoesNotExist:
        context = {'projects': None}

    return render(request, 'app/faculty/supervisor/projects.html', context)


@login_required
def supervisor_new_project_request(request):
    """
    Request new project under supervision privileges
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        if request.user.faculty.is_supervisor:
            if request.method == "POST" and request.FILES['project_proposal']:
                project = Project()
                project.title = request.POST["project_title"]
                project.description = request.POST['project_description']
                project.proposal = request.FILES['project_proposal']
                project.supervisor = request.user.faculty
                project.save()

                project_request = ProjectRequest()
                project_request.project = project
                project_request.is_accepted = False
                project_request.is_forwarded = False
                project_request.is_need_changes = False
                project_request.is_active = True
                project_request.save()

                title = "New Project Request from {}".format(request.user.first_name)
                msg = "{} has request approval of project '{}'.".format(request.user.first_name, project.title)

                for coordinator in Faculty.objects.filter(is_coordinator=True).all():
                    notify_faculty(title, msg, request.user.faculty, coordinator)

                messages.success(request, "Your request for '{}' has been created".format(project.title))

                return redirect("faculty-supervisor-projects")

    return render(request, 'app/faculty/supervisor/new_project.html')


@login_required
def supervisor_groups(request):
    """
    Display all groups under supervision privileges
    :param request:
    :return:
    """
    group = None
    context = {'group': group}
    return render(request, 'app/faculty/supervisor/groups.html', context)


@login_required
def supervisor_new_group(request):
    """

    :param request:
    :return:
    """
    projects = None
    context = {'projects': projects}
    return render(request, 'app/faculty/supervisor/new_group.html', context)


@login_required
def supervisor_resubmit_project(request, pk):
    """
    Resubmit project request under supervision of
    supervisor
    :param request:
    :param pk:
    :return:
    """
    project = Project.objects.get(pk=pk)

    if request.user.is_authenticated:
        if request.user.faculty.is_supervisor:
            if request.method == "POST":
                project.title = request.POST["project_title"]
                project.description = request.POST['project_description']
                project.proposal = request.FILES['project_proposal']
                project.save()

                project.projectrequest.is_active = True
                project.projectrequest.is_need_changes = False
                project.projectrequest.save()

                title = "{} is resubmitted".format(project.title)
                msg = "The project '{}' is resubmitted. Kindly review it and forward it or reject it accordingly" \
                    .format(project.title)
                for coordinator in Faculty.objects.filter(is_coordinator=True).all():
                    notify_faculty(title, msg, request.user.faculty, coordinator)

                return redirect("faculty-supervisor-projects")

    context = {'project': project}
    return render(request, 'app/faculty/supervisor/new_project.html', context)


@login_required
def evaluation_committee_proposals(request):
    """
    Display only forwarded projects under Evaluation
    Committee privileges
    :param request:
    :return:
    """
    context = {"projects": ProjectRequest.objects.filter(is_forwarded=True).all()}
    return render(request, 'app/faculty/evaluation_committee/proposals.html', context)


@login_required
def evaluation_committee_approve(request, pk):
    """
    Approve project request under evaluation committee
    privileges
    :param request:
    :param pk:
    :return:
    """
    project_request = ProjectRequest.objects.get(pk=pk)
    context = {"project": project_request}
    if request.method == "POST":
        comment = request.POST["comment"]
        project_request.is_accepted = True
        project_request.is_active = True
        project_request.is_need_changes = False
        project_request.is_forwarded = False
        project_request.comments = comment
        project_request.save()

        title = "Your project is Approved"
        msg = "Your {} project is approved by Evaluation Committee".format(project_request.project.title)
        notify_faculty(title, msg, request.user.faculty, project_request.project.supervisor)

        title = "{}'s project '{}' was approved".format(project_request.project.supervisor,
                                                        project_request.project.title)
        msg = "{}'s project '{}' was approved by committee after evaluation process".format(
            project_request.project.supervisor,
            project_request.project.title)
        for co in Faculty.objects.filter(is_coordinator=True).all():
            notify_faculty(title, msg, request.user.faculty, co)

        return redirect('faculty-ec-proposals')
    return render(request, 'app/faculty/evaluation_committee/accept_project.html', context)


@login_required
def evaluation_committee_changes(request, pk):
    """
    Suggest changes against project request to supervisor
    under Evaluation Committee privileges
    :param request:
    :param pk:
    :return:
    """
    project_request = ProjectRequest.objects.get(pk=pk)
    context = {"project": project_request}
    if request.method == "POST":
        comment = request.POST["changes"]
        project_request.is_accepted = False
        project_request.is_active = True
        project_request.is_need_changes = True
        project_request.is_forwarded = False
        project_request.changes_required = comment
        project_request.save()

        title = "Your project Need Changes"
        msg = "Your {} project need following changes: {}".format(project_request.project.title, comment)
        notify_faculty(title, msg, request.user.faculty, project_request.project.supervisor)

        title = "{}'s project Need Changes".format(project_request.project.supervisor, project_request.project.title)
        msg = "{}'s project need following changes: {}".format(project_request.project.supervisor, comment)
        for co in Faculty.objects.filter(is_coordinator=True).all():
            notify_faculty(title, msg, request.user.faculty, co)

        return redirect('faculty-ec-proposals')
    return render(request, 'app/faculty/evaluation_committee/suggest_change.html', context)


def notify_faculty(title, text, sender, receiver):
    """
    Send notification to designated recipient
    :param title: Title of notification
    :param text: Message of notification
    :param sender: Sender of notification
    :param receiver: Receiver of notification
    :return:
    """
    notification = FacultyNotifications()
    notification.title = title
    notification.text = text
    notification.sender = sender
    notification.receiver = receiver
    notification.save()


# ******************************************* #
#                                             #
#             S T U D E N T S                 #
#                                             #
# ******************************************* #
@login_required
def student_portal(request):
    """
    Redirect to Student portal after successful login
    or registration
    :param request:
    :return:
    """
    return render(request, 'app/students/base.html')


@login_required
def student_projects(request):
    """
    Display any subject belongs to student
    :param request:
    :return:
    """
    projects = None
    context = {'projects': projects}
    return render(request, 'app/students/projects.html', context)


@login_required
def student_group_members(request):
    """
    Display all group members related to student's group
    :param request:
    :return:
    """
    group = None
    context = {'group': group}
    return render(request, 'app/students/group_members.html', context)


@login_required
def student_events(request):
    """
    Display all events related to student's group
    :param request:
    :return:
    """
    events = None
    context = {'events': events}
    return render(request, 'app/students/events.html', context)


@login_required
def student_notifications(request):
    """
    Display all events related to student's group
    :param request:
    :return:
    """
    notifications = None
    context = {'notifications': notifications}
    return render(request, 'app/students/notifications.html', context)


@login_required
def notify_student(title, text, sender, receiver):
    """
    Send notification to designated recipient
    :param title: Title of notification
    :param text: Message of notification
    :param sender: Sender of notification
    :param receiver: Receiver of notification
    :return:
    """
    notification = StudentNotifications()
    notification.title = title
    notification.text = text
    notification.sender = sender
    notification.receiver = receiver
    notification.save()
