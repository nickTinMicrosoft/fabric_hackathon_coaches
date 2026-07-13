/* =====================================================================
   03_queries.sql  -- "intelligence" queries over the sandbox schema.
   Each block answers one of the business questions the design targets.
   ===================================================================== */
SET NOCOUNT ON;

/* ---------------------------------------------------------------------
   1. RETENTION: which term-1 signals predict dropping out?
   --------------------------------------------------------------------- */
PRINT '=== 1. Retention: dropout vs term-1 signals ===';
WITH t1 AS (
    SELECT s.StudentID, s.CurrentStatus, s.FirstGen, s.FinancialAidTier,
           sts.TermGpa, sts.AttendancePct, sts.LmsLogins
    FROM dbo.Student s
    JOIN dbo.StudentTermStatus sts
      ON sts.StudentID = s.StudentID AND sts.TermID = 1)
SELECT CASE WHEN CurrentStatus = 'Withdrawn' THEN 'Dropped out'
            ELSE 'Retained / Graduated' END           AS Outcome,
       COUNT(*)                                        AS Students,
       CAST(AVG(TermGpa) AS DECIMAL(3,2))              AS AvgTerm1GPA,
       AVG(AttendancePct)                              AS AvgAttendance,
       AVG(LmsLogins)                                  AS AvgLmsLogins,
       CAST(AVG(CAST(FinancialAidTier AS FLOAT)) AS DECIMAL(3,2)) AS AvgAidTier,
       CAST(AVG(CAST(FirstGen AS FLOAT))         AS DECIMAL(3,2)) AS PctFirstGen
FROM t1
GROUP BY CASE WHEN CurrentStatus = 'Withdrawn' THEN 'Dropped out'
              ELSE 'Retained / Graduated' END;

/* ---------------------------------------------------------------------
   2. GRADUATION: credit trajectory vs requirement (who is off-pace?)
   --------------------------------------------------------------------- */
PRINT '';
PRINT '=== 2. Graduation: latest credit progress vs program requirement ===';
WITH latest AS (
    SELECT sts.StudentID, sts.CumCreditsEarned,
           ROW_NUMBER() OVER (PARTITION BY sts.StudentID ORDER BY sts.TermID DESC) rn
    FROM dbo.StudentTermStatus sts)
SELECT s.CurrentStatus,
       COUNT(*)                                        AS Students,
       AVG(l.CumCreditsEarned)                         AS AvgCreditsEarned,
       MIN(pr.RequiredCredits)                         AS RequiredCredits,
       CAST(AVG(100.0 * l.CumCreditsEarned / pr.RequiredCredits) AS DECIMAL(5,1)) AS PctToDegree
FROM latest l
JOIN dbo.Student s  ON s.StudentID = l.StudentID
JOIN dbo.Program pr ON pr.ProgramID = s.ProgramID
WHERE l.rn = 1
GROUP BY s.CurrentStatus;

/* ---------------------------------------------------------------------
   3. COST-EFFECTIVENESS: cost per COMPLETED credit (worst offenders)
   --------------------------------------------------------------------- */
PRINT '';
PRINT '=== 3. Cost-effectiveness: most expensive sections per earned credit ===';
SELECT TOP 10
       c.CrsNmbr, t.TermName, p.ProfName, cs.SeatsFilled, cs.Capacity,
       cs.InstructorCost + cs.RoomCost                 AS SectionCost,
       SUM(CASE WHEN e.GradePoints >= 1.0 THEN 3 ELSE 0 END) AS CreditsEarned,
       CAST((cs.InstructorCost + cs.RoomCost)
            / NULLIF(SUM(CASE WHEN e.GradePoints >= 1.0 THEN 3 ELSE 0 END), 0)
            AS DECIMAL(10,2))                           AS CostPerEarnedCredit
FROM dbo.CourseSection cs
JOIN dbo.Course c     ON c.CrsID   = cs.CrsID
JOIN dbo.Term t       ON t.TermID  = cs.TermID
JOIN dbo.Professor p  ON p.ProfID  = cs.ProfID
JOIN dbo.Enrollment e ON e.SectionID = cs.SectionID
GROUP BY c.CrsNmbr, t.TermName, p.ProfName, cs.SeatsFilled, cs.Capacity,
         cs.InstructorCost, cs.RoomCost
ORDER BY CostPerEarnedCredit DESC;

/* ---------------------------------------------------------------------
   4. REVIEWS (AI signal): sentiment tracks grade outcome
   --------------------------------------------------------------------- */
PRINT '';
PRINT '=== 4. Reviews: sentiment vs grade earned ===';
SELECT CASE WHEN e.GradePoints >= 3.0 THEN 'A/B (>=3.0)'
            WHEN e.GradePoints >= 2.0 THEN 'C (2.0-2.9)'
            ELSE 'D/F (<2.0)' END                      AS GradeBand,
       COUNT(*)                                        AS Reviews,
       CAST(AVG(r.SentimentScore) AS DECIMAL(3,2))     AS AvgSentiment,
       CAST(AVG(CAST(r.WouldRecommend AS FLOAT)) AS DECIMAL(3,2)) AS PctRecommend
FROM dbo.CourseReviewSignal r
JOIN dbo.Enrollment e
  ON e.StudentID = r.StudentID AND e.SectionID = r.SectionID
GROUP BY CASE WHEN e.GradePoints >= 3.0 THEN 'A/B (>=3.0)'
              WHEN e.GradePoints >= 2.0 THEN 'C (2.0-2.9)'
              ELSE 'D/F (<2.0)' END;

/* ---------------------------------------------------------------------
   5. INSTRUCTOR QUALITY: lowest-rated professors (find weak sections)
   --------------------------------------------------------------------- */
PRINT '';
PRINT '=== 5. Instructor quality: professors by avg review sentiment ===';
SELECT p.ProfName, d.DeptCode, COUNT(*) AS Reviews,
       CAST(AVG(r.SentimentScore) AS DECIMAL(3,2)) AS AvgSentiment
FROM dbo.CourseReviewSignal r
JOIN dbo.CourseSection cs ON cs.SectionID = r.SectionID
JOIN dbo.Professor p      ON p.ProfID = cs.ProfID
JOIN dbo.Department d     ON d.DeptID = p.DeptID
GROUP BY p.ProfName, d.DeptCode
ORDER BY AvgSentiment ASC;

/* ---------------------------------------------------------------------
   6. CROSS-STORE hook: SQL drivers ready to join Cosmos grad-exams on StudentID
   --------------------------------------------------------------------- */
PRINT '';
PRINT '=== 6. Per-student profile (join key for Cosmos grad-exam docs) ===';
SELECT TOP 10 s.StudentID, s.StudentName, pr.ProgramName, s.CurrentStatus,
       MAX(sts.CumGpa) AS CumGpa, MAX(sts.CumCreditsEarned) AS CreditsEarned
FROM dbo.Student s
JOIN dbo.Program pr ON pr.ProgramID = s.ProgramID
JOIN dbo.StudentTermStatus sts ON sts.StudentID = s.StudentID
GROUP BY s.StudentID, s.StudentName, pr.ProgramName, s.CurrentStatus
ORDER BY s.StudentID;
