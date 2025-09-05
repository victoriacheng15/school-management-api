from .student import (
    get_all_students,
    get_student_by_id,
    create_new_students,
    update_students,
    archive_students,
)

from .instructor import (
    get_all_instructors,
    get_instructor_by_id,
    create_new_instructors,
    update_instructors,
    archive_instructors,
)

from .department import (
    get_all_departments,
    get_department_by_id,
    create_new_departments,
    update_departments,
    archive_departments,
)

from .program import (
    get_all_programs,
    get_program_by_id,
    create_new_programs,
    update_programs,
    archive_programs,
)

from .course import (
    get_all_courses,
    get_course_by_id,
    create_new_courses,
    update_courses,
    archive_courses,
)

from .term import (
    get_all_terms,
    get_term_by_id,
    create_new_terms,
    update_terms,
    archive_terms,
)

from .enrollment import (
    get_all_enrollments,
    get_enrollment_by_id,
    create_new_enrollments,
    update_enrollments,
    archive_enrollments,
)

from .assignment import (
    get_all_assignments,
    get_assignment_by_id,
    create_new_assignments,
    update_assignments,
    archive_assignments,
)

from .course_schedule import (
    get_all_course_schedules,
    get_course_schedule_by_id,
    create_new_course_schedules,
    update_course_schedules,
    archive_course_schedules,
)
