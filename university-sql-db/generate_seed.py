#!/usr/bin/env python3
"""Generate seed data (02_seed.sql) for the intelligent university schema.

Design goal: produce data where INTELLIGENCE is *discoverable* -- i.e. real,
learnable correlations exist between leading indicators and outcomes:

  * A latent student "ability" (driven by AdmissionScore) drives grades,
    attendance and LMS engagement.
  * Retention (does the student appear next term?) is a function of ability,
    attendance, financial-aid need and first-gen status -> dropout risk is
    predictable, not random.
  * A few "weak" professors run low-quality sections -> lower grades, more
    withdrawals AND more negative course reviews -> sentiment correlates with
    section pass rate.
  * Cost is attached to every section -> cost-per-completed-credit is real.

Student IDs 1..55 and course IDs 1..54 match Brian Darcy's `Azure Days`
reference data, so this SQL DB joins the Cosmos grad-exam documents on
StudentID.  Deterministic: re-running yields identical SQL.
"""

import random
from pathlib import Path

random.seed(42)

OUT = Path(__file__).parent / "sql" / "02_seed.sql"

# --------------------------------------------------------------------------
# Reference data (aligned with Brian Darcy's Azure Days scripts / Cosmos seed)
# --------------------------------------------------------------------------
STUDENT_NAMES = {
    1: "Andrew Fender", 2: "Barbara Lawrence", 3: "Charles Cargo",
    4: "Daniel Edstrom", 5: "Edgar Ortiz", 6: "Liam Anderson",
    7: "Olivia Bennett", 8: "Noah Carter", 9: "Emma Davis",
    10: "Oliver Edwards", 11: "Ava Foster", 12: "Elijah Garcia",
    13: "Sophia Harris", 14: "William Johnson", 15: "Isabella King",
    16: "James Lewis", 17: "Mia Martinez", 18: "Benjamin Moore",
    19: "Charlotte Nelson", 20: "Lucas Perez", 21: "Amelia Roberts",
    22: "Henry Scott", 23: "Evelyn Turner", 24: "Alexander Walker",
    25: "Harper Young", 26: "Michael Allen", 27: "Abigail Baker",
    28: "Daniel Collins", 29: "Emily Cox", 30: "Matthew Diaz",
    31: "Elizabeth Evans", 32: "Joseph Flores", 33: "Ella Griffin",
    34: "David Hall", 35: "Avery Howard", 36: "Samuel Jenkins",
    37: "Sofia Kelly", 38: "Christopher Long", 39: "Scarlett Mitchell",
    40: "Andrew Morris", 41: "Chloe Murphy", 42: "Joshua Reed",
    43: "Victoria Rivera", 44: "Anthony Rogers", 45: "Grace Russell",
    46: "Ryan Sanchez", 47: "Lily Stewart", 48: "Nathan Torres",
    49: "Zoey Ward", 50: "Justin Watson", 51: "Hannah Wood",
    52: "Aaron Wright", 53: "Natalie Cooper", 54: "Dylan Price",
    55: "Leah Richardson",
}

COURSES = {
    1: ("ENG100", "Introduction to English Literature"),
    2: ("MATH100", "College Algebra"),
    3: ("HIST100", "Introduction to American History"),
    4: ("BIOL100", "Introduction to Biology"),
    5: ("CS101", "Introduction to Computer Science"),
    6: ("CS102", "Data Structures"), 7: ("CS103", "Algorithms"),
    8: ("CS104", "Database Systems"), 9: ("CS105", "Operating Systems"),
    10: ("CS106", "Computer Networks"), 11: ("CS107", "Software Engineering"),
    12: ("CS108", "Artificial Intelligence"), 13: ("CS109", "Machine Learning"),
    14: ("CS110", "Cloud Computing"), 15: ("BUS101", "Introduction to Business"),
    16: ("BUS102", "Marketing Principles"), 17: ("BUS103", "Financial Accounting"),
    18: ("BUS104", "Managerial Accounting"), 19: ("BUS105", "Business Analytics"),
    20: ("BUS106", "Operations Management"), 21: ("BUS107", "Organizational Behavior"),
    22: ("BUS108", "Corporate Finance"), 23: ("BUS109", "Strategic Management"),
    24: ("BUS110", "Entrepreneurship"), 25: ("MATH101", "Calculus I"),
    26: ("MATH102", "Calculus II"), 27: ("MATH103", "Linear Algebra"),
    28: ("MATH104", "Discrete Mathematics"), 29: ("MATH105", "Probability Theory"),
    30: ("MATH106", "Statistics"), 31: ("MATH107", "Numerical Methods"),
    32: ("MATH108", "Differential Equations"), 33: ("MATH109", "Abstract Algebra"),
    34: ("MATH110", "Real Analysis"), 35: ("ENG101", "English Composition"),
    36: ("ENG102", "Literature Analysis"), 37: ("ENG103", "Creative Writing"),
    38: ("ENG104", "Technical Writing"), 39: ("ENG105", "Public Speaking"),
    40: ("ENG106", "Modern Literature"), 41: ("ENG107", "World Literature"),
    42: ("ENG108", "Poetry Writing"), 43: ("ENG109", "Grammar and Syntax"),
    44: ("ENG110", "Rhetoric"), 45: ("SCI101", "General Biology"),
    46: ("SCI102", "General Chemistry"), 47: ("SCI103", "Physics I"),
    48: ("SCI104", "Physics II"), 49: ("SCI105", "Environmental Science"),
    50: ("SCI106", "Earth Science"), 51: ("SCI107", "Astronomy"),
    52: ("SCI108", "Genetics"), 53: ("SCI109", "Microbiology"),
    54: ("SCI110", "Organic Chemistry"),
}

# Department mapping by course-number prefix
DEPTS = {1: ("ENG", "English & Humanities"), 2: ("MATH", "Mathematics"),
         3: ("CS", "Computer Science"), 4: ("BUS", "Business"),
         5: ("SCI", "Natural Sciences")}
PREFIX_DEPT = {"ENG": 1, "HIST": 1, "MATH": 2, "CS": 3, "BUS": 4, "BIOL": 5, "SCI": 5}


def course_dept(crs_id):
    nmbr = COURSES[crs_id][0]
    prefix = "".join(c for c in nmbr if not c.isdigit())
    return PREFIX_DEPT[prefix]


def course_level(crs_id):
    digits = "".join(c for c in COURSES[crs_id][0] if c.isdigit())
    return (int(digits) // 100) * 100 or 100


COURSES_BY_DEPT = {}
for cid in COURSES:
    COURSES_BY_DEPT.setdefault(course_dept(cid), []).append(cid)

# Programs: one per department
PROGRAMS = {
    1: ("BA English",           1, "BA", 24),
    2: ("BS Mathematics",       2, "BS", 24),
    3: ("BS Computer Science",  3, "BS", 24),
    4: ("BS Business Admin",    4, "BS", 24),
    5: ("BS Natural Sciences",  5, "BS", 24),
}

# Terms (4 chronological terms)
TERMS = {
    1: ("Fall 2024",   "2024-09-01", "2024-12-15", 1),
    2: ("Spring 2025", "2025-01-15", "2025-05-15", 2),
    3: ("Fall 2025",   "2025-09-01", "2025-12-15", 3),
    4: ("Spring 2026", "2026-01-15", "2026-05-15", 4),
}
TERM_REVIEW_DATE = {1: "2024-12-18", 2: "2025-05-18", 3: "2025-12-18", 4: "2026-05-18"}

# Buildings & rooms (varied room types incl. Lab / Research / Seminar)
BUILDINGS = {1: "Science Hall", 2: "Liberal Arts Center", 3: "Innovation Commons"}
ROOMS = {
    1: ("SH-101", 1, "Lecture",  40), 2: ("SH-Lab-A", 1, "Lab", 24),
    3: ("SH-Research-1", 1, "Research", 12), 4: ("LA-201", 2, "Lecture", 45),
    5: ("LA-Seminar-1", 2, "Seminar", 18), 6: ("LA-105", 2, "Lecture", 35),
    7: ("IC-300", 3, "Lecture", 50), 8: ("IC-Lab-B", 3, "Lab", 28),
    9: ("IC-Research-2", 3, "Research", 10), 10: ("IC-Seminar-2", 3, "Seminar", 20),
}
ROOM_RATE = {"Lecture": 6.0, "Lab": 12.0, "Research": 18.0, "Seminar": 9.0}

# Professors (2 deliberately "weak" -> quality < 1 -> worse outcomes/reviews)
RANKS = ["Adjunct", "Assistant", "Associate", "Full"]
PROFESSORS = {}  # profId -> (name, deptId, rank, salary, quality)
_prof_names = [
    "Dr. Alan Reed", "Dr. Nina Patel", "Dr. Omar Haddad", "Dr. Grace Lin",
    "Dr. Victor Cho", "Dr. Priya Rao", "Dr. Ellen Frost", "Dr. Marcus Webb",
    "Dr. Sara Kim", "Dr. Ivan Petrov", "Dr. Tara Osei", "Dr. Leo Marsh",
]
_weak_profs = {3, 8}   # these two run low-quality sections
for pid, pname in enumerate(_prof_names, start=1):
    dept = ((pid - 1) % 5) + 1
    rank = RANKS[(pid * 7) % 4]
    salary = {"Adjunct": 55000, "Assistant": 82000,
              "Associate": 105000, "Full": 135000}[rank]
    quality = 0.72 if pid in _weak_profs else round(random.uniform(0.92, 1.05), 3)
    PROFESSORS[pid] = (pname, dept, rank, salary, quality)

PROFS_BY_DEPT = {}
for pid, (_, d, *_rest) in PROFESSORS.items():
    PROFS_BY_DEPT.setdefault(d, []).append(pid)

# --------------------------------------------------------------------------
# Student attributes (demographics + latent ability)
# --------------------------------------------------------------------------
students = {}
for sid in STUDENT_NAMES:
    program = ((sid - 1) % 5) + 1
    ability = min(1.0, max(0.05, random.gauss(0.6, 0.22)))
    admission = int(900 + ability * 700 + random.gauss(0, 40))
    admission = max(900, min(1600, admission))
    first_gen = 1 if random.random() < 0.35 else 0
    residency = "InState" if random.random() < 0.6 else "OutOfState"
    # higher need for first-gen students
    aid = random.choice([0, 1, 2, 3, 3]) if first_gen else random.choice([0, 0, 1, 2, 3])
    students[sid] = {
        "name": STUDENT_NAMES[sid], "program": program, "ability": ability,
        "admission": admission, "first_gen": first_gen, "residency": residency,
        "aid": aid, "status": "Active",
        "cum_credits": 0, "cum_qp": 0.0, "cum_graded_credits": 0,
        "taken": set(), "active": True,
    }

# --------------------------------------------------------------------------
# Simulation across the 4 terms
# --------------------------------------------------------------------------
sections = {}           # (crsId, termId) -> sectionId
section_rows = []       # SectionID, CrsID, TermID, ProfID, RoomID, Cap, Filled, InstrCost, RoomCost
section_seats = {}      # sectionId -> filled count
enrollment_rows = []
term_status_rows = []
review_rows = []

_sec_id = 0
_enr_id = 0
_sts_id = 0
_rev_id = 0
CREDITS = 3


def get_section(crs_id, term_id):
    global _sec_id
    key = (crs_id, term_id)
    if key in sections:
        return sections[key]
    _sec_id += 1
    dept = course_dept(crs_id)
    prof = random.choice(PROFS_BY_DEPT[dept])
    room = random.choice(list(ROOMS))
    cap = ROOMS[room][3]
    salary = PROFESSORS[prof][3]
    instr_cost = round(salary / 8.0, 2)          # ~1/8 of load per section
    room_cost = round(ROOM_RATE[ROOMS[room][2]] * cap * 15, 2)  # 15 sessions
    sections[key] = _sec_id
    section_seats[_sec_id] = 0
    section_rows.append([_sec_id, crs_id, term_id, prof, room, cap, 0,
                         instr_cost, room_cost])
    return _sec_id


def snap_grade(gp):
    table = [(3.85, "A", 4.0), (3.5, "A-", 3.7), (3.15, "B+", 3.3),
             (2.85, "B", 3.0), (2.5, "B-", 2.7), (2.15, "C+", 2.3),
             (1.85, "C", 2.0), (1.5, "C-", 1.7), (1.0, "D", 1.0),
             (-1, "F", 0.0)]
    for thr, letter, val in table:
        if gp >= thr:
            return letter, val
    return "F", 0.0


def pick_courses(stu, term_id, n=3):
    """Pick up to n new courses: mostly from the student's own department."""
    own = [c for c in COURSES_BY_DEPT[stu["program"]] if c not in stu["taken"]]
    others = [c for c in COURSES if c not in stu["taken"]
              and course_dept(c) != stu["program"]]
    random.shuffle(own)
    random.shuffle(others)
    chosen = own[:max(1, n - 1)] + others[:1]
    chosen = chosen[:n]
    return chosen


for term_id in sorted(TERMS):
    for sid, stu in students.items():
        if not stu["active"]:
            continue
        courses = pick_courses(stu, term_id)
        if not courses:
            continue

        term_qp, graded_credits, credits_att, credits_earned = 0.0, 0, 0, 0
        term_withdrawals = 0
        enroll_this_term = []

        for crs in courses:
            sec = get_section(crs, term_id)
            prof = section_rows[sec - 1][3]
            quality = PROFESSORS[prof][4]
            stu["taken"].add(crs)
            credits_att += CREDITS
            section_seats[sec] += 1

            # withdrawal probability: worse for low ability / weak section / high need
            wd_prob = 0.03 + (1 - stu["ability"]) * 0.14 \
                + (1.0 - quality) * 0.20 + stu["aid"] * 0.015
            withdrawn = random.random() < wd_prob

            if withdrawn:
                term_withdrawals += 1
                enroll_this_term.append((crs, sec, None, None, 1))
            else:
                base = stu["ability"] * 4.0 * quality + random.gauss(0, 0.45)
                base = min(4.0, max(0.0, base))
                letter, gp = snap_grade(base)
                term_qp += gp
                graded_credits += CREDITS
                if gp >= 1.0:
                    credits_earned += CREDITS
                enroll_this_term.append((crs, sec, letter, gp, 1))

        # write enrollment rows
        for (crs, sec, letter, gp, attempt) in enroll_this_term:
            _enr_id += 1
            lg = f"'{letter}'" if letter else "NULL"
            gpv = f"{gp:.2f}" if gp is not None else "NULL"
            wd = 1 if letter is None else 0
            enrollment_rows.append([_enr_id, sid, sec, crs, term_id, lg, gpv, wd, attempt])

        # update cumulative
        stu["cum_qp"] += term_qp
        stu["cum_graded_credits"] += graded_credits
        stu["cum_credits"] += credits_earned
        term_gpa = round(term_qp / graded_credits * CREDITS, 2) if graded_credits else 0.0
        cum_gpa = round(stu["cum_qp"] / stu["cum_graded_credits"] * CREDITS, 2) \
            if stu["cum_graded_credits"] else 0.0

        # engagement signals (correlate with ability; withdrawals depress them)
        attendance = int(min(100, max(40, 58 + stu["ability"] * 42
                                      + random.gauss(0, 6) - term_withdrawals * 6)))
        lms = int(max(5, attendance * 1.6 + random.gauss(0, 12)))
        advising = max(0, int(random.gauss(2.2 - stu["ability"] * 1.5, 1.0)))

        # determine status for this term
        required = PROGRAMS[stu["program"]][3]
        if stu["cum_credits"] >= required:
            status = "Graduated"
            stu["status"] = "Graduated"
            stu["active"] = False
        else:
            status = "Enrolled"
            # retention to NEXT term (skip decision on last term)
            if term_id != max(TERMS):
                keep = 0.55 + stu["ability"] * 0.42 + (attendance - 70) * 0.004 \
                    - stu["aid"] * 0.04 - stu["first_gen"] * 0.05
                if random.random() > keep:
                    stu["status"] = "Withdrawn"
                    stu["active"] = False

        _sts_id += 1
        term_status_rows.append([_sts_id, sid, term_id, "'" + status + "'", f"{term_gpa:.2f}",
                                 f"{cum_gpa:.2f}", credits_att, credits_earned,
                                 stu["cum_credits"], attendance, lms, advising])

        # course reviews (AI-distilled signals) for non-withdrawn enrollments
        for (crs, sec, letter, gp, attempt) in enroll_this_term:
            if letter is None or random.random() > 0.7:
                continue
            prof = section_rows[sec - 1][3]
            quality = PROFESSORS[prof][4]
            sentiment = max(-1.0, min(1.0,
                (gp - 2.0) / 2.0 * 0.6 + (quality - 0.9) * 2.2 + random.gauss(0, 0.18)))
            sentiment = round(sentiment, 2)
            neg = sentiment < 0
            theme_pacing = 1 if (neg and random.random() < 0.6) else 0
            theme_workload = 1 if (gp < 2.5 and random.random() < 0.5) else 0
            theme_instructor = 1 if (quality < 0.8 and random.random() < 0.8) else \
                               (1 if random.random() < 0.2 else 0)
            theme_materials = 1 if random.random() < 0.3 else 0
            recommend = 1 if sentiment > 0.1 else 0
            if sentiment > 0.4:
                summary = "Engaging course, clear instruction, would take again."
            elif sentiment > 0.0:
                summary = "Solid course overall with a few rough spots."
            elif sentiment > -0.4:
                summary = "Mixed experience; pacing and workload were challenging."
            else:
                summary = "Frustrating; unclear instruction and heavy workload."
            nmbr = COURSES[crs][0]
            blob = f"reviews/{TERMS[term_id][0].replace(' ', '')}/{nmbr}/student-{sid}.json"
            _rev_id += 1
            review_rows.append([_rev_id, sid, sec, crs, term_id,
                                TERM_REVIEW_DATE[term_id], f"{sentiment:.2f}",
                                theme_pacing, theme_workload, theme_instructor,
                                theme_materials, recommend, summary, blob])

# fill SeatsFilled
for row in section_rows:
    row[6] = section_seats[row[0]]

# --------------------------------------------------------------------------
# Emit SQL
# --------------------------------------------------------------------------
def q(s):
    return "'" + str(s).replace("'", "''") + "'"


def chunked_insert(f, table, columns, rows, size=200):
    if not rows:
        return
    collist = ", ".join(columns)
    for i in range(0, len(rows), size):
        batch = rows[i:i + size]
        f.write(f"INSERT INTO dbo.{table} ({collist}) VALUES\n")
        f.write(",\n".join("(" + ", ".join(str(v) for v in r) + ")" for r in batch))
        f.write(";\nGO\n")


with OUT.open("w", encoding="utf-8") as f:
    f.write("/* Auto-generated by generate_seed.py -- do not edit by hand. */\n")
    f.write("SET NOCOUNT ON;\nGO\n\n")

    # Department
    dept_rows = [[d, q(c), q(n)] for d, (c, n) in DEPTS.items()]
    chunked_insert(f, "Department", ["DeptID", "DeptCode", "DeptName"], dept_rows)

    # Term
    term_rows = [[t, q(n), q(sd), q(ed), o] for t, (n, sd, ed, o) in TERMS.items()]
    chunked_insert(f, "Term",
                   ["TermID", "TermName", "StartDate", "EndDate", "TermOrder"], term_rows)

    # Building
    bld_rows = [[b, q(n)] for b, n in BUILDINGS.items()]
    chunked_insert(f, "Building", ["BldID", "BldName"], bld_rows)

    # Classroom
    room_rows = [[r, q(n), b, q(rt), cap] for r, (n, b, rt, cap) in ROOMS.items()]
    chunked_insert(f, "Classroom",
                   ["RoomID", "RoomName", "BldID", "RoomType", "Capacity"], room_rows)

    # Program
    prog_rows = [[p, q(n), d, q(dt), rc] for p, (n, d, dt, rc) in PROGRAMS.items()]
    chunked_insert(f, "Program",
                   ["ProgramID", "ProgramName", "DeptID", "DegreeType",
                    "RequiredCredits"], prog_rows)

    # Professor
    prof_rows = [[p, q(n), d, q(rk), sal] for p, (n, d, rk, sal, _qy) in PROFESSORS.items()]
    chunked_insert(f, "Professor",
                   ["ProfID", "ProfName", "DeptID", "Rank", "AnnualSalary"], prof_rows)

    # Course
    crs_rows = [[c, q(nm), q(cn), course_dept(c), CREDITS, course_level(c)]
                for c, (nm, cn) in COURSES.items()]
    chunked_insert(f, "Course",
                   ["CrsID", "CrsNmbr", "CrsName", "DeptID", "Credits", "CrsLevel"],
                   crs_rows)

    # Student
    stu_rows = []
    for sid, s in students.items():
        exp_grad = 4
        stu_rows.append([sid, q(s["name"]), s["program"], 1, exp_grad,
                         s["first_gen"], q(s["residency"]), s["admission"],
                         s["aid"], q(s["status"])])
    chunked_insert(f, "Student",
                   ["StudentID", "StudentName", "ProgramID", "EnrollmentTermID",
                    "ExpectedGradTermID", "FirstGen", "Residency", "AdmissionScore",
                    "FinancialAidTier", "CurrentStatus"], stu_rows)

    # CourseSection
    chunked_insert(f, "CourseSection",
                   ["SectionID", "CrsID", "TermID", "ProfID", "RoomID", "Capacity",
                    "SeatsFilled", "InstructorCost", "RoomCost"], section_rows)

    # Enrollment
    chunked_insert(f, "Enrollment",
                   ["EnrollmentID", "StudentID", "SectionID", "CrsID", "TermID",
                    "LetterGrade", "GradePoints", "Withdrawn", "AttemptNumber"],
                   enrollment_rows)

    # StudentTermStatus
    chunked_insert(f, "StudentTermStatus",
                   ["StatusID", "StudentID", "TermID", "Status", "TermGpa", "CumGpa",
                    "CreditsAttempted", "CreditsEarned", "CumCreditsEarned",
                    "AttendancePct", "LmsLogins", "AdvisingVisits"], term_status_rows)

    # CourseReviewSignal
    rev_sql_rows = []
    for r in review_rows:
        rev_sql_rows.append([r[0], r[1], r[2], r[3], r[4], q(r[5]), r[6], r[7],
                             r[8], r[9], r[10], r[11], q(r[12]), q(r[13])])
    chunked_insert(f, "CourseReviewSignal",
                   ["ReviewID", "StudentID", "SectionID", "CrsID", "TermID",
                    "SubmittedDate", "SentimentScore", "ThemePacing", "ThemeWorkload",
                    "ThemeInstructor", "ThemeMaterials", "WouldRecommend",
                    "SummaryText", "BlobPath"], rev_sql_rows)

print(f"Wrote {OUT}")
print(f"  departments={len(DEPTS)} programs={len(PROGRAMS)} professors={len(PROFESSORS)}")
print(f"  courses={len(COURSES)} terms={len(TERMS)} rooms={len(ROOMS)}")
print(f"  students={len(students)} sections={len(section_rows)} "
      f"enrollments={len(enrollment_rows)}")
print(f"  term_status={len(term_status_rows)} reviews={len(review_rows)}")
grads = sum(1 for s in students.values() if s['status'] == 'Graduated')
withd = sum(1 for s in students.values() if s['status'] == 'Withdrawn')
active = sum(1 for s in students.values() if s['status'] == 'Active')
print(f"  outcomes: graduated={grads} withdrawn={withd} active={active}")
