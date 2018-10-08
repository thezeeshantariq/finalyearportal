from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
                  path('', views.index, name="home"),

                  # registration
                  path('signup/faculty/', views.signup_as_faculty, name="register-as-faculty"),
                  path('login/faculty/', views.login_as_faculty, name="login-as-faculty"),
                  path('signup/student/', views.signup_as_student, name="register-as-student"),
                  path('login/student/', views.login_as_student, name="login-as-student"),

                  path('logout/', views.user_logout, name="logout"),

                  # faculty
                  path('faculty/portal/', views.faculty_portal, name="faculty-portal"),

                  # faculty coordinator
                  path('faculty/portal/coordinator/faculty', views.coordinator_supervisors,
                       name="coordinator-supervisors"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/make-supervisor', views.make_supervisor,
                       name="make-supervisor"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/make-coordinator', views.make_coordinator,
                       name="make-coordinator"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/make-committee-head', views.make_committee_head,
                       name="make-committee-head"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/make-committee-member', views.make_committee_member,
                       name="make-committee-member"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/make-committee-evaluation',
                       views.make_evaluation_committee,
                       name="make-committee-evaluation"),

                  path('faculty/portal/coordinator/faculty/<int:pk>/remove-supervisor', views.remove_supervisor,
                       name="remove-supervisor"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/remove-coordinator', views.remove_coordinator,
                       name="remove-coordinator"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/remove-committee-head', views.remove_committee_head,
                       name="remove-committee-head"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/remove-committee-member',
                       views.remove_committee_member,
                       name="remove-committee-member"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/remove-committee-evaluation',
                       views.remove_evaluation_committee,
                       name="remove-committee-evaluation"),
                  path('faculty/portal/coordinator/projects/', views.coordinator_projects,
                       name="coordinator-projects"),
                  path('faculty/portal/coordinator/projects/<int:pk>/forward', views.coordinator_forward_project,
                       name="coordinator-forward-project"),
                  path('faculty/portal/coordinator/projects/<int:pk>/reject', views.coordinator_reject_project,
                       name="coordinator-reject-project"),

                  path('faculty/portal/coordinator/faculty/<int:pk>/activate', views.activate_faculty,
                       name="activate-faculty"),
                  path('faculty/portal/coordinator/faculty/<int:pk>/deactivate', views.deactivate_faculty,
                       name="deactivate-faculty"),
                  path('faculty/portal/coordinator/faculty/notifications/', views.faculty_notifications,
                       name="faculty-notifications"),
                  path('faculty/portal/coordinator/faculty/notifications/<int:pk>/read',
                       views.mark_faculty_notification_read,
                       name="mark-faculty-notification-read"),

                  # faculty supervisor
                  path('faculty/portal/supervisor/projects/', views.supervisor_projects,
                       name="faculty-supervisor-projects"),

                  path('faculty/portal/supervisor/projects/request', views.supervisor_new_project_request,
                       name="faculty-supervisor-project-request"),

                  path('faculty/portal/supervisor/projects/<int:pk>/resubmit', views.supervisor_resubmit_project,
                       name="faculty-supervisor-project-resubmit"),
                  path('faculty/portal/supervisor/groups/', views.supervisor_groups,
                       name="faculty-supervisor-groups"),
                  path('faculty/portal/supervisor/groups/new/', views.supervisor_new_group,
                       name="faculty-supervisor-new-group"),

                  # faculty evaluation committee
                  path('faculty/portal/evaluation-committee/proposals/', views.evaluation_committee_proposals,
                       name="faculty-ec-proposals"),
                  path('faculty/portal/evaluation-committee/<int:pk>/approve/', views.evaluation_committee_approve,
                       name="faculty-ec-approve"),
                  path('faculty/portal/evaluation-committee/<int:pk>/changes/', views.evaluation_committee_changes,
                       name="faculty-ec-changes"),
                  path('faculty/portal/evaluation-committee/<int:pk>/reject/', views.evaluation_committee_proposals,
                       name="faculty-ec-reject"),

                  # student
                  path('student/portal/', views.student_portal, name="student-portal"),
                  path('student/portal/notifications', views.student_notifications, name="student-notifications"),
                  path('student/portal/projects', views.student_projects, name="student-projects"),
                  path('student/portal/group', views.student_group_members, name="student-group"),
                  path('student/portal/events', views.student_events, name="student-events"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
