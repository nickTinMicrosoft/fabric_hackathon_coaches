SET NOCOUNT ON;

IF (SELECT COUNT(*) FROM dbo.Parcel) <> 240
    THROW 51000, 'Expected exactly 240 synthetic parcels.', 1;

IF (SELECT COUNT(*) FROM dbo.Assessment) <> 480
    THROW 51001, 'Expected exactly 480 annual assessments.', 1;

IF (SELECT COUNT(*) FROM dbo.vw_PropertyTaxRoll) <> 480
    THROW 51002, 'The tax-roll view is incomplete.', 1;

IF EXISTS
(
    SELECT 1
    FROM dbo.vw_PropertyTaxRoll
    WHERE IsSynthetic <> 1
       OR EstimatedTax <= 0
       OR CurrencyCode <> 'CAD'
)
    THROW 51003, 'Tax-roll safety or calculation validation failed.', 1;

IF NOT EXISTS
(
    SELECT 1
    FROM dbo.Sale AS s
    JOIN dbo.Assessment AS a
      ON a.ParcelId = s.ParcelId
     AND a.TaxYear = 2025
    WHERE s.IsArmsLength = 1
      AND s.SalePrice > 0
      AND a.AssessedValue > 0
)
    THROW 51004, 'Comparable-sales data is unavailable.', 1;

SELECT
    NeighborhoodName,
    TaxYear,
    COUNT(*) AS ParcelCount,
    CAST(AVG(AssessedValue) AS decimal(14,2)) AS AverageAssessedValue,
    CAST(SUM(EstimatedTax) AS decimal(16,2)) AS EstimatedTaxTotal
FROM dbo.vw_PropertyTaxRoll
GROUP BY NeighborhoodName, TaxYear
ORDER BY TaxYear, NeighborhoodName;

SELECT
    'PASS' AS ValidationStatus,
    (SELECT COUNT(*) FROM dbo.Parcel) AS Parcels,
    (SELECT COUNT(*) FROM dbo.Assessment) AS Assessments,
    (SELECT COUNT(*) FROM dbo.Sale) AS ComparableSales;

