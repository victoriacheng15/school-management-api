-- Creating students table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    address TEXT,
    city TEXT,
    province TEXT,
    country TEXT,
    address_type TEXT CHECK(address_type IN ('local', 'permanent')),
    status TEXT CHECK(status IN ('active', 'inactive')) DEFAULT 'active',
    coop INTEGER DEFAULT 0,
    is_international INTEGER,
    program_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_archived INTEGER DEFAULT 0,
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_archived INTEGER DEFAULT 0,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Creating departments table
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_archived INTEGER DEFAULT 0
);

-- Creating programs table
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT CHECK(type IN ('bachelor', 'diploma', 'certificate')),
    department_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_archived INTEGER DEFAULT 0,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Creating courses table
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    title TEXT,
    code TEXT UNIQUE,
    term_id INTEGER,
    department_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_archived INTEGER DEFAULT 0,
    FOREIGN KEY (term_id) REFERENCES terms(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- Creating terms table
CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY,
    name TEXT,
    start_date DATE,
    end_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Creating enrollments table
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    grade TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Creating assignments table
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY,
    instructor_id INTEGER,
    course_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_archived INTEGER DEFAULT 0,
    FOREIGN KEY (instructor_id) REFERENCES instructors(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Creating course_schedule table
CREATE TABLE IF NOT EXISTS course_schedule (
    id INTEGER PRIMARY KEY,
    course_id INTEGER,
    day TEXT,
    time TEXT,
    room TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_archived INTEGER DEFAULT 0, 
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
