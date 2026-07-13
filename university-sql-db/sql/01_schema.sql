/* =====================================================================
   Intelligent University schema  (student / courses / school)
   Designed for DISCOVERABLE INTELLIGENCE, not just record-keeping:
     - Dimensions describe WHO/WHAT (Student, Program, Course, Professor, Term, Room)
     - Fact tables carry OUTCOMES and LEADING INDICATORS you can GROUP BY:
         * StudentTermStatus  -> retention & time-to-degree backbone
         * Enrollment         -> grades as quality points + withdrawals
         * CourseSection      -> cost + capacity utilisation
         * CourseReviewSignal -> AI-distilled sentiment/themes from the
                                 unstructured course reviews in Blob Storage
   StudentID is the stable key shared with the Cosmos grad-exam documents.
   Idempotent: drops existing objects first (old Brian tables included).
   ===================================================================== */

SET NOCOUNT ON;

/* ---- drop new-schema tables (child -> parent) ---- */
IF OBJECT_ID('dbo.CourseReviewSignal','U') IS NOT NULL DROP TABLE dbo.CourseReviewSignal;
IF OBJECT_ID('dbo.StudentTermStatus','U')  IS NOT NULL DROP TABLE dbo.StudentTermStatus;
IF OBJECT_ID('dbo.Enrollment','U')         IS NOT NULL DROP TABLE dbo.Enrollment;
IF OBJECT_ID('dbo.CourseSection','U')      IS NOT NULL DROP TABLE dbo.CourseSection;
IF OBJECT_ID('dbo.Student','U')            IS NOT NULL DROP TABLE dbo.Student;
IF OBJECT_ID('dbo.Course','U')             IS NOT NULL DROP TABLE dbo.Course;
IF OBJECT_ID('dbo.Professor','U')          IS NOT NULL DROP TABLE dbo.Professor;
IF OBJECT_ID('dbo.Program','U')            IS NOT NULL DROP TABLE dbo.Program;
IF OBJECT_ID('dbo.Classroom','U')          IS NOT NULL DROP TABLE dbo.Classroom;
IF OBJECT_ID('dbo.Building','U')           IS NOT NULL DROP TABLE dbo.Building;
IF OBJECT_ID('dbo.Term','U')               IS NOT NULL DROP TABLE dbo.Term;
IF OBJECT_ID('dbo.Department','U')         IS NOT NULL DROP TABLE dbo.Department;

/* ---- drop legacy (Brian Darcy 'Azure Days') tables if present ---- */
IF OBJECT_ID('dbo.CourseGrade','U')      IS NOT NULL DROP TABLE dbo.CourseGrade;
IF OBJECT_ID('dbo.CourseEnrollment','U') IS NOT NULL DROP TABLE dbo.CourseEnrollment;
IF OBJECT_ID('dbo.CourseOffering','U')   IS NOT NULL DROP TABLE dbo.CourseOffering;
IF OBJECT_ID('dbo.Grade','U')            IS NOT NULL DROP TABLE dbo.Grade;
IF OBJECT_ID('dbo.Semester','U')         IS NOT NULL DROP TABLE dbo.Semester;
GO

/* ============================ DIMENSIONS ============================ */

CREATE TABLE dbo.Department (
    DeptID   INT          NOT NULL PRIMARY KEY,
    DeptCode VARCHAR(8)   NOT NULL,
    DeptName VARCHAR(100) NOT NULL
);

CREATE TABLE dbo.Term (
    TermID    INT         NOT NULL PRIMARY KEY,
    TermName  VARCHAR(40) NOT NULL,
    StartDate DATE        NOT NULL,
    EndDate   DATE        NOT NULL,
    TermOrder INT         NOT NULL     -- chronological order, 1 = earliest
);

CREATE TABLE dbo.Building (
    BldID   INT          NOT NULL PRIMARY KEY,
    BldName VARCHAR(100) NOT NULL
);

CREATE TABLE dbo.Classroom (
    RoomID   INT         NOT NULL PRIMARY KEY,
    RoomName VARCHAR(40) NOT NULL,
    BldID    INT         NOT NULL REFERENCES dbo.Building(BldID),
    RoomType VARCHAR(20) NOT NULL,   -- Lecture | Lab | Research | Seminar
    Capacity INT         NOT NULL
);

CREATE TABLE dbo.Program (
    ProgramID       INT          NOT NULL PRIMARY KEY,
    ProgramName     VARCHAR(100) NOT NULL,
    DeptID          INT          NOT NULL REFERENCES dbo.Department(DeptID),
    DegreeType      VARCHAR(20)  NOT NULL,   -- BA | BS
    RequiredCredits INT          NOT NULL    -- credits needed to graduate
);

CREATE TABLE dbo.Professor (
    ProfID       INT          NOT NULL PRIMARY KEY,
    ProfName     VARCHAR(100) NOT NULL,
    DeptID       INT          NOT NULL REFERENCES dbo.Department(DeptID),
    Rank         VARCHAR(30)  NOT NULL,   -- Adjunct | Assistant | Associate | Full
    AnnualSalary INT          NOT NULL
);

CREATE TABLE dbo.Course (
    CrsID     INT          NOT NULL PRIMARY KEY,
    CrsNmbr   VARCHAR(12)  NOT NULL,
    CrsName   VARCHAR(120) NOT NULL,
    DeptID    INT          NOT NULL REFERENCES dbo.Department(DeptID),
    Credits   INT          NOT NULL,
    CrsLevel  INT          NOT NULL   -- 100/200/... course level
);

CREATE TABLE dbo.Student (
    StudentID          INT          NOT NULL PRIMARY KEY,  -- shared key w/ Cosmos
    StudentName        VARCHAR(100) NOT NULL,
    ProgramID          INT          NOT NULL REFERENCES dbo.Program(ProgramID),
    EnrollmentTermID   INT          NOT NULL REFERENCES dbo.Term(TermID),
    ExpectedGradTermID INT          NOT NULL REFERENCES dbo.Term(TermID),
    FirstGen           BIT          NOT NULL,   -- first-generation student
    Residency          VARCHAR(12)  NOT NULL,   -- InState | OutOfState
    AdmissionScore     INT          NOT NULL,   -- 900-1600, admission strength
    FinancialAidTier   INT          NOT NULL,   -- 0 (none) .. 3 (high need)
    CurrentStatus      VARCHAR(12)  NOT NULL    -- Active | Withdrawn | Graduated
);

/* ============================== FACTS ============================== */

CREATE TABLE dbo.CourseSection (
    SectionID      INT     NOT NULL PRIMARY KEY,
    CrsID          INT     NOT NULL REFERENCES dbo.Course(CrsID),
    TermID         INT     NOT NULL REFERENCES dbo.Term(TermID),
    ProfID         INT     NOT NULL REFERENCES dbo.Professor(ProfID),
    RoomID         INT     NOT NULL REFERENCES dbo.Classroom(RoomID),
    Capacity       INT     NOT NULL,
    SeatsFilled    INT     NOT NULL,
    InstructorCost DECIMAL(10,2) NOT NULL,  -- cost to run this section (instructor)
    RoomCost       DECIMAL(10,2) NOT NULL   -- facility cost for this section
);

CREATE TABLE dbo.Enrollment (
    EnrollmentID  INT         NOT NULL PRIMARY KEY,
    StudentID     INT         NOT NULL REFERENCES dbo.Student(StudentID),
    SectionID     INT         NOT NULL REFERENCES dbo.CourseSection(SectionID),
    CrsID         INT         NOT NULL REFERENCES dbo.Course(CrsID),
    TermID        INT         NOT NULL REFERENCES dbo.Term(TermID),
    LetterGrade   VARCHAR(2)  NULL,          -- NULL if withdrawn
    GradePoints   DECIMAL(3,2) NULL,         -- 0.00-4.00 quality points
    Withdrawn     BIT         NOT NULL,
    AttemptNumber INT         NOT NULL
);

/* One row per student per term -> the retention & progress backbone */
CREATE TABLE dbo.StudentTermStatus (
    StatusID          INT           NOT NULL PRIMARY KEY,
    StudentID         INT           NOT NULL REFERENCES dbo.Student(StudentID),
    TermID            INT           NOT NULL REFERENCES dbo.Term(TermID),
    Status            VARCHAR(12)   NOT NULL,  -- Enrolled | Withdrawn | Graduated | Leave
    TermGpa           DECIMAL(3,2)  NOT NULL,
    CumGpa            DECIMAL(3,2)  NOT NULL,
    CreditsAttempted  INT           NOT NULL,
    CreditsEarned     INT           NOT NULL,
    CumCreditsEarned  INT           NOT NULL,
    AttendancePct     INT           NOT NULL,  -- engagement signal 0-100
    LmsLogins         INT           NOT NULL,  -- engagement signal
    AdvisingVisits    INT           NOT NULL   -- engagement signal
);

/* AI-distilled signals from the free-text course reviews (Blob Storage).
   Raw review text stays in the storage account at BlobPath; the LLM output
   (sentiment/themes/recommendation) is materialised here for analytics. */
CREATE TABLE dbo.CourseReviewSignal (
    ReviewID        INT           NOT NULL PRIMARY KEY,
    StudentID       INT           NOT NULL REFERENCES dbo.Student(StudentID),
    SectionID       INT           NOT NULL REFERENCES dbo.CourseSection(SectionID),
    CrsID           INT           NOT NULL REFERENCES dbo.Course(CrsID),
    TermID          INT           NOT NULL REFERENCES dbo.Term(TermID),
    SubmittedDate   DATE          NOT NULL,
    SentimentScore  DECIMAL(3,2)  NOT NULL,   -- -1.00 (neg) .. 1.00 (pos)
    ThemePacing     BIT           NOT NULL,
    ThemeWorkload   BIT           NOT NULL,
    ThemeInstructor BIT           NOT NULL,
    ThemeMaterials  BIT           NOT NULL,
    WouldRecommend  BIT           NOT NULL,
    SummaryText     VARCHAR(300)  NOT NULL,
    BlobPath        VARCHAR(200)  NOT NULL     -- path to raw review in storage
);
GO

/* ---- helpful indexes for the analytics queries ---- */
CREATE INDEX IX_STS_Term        ON dbo.StudentTermStatus(TermID, Status);
CREATE INDEX IX_STS_Student     ON dbo.StudentTermStatus(StudentID, TermID);
CREATE INDEX IX_Enroll_Section  ON dbo.Enrollment(SectionID);
CREATE INDEX IX_Enroll_Student  ON dbo.Enrollment(StudentID, TermID);
CREATE INDEX IX_Review_Section  ON dbo.CourseReviewSignal(SectionID);
CREATE INDEX IX_Section_Course  ON dbo.CourseSection(CrsID, TermID);
GO
