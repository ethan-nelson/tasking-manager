from enum import Enum


class ProjectStatus(Enum):
    """ Enum to describes all possible states of a Mapping Project """

    ARCHIVED = 0
    PUBLISHED = 1
    DRAFT = 2


class ProjectPriority(Enum):
    """ Enum to describe all possible project priority levels """

    URGENT = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class TaskCreationMode(Enum):
    """ Enum to describe task creation mode """

    GRID = 0
    ARBITRARY = 1


class TaskStatus(Enum):
    """ Enum describing available Task Statuses """

    READY = 0
    LOCKED_FOR_MAPPING = 1
    MAPPED = 2
    LOCKED_FOR_VALIDATION = 3
    VALIDATED = 4
    INVALIDATED = 5
    BADIMAGERY = 6  # Task cannot be mapped because of clouds, fuzzy imagery
    SPLIT = 7  # Task has been split


class MappingLevel(Enum):
    """ The mapping level the mapper has achieved """

    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


class MappingTypes(Enum):
    """ Enum describing types of mapping a project may specify"""

    ROADS = 1
    BUILDINGS = 2
    WATERWAYS = 3
    LAND_USE = 4
    OTHER = 5


class MappingNotAllowed(Enum):
    """ Enum describing reasons a user cannot map """

    USER_ALREADY_HAS_TASK_LOCKED = 100
    USER_NOT_CORRECT_MAPPING_LEVEL = 101
    USER_NOT_ACCEPTED_LICENSE = 102
    USER_NOT_ON_ALLOWED_LIST = 103
    PROJECT_NOT_PUBLISHED = 104


class ValidatingNotAllowed(Enum):
    """ Enum describing reasons a user cannot map """

    USER_NOT_VALIDATOR = 100
    USER_NOT_ACCEPTED_LICENSE = 101
    USER_NOT_ON_ALLOWED_LIST = 102
    PROJECT_NOT_PUBLISHED = 103


class UserRole(Enum):
    """ Describes the role a user can be assigned, app doesn't support multiple roles """

    READ_ONLY = -1
    MAPPER = 0
    ADMIN = 1
    PROJECT_MANAGER = 2
    VALIDATOR = 4


class Editors(Enum):
    """ Enum describing the possible editors for projects """

    ID = 0
    JOSM = 1
    POTLATCH_2 = 2
    FIELD_PAPERS = 3


class Event(Enum):
    """ Enum describing different event types """
    TASK_LOCKED_FOR_MAPPING = 1
    TASK_LOCKED_FOR_VALIDATION = 2
    TASK_MARKED_MAPPED = 3
    TASK_MARKED_BAD_IMAGERY = 4
    TASK_VALIDATED = 5
    TASK_INVALIDATED = 6
    TASK_UNLOCKED_FROM_MAPPING = 7
    TASK_UNLOCKED_FROM_VALIDATION = 8
    TASK_UNDO = 9
    PROJECT_CREATED = 10
    PROJECT_DRAFTED = 11
    PROJECT_PUBLISHED = 12
    PROJECT_UPDATED = 13
    PROJECT_ARCHIVED = 14
    PROJECT_RESET = 15
    PROJECT_BAD_IMAGERY_RESET = 16
    PROJECT_OWNER_CHANGED = 17
    USER_REGISTERED = 20
    USER_LEVEL_UP = 21
    USER_CHANGED_TO_MAPPER = 22
    USER_CHANGED_TO_VALIDATOR = 23
    USER_CHANGED_TO_PROJECT_MANAGER = 24
    USER_CHANGED_TO_ADMIN = 25
    USER_BLOCKED = 26
    IMAGERY_LICENSE_CREATED = 30
    IMAGERY_LICENSE_MODIFIED = 31
    PROJECT_ANNOTATION_REQUESTED = 50
