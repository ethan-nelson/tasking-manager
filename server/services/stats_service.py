from server import db
from server.models.dtos.project_dto import ProjectSummary
from server.models.dtos.stats_dto import ProjectContributionsDTO, UserContribution, Pagination, TaskHistoryDTO, \
    ProjectActivityDTO, AllUserDTO, UserDTO, UserActivityDTO, UserActionActivityDTO
from server.models.postgis.project import Project
from server.models.postgis.statuses import TaskStatus
from server.models.postgis.task import TaskHistory, User
from server.models.postgis.utils import timestamp, NotFound
from server.services.project_service import ProjectService
from server.services.users.user_service import UserService


class StatsService:
    @staticmethod
    def update_stats_after_task_state_change(project_id: int, user_id: int, new_state: TaskStatus, task_id: int):
        """ Update stats when a task has had a state change """
        if new_state in [TaskStatus.READY, TaskStatus.LOCKED_FOR_VALIDATION, TaskStatus.LOCKED_FOR_MAPPING]:
            return  # No stats to record for these states

        project = ProjectService.get_project_by_id(project_id)
        user = UserService.get_user_by_id(user_id)

        if new_state == TaskStatus.MAPPED:
            StatsService._set_counters_after_mapping(project, user)
        elif new_state == TaskStatus.INVALIDATED:
            StatsService._set_counters_after_invalidated(task_id, project, user)
        elif new_state == TaskStatus.VALIDATED:
            StatsService._set_counters_after_validated(project, user)
        elif new_state == TaskStatus.BADIMAGERY:
            StatsService._set_counters_after_bad_imagery(project)

        UserService.upsert_mapped_projects(user_id, project_id)
        project.last_updated = timestamp()

        # Transaction will be saved when task is saved
        return project, user

    @staticmethod
    def _set_counters_after_mapping(project: Project, user: User):
        """ Set counters after user has mapped a task """
        project.tasks_mapped += 1
        user.tasks_mapped += 1

    @staticmethod
    def _set_counters_after_validated(project: Project, user: User):
        """ Set counters after user has validated a task """
        project.tasks_validated += 1
        user.tasks_validated += 1

    @staticmethod
    def _set_counters_after_bad_imagery(project: Project):
        """ Set counters after user has marked a task as Bad Imagery """
        project.tasks_bad_imagery += 1

    @staticmethod
    def _set_counters_after_invalidated(task_id: int, project: Project, user: User):
        """ Set counters after user has validated a task """

        last_state = TaskHistory.get_last_status(project.id, task_id)

        if last_state == TaskStatus.BADIMAGERY:
            project.tasks_bad_imagery -= 1
        elif last_state == TaskStatus.MAPPED:
            project.tasks_mapped -= 1
        elif last_state == TaskStatus.VALIDATED:
            project.tasks_mapped -= 1
            project.tasks_validated -= 1

        user.tasks_invalidated += 1

    @staticmethod
    def get_latest_activity(project_id: int, page: int) -> ProjectActivityDTO:
        """ Gets all the activity on a project """

        results = db.session.query(TaskHistory.action, TaskHistory.action_date, TaskHistory.action_text, User.username) \
            .join(User).filter(TaskHistory.project_id == project_id, TaskHistory.action != 'COMMENT')\
            .order_by(TaskHistory.action_date.desc())\
            .paginate(page, 10, True)

        if results.total == 0:
            raise NotFound()

        activity_dto = ProjectActivityDTO()
        for item in results.items:
            history = TaskHistoryDTO()
            history.action = item.action
            history.action_text = item.action_text
            history.action_date = item.action_date
            history.action_by = item.username

            activity_dto.activity.append(history)

        activity_dto.pagination = Pagination(results)
        return activity_dto

    @staticmethod
    def get_user_contributions(project_id: int) -> ProjectContributionsDTO:
        """ Get all user contributions on a project"""
        contrib_query = '''select m.mapped_by, m.username, m.mapped, v.validated_by, v.username, v.validated
                             from (select t.mapped_by, u.username, count(t.mapped_by) mapped
                                     from tasks t,
                                          users u
                                    where t.mapped_by = u.id
                                      and t.project_id = {0}
                                      and t.mapped_by is not null
                                    group by t.mapped_by, u.username) m FULL OUTER JOIN
                                  (select t.validated_by, u.username, count(t.validated_by) validated
                                     from tasks t,
                                          users u
                                    where t.validated_by = u.id
                                      and t.project_id = {0}
                                      and t.validated_by is not null
                                    group by t.validated_by, u.username) v
                                       ON m.mapped_by = v.validated_by
        '''.format(project_id)

        results = db.engine.execute(contrib_query)
        if results.rowcount == 0:
            raise NotFound()

        contrib_dto = ProjectContributionsDTO()
        for row in results:
            user_contrib = UserContribution()
            user_contrib.username = row[1] if row[1] else row[4]
            user_contrib.mapped = row[2] if row[2] else 0
            user_contrib.validated = row[5] if row[5] else 0

            contrib_dto.user_contributions.append(user_contrib)

        return contrib_dto

    @staticmethod
    def get_all_user_stats() -> AllUserDTO:
        """ Get user done, validating, and invalidating information"""
        contrib_query = '''SELECT t.user_id, t.project_id, t.action_text, t.action_date
                             FROM task_history t
                            WHERE t.action_text in ('MAPPED', 'VALIDATED', 'INVALIDATED')
        '''

        results = db.engine.execute(contrib_query)
        if results.rowcount == 0:
            raise NotFound()

        results_dict = {}
        for row in results:
            if row[0] not in results_dict:
                results_dict[row[0]] = {row[1]: {'MAPPED': [], 'VALIDATED': [], 'INVALIDATED': []}}
            else:
                if row[1] not in results_dict[row[0]]:
                    results_dict[row[0]].update((row[1],{'MAPPED': [], 'VALIDATED': [], 'INVALIDATED': []}))
            results_dict[row[0]][row[1]][row[2]].append(row[3])

        all_users_dto = AllUserDTO()
        for user in results_dict:
            user_activity = UserDTO()
            user_activity.user_id = user
            for project in results_dict[user]:
                project_activity = UserActivityDTO()
                project_activity.project_id = project
                for action in results_dict[user][project]:
                    action_activity = UserActionActivityDTO()
                    action_activity.action_type = action
                    action_activity.datetimes = results_dict[user][project][action]
                    project_activity.action.append(action_activity)
                user_activity.activity.append(project_activity)
            all_users_dto.all_activity.append(user_activity)

        return all_users_dto
