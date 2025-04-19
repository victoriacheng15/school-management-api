-- Creating students table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    address TEXT,
    province_state TEXT,
    country TEXT,
    address_type TEXT CHECK(address_type IN ('local', 'permanent')),
    status TEXT CHECK(status IN ('active', 'inactive')),
    coop BOOLEAN,
    is_international BOOLEAN,
    program_id INTEGER,
    FOREIGN KEY (program_id) REFERENCES programs(id)
);

-- Creating instructors table
CREATE TABLE IF NOT EXISTS instructors (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    address TEXT,
    province TEXT,
    employment TEXT CHECK(employment IN ('full-time', 'part-time', 'adjunct')),
    status TEXT CHECK(status IN ('active', 'inactive')),
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Creating departments table
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Creating programs table
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Creating courses table
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    title TEXT,
    code TEXT UNIQUE,
    term_id INTEGER,
    department_id INTEGER,
    FOREIGN KEY (term_id) REFERENCES terms(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Creating terms table
CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY,
    name TEXT,
    start_date DATE,
    end_date DATE
);

-- Creating enrollments table (many-to-many between students and courses)
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    grade TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Creating assignments table (many-to-many between instructors and courses)
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY,
    instructor_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (instructor_id) REFERENCES instructors(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Creating course_schedule table (optional, depending on need)
CREATE TABLE IF NOT EXISTS course_schedule (
    id INTEGER PRIMARY KEY,
    course_id INTEGER,
    day TEXT,
    time TEXT,
    room TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
