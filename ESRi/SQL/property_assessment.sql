SET NOCOUNT ON;
SET XACT_ABORT ON;

BEGIN TRANSACTION;

DROP VIEW IF EXISTS dbo.vw_PropertyTaxRoll;
DROP TABLE IF EXISTS dbo.Sale;
DROP TABLE IF EXISTS dbo.Assessment;
DROP TABLE IF EXISTS dbo.Building;
DROP TABLE IF EXISTS dbo.Parcel;
DROP TABLE IF EXISTS dbo.TaxRate;
DROP TABLE IF EXISTS dbo.PropertyClass;
DROP TABLE IF EXISTS dbo.Neighborhood;
DROP TABLE IF EXISTS dbo.Jurisdiction;

CREATE TABLE dbo.Jurisdiction
(
    JurisdictionId      int             NOT NULL PRIMARY KEY,
    JurisdictionName    nvarchar(100)   NOT NULL,
    CountryCode         char(2)         NOT NULL,
    RegionCode          nvarchar(10)    NOT NULL,
    CurrencyCode        char(3)         NOT NULL,
    AreaUnit            nvarchar(20)    NOT NULL,
    IsSynthetic         bit             NOT NULL
);

CREATE TABLE dbo.Neighborhood
(
    NeighborhoodId     varchar(10)     NOT NULL PRIMARY KEY,
    JurisdictionId     int             NOT NULL,
    NeighborhoodName   nvarchar(100)   NOT NULL,
    MarketArea          nvarchar(30)    NOT NULL,
    CONSTRAINT FK_Neighborhood_Jurisdiction
        FOREIGN KEY (JurisdictionId) REFERENCES dbo.Jurisdiction(JurisdictionId)
);

CREATE TABLE dbo.PropertyClass
(
    PropertyClassCode  varchar(10)     NOT NULL PRIMARY KEY,
    PropertyClassName  nvarchar(100)   NOT NULL,
    Description        nvarchar(250)   NOT NULL
);

CREATE TABLE dbo.TaxRate
(
    TaxYear             smallint        NOT NULL,
    PropertyClassCode   varchar(10)     NOT NULL,
    MunicipalRate       decimal(10,8)   NOT NULL,
    RegionalRate        decimal(10,8)   NOT NULL,
    EducationRate       decimal(10,8)   NOT NULL,
    CONSTRAINT PK_TaxRate PRIMARY KEY (TaxYear, PropertyClassCode),
    CONSTRAINT FK_TaxRate_PropertyClass
        FOREIGN KEY (PropertyClassCode) REFERENCES dbo.PropertyClass(PropertyClassCode)
);

CREATE TABLE dbo.Parcel
(
    ParcelId            varchar(20)     NOT NULL PRIMARY KEY,
    ParcelNumber        varchar(30)     NOT NULL UNIQUE,
    NeighborhoodId      varchar(10)     NOT NULL,
    PropertyClassCode   varchar(10)     NOT NULL,
    SyntheticAddress    nvarchar(150)   NOT NULL,
    PostalArea          varchar(7)      NOT NULL,
    Latitude            decimal(9,6)    NOT NULL,
    Longitude           decimal(9,6)    NOT NULL,
    LotAreaSquareMetres decimal(12,2)   NOT NULL,
    ZoningCode          varchar(12)     NOT NULL,
    CONSTRAINT FK_Parcel_Neighborhood
        FOREIGN KEY (NeighborhoodId) REFERENCES dbo.Neighborhood(NeighborhoodId),
    CONSTRAINT FK_Parcel_PropertyClass
        FOREIGN KEY (PropertyClassCode) REFERENCES dbo.PropertyClass(PropertyClassCode)
);

CREATE TABLE dbo.Building
(
    BuildingId          int             IDENTITY(1,1) NOT NULL PRIMARY KEY,
    ParcelId            varchar(20)     NOT NULL,
    BuildingType        nvarchar(50)    NOT NULL,
    YearBuilt           smallint        NOT NULL,
    FloorAreaSquareMetres decimal(12,2) NOT NULL,
    Storeys             decimal(4,1)    NOT NULL,
    ConditionCode       varchar(12)     NOT NULL,
    Bedrooms            tinyint         NULL,
    Bathrooms           decimal(3,1)    NULL,
    CONSTRAINT FK_Building_Parcel
        FOREIGN KEY (ParcelId) REFERENCES dbo.Parcel(ParcelId)
);

CREATE TABLE dbo.Assessment
(
    AssessmentId        int             IDENTITY(1,1) NOT NULL PRIMARY KEY,
    ParcelId            varchar(20)     NOT NULL,
    TaxYear             smallint        NOT NULL,
    ValuationDate       date            NOT NULL,
    LandValue           decimal(14,2)   NOT NULL,
    ImprovementValue    decimal(14,2)   NOT NULL,
    AssessedValue AS (LandValue + ImprovementValue) PERSISTED,
    ConfidenceScore     decimal(5,4)    NOT NULL,
    AssessmentStatus    varchar(20)     NOT NULL,
    CONSTRAINT UQ_Assessment_ParcelYear UNIQUE (ParcelId, TaxYear),
    CONSTRAINT FK_Assessment_Parcel
        FOREIGN KEY (ParcelId) REFERENCES dbo.Parcel(ParcelId)
);

CREATE TABLE dbo.Sale
(
    SaleId              int             IDENTITY(1,1) NOT NULL PRIMARY KEY,
    ParcelId            varchar(20)     NOT NULL,
    SaleDate            date            NOT NULL,
    SalePrice           decimal(14,2)   NOT NULL,
    SaleType            varchar(20)     NOT NULL,
    IsArmsLength        bit             NOT NULL,
    CONSTRAINT FK_Sale_Parcel
        FOREIGN KEY (ParcelId) REFERENCES dbo.Parcel(ParcelId)
);

INSERT dbo.Jurisdiction
    (JurisdictionId, JurisdictionName, CountryCode, RegionCode, CurrencyCode, AreaUnit, IsSynthetic)
VALUES
    (1, N'Sudsberry', 'CA', N'ON', 'CAD', N'square metres', 1);

INSERT dbo.Neighborhood
    (NeighborhoodId, JurisdictionId, NeighborhoodName, MarketArea)
VALUES
    ('NORTH', 1, N'North Ridge', N'Urban'),
    ('LAKE', 1, N'Lake Junction', N'Waterfront'),
    ('PINE', 1, N'Pine Crossing', N'Suburban'),
    ('COPPER', 1, N'Copper Works', N'Mixed Use'),
    ('VALLEY', 1, N'Valley East', N'Rural'),
    ('CENTRAL', 1, N'Central Sudsberry', N'Urban Core');

INSERT dbo.PropertyClass
    (PropertyClassCode, PropertyClassName, Description)
VALUES
    ('RES', N'Residential', N'Synthetic low- and medium-density residential property'),
    ('MUR', N'Multi-unit residential', N'Synthetic residential property with multiple dwelling units'),
    ('COM', N'Commercial', N'Synthetic retail, office, and service property'),
    ('AGR', N'Agricultural', N'Synthetic agricultural land and improvements');

INSERT dbo.TaxRate
    (TaxYear, PropertyClassCode, MunicipalRate, RegionalRate, EducationRate)
VALUES
    (2025, 'RES', 0.00780000, 0.00310000, 0.00150000),
    (2025, 'MUR', 0.00940000, 0.00370000, 0.00180000),
    (2025, 'COM', 0.01420000, 0.00510000, 0.00600000),
    (2025, 'AGR', 0.00210000, 0.00090000, 0.00040000),
    (2026, 'RES', 0.00805000, 0.00320000, 0.00155000),
    (2026, 'MUR', 0.00970000, 0.00385000, 0.00185000),
    (2026, 'COM', 0.01465000, 0.00525000, 0.00610000),
    (2026, 'AGR', 0.00220000, 0.00095000, 0.00042000);

;WITH Numbers AS
(
    SELECT TOP (240)
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n
    FROM sys.all_objects AS a
    CROSS JOIN sys.all_objects AS b
)
INSERT dbo.Parcel
(
    ParcelId,
    ParcelNumber,
    NeighborhoodId,
    PropertyClassCode,
    SyntheticAddress,
    PostalArea,
    Latitude,
    Longitude,
    LotAreaSquareMetres,
    ZoningCode
)
SELECT
    CONCAT('SUD-', RIGHT(CONCAT('00000', n), 5)),
    CONCAT('99-', RIGHT(CONCAT('0000', ((n - 1) / 20) + 1), 4), '-', RIGHT(CONCAT('0000', n), 4)),
    CASE n % 6
        WHEN 0 THEN 'NORTH'
        WHEN 1 THEN 'LAKE'
        WHEN 2 THEN 'PINE'
        WHEN 3 THEN 'COPPER'
        WHEN 4 THEN 'VALLEY'
        ELSE 'CENTRAL'
    END,
    CASE
        WHEN n % 17 = 0 THEN 'AGR'
        WHEN n % 11 = 0 THEN 'COM'
        WHEN n % 7 = 0 THEN 'MUR'
        ELSE 'RES'
    END,
    CONCAT(
        100 + n,
        N' ',
        CASE n % 8
            WHEN 0 THEN N'Aurora'
            WHEN 1 THEN N'Boreal'
            WHEN 2 THEN N'Copper'
            WHEN 3 THEN N'Granite'
            WHEN 4 THEN N'Juniper'
            WHEN 5 THEN N'Northern Light'
            WHEN 6 THEN N'Pinecone'
            ELSE N'Silver Birch'
        END,
        N' ',
        CASE n % 4 WHEN 0 THEN N'Road' WHEN 1 THEN N'Avenue' WHEN 2 THEN N'Lane' ELSE N'Drive' END
    ),
    CONCAT('S', n % 9, 'S ', (n * 3) % 9, 'B', (n * 7) % 9),
    CAST(46.430000 + ((n % 20) * 0.003100) AS decimal(9,6)),
    CAST(-81.060000 + (((n - 1) / 20) * 0.004200) AS decimal(9,6)),
    CAST(
        CASE
            WHEN n % 17 = 0 THEN 12000 + (n * 83)
            WHEN n % 11 = 0 THEN 900 + (n * 17)
            ELSE 420 + (n * 9)
        END
        AS decimal(12,2)
    ),
    CASE
        WHEN n % 17 = 0 THEN 'AG-1'
        WHEN n % 11 = 0 THEN 'C-2'
        WHEN n % 7 = 0 THEN 'RM-2'
        ELSE 'R-1'
    END
FROM Numbers;

INSERT dbo.Building
(
    ParcelId,
    BuildingType,
    YearBuilt,
    FloorAreaSquareMetres,
    Storeys,
    ConditionCode,
    Bedrooms,
    Bathrooms
)
SELECT
    ParcelId,
    CASE PropertyClassCode
        WHEN 'AGR' THEN N'Farm residence and outbuilding'
        WHEN 'COM' THEN N'Commercial building'
        WHEN 'MUR' THEN N'Multi-unit residence'
        ELSE CASE ABS(CHECKSUM(ParcelId)) % 3
            WHEN 0 THEN N'Detached residence'
            WHEN 1 THEN N'Semi-detached residence'
            ELSE N'Townhouse'
        END
    END,
    1955 + (ABS(CHECKSUM(ParcelId)) % 69),
    CAST(
        CASE PropertyClassCode
            WHEN 'AGR' THEN 180 + (ABS(CHECKSUM(ParcelId)) % 140)
            WHEN 'COM' THEN 300 + (ABS(CHECKSUM(ParcelId)) % 900)
            WHEN 'MUR' THEN 260 + (ABS(CHECKSUM(ParcelId)) % 500)
            ELSE 85 + (ABS(CHECKSUM(ParcelId)) % 190)
        END
        AS decimal(12,2)
    ),
    CASE PropertyClassCode
        WHEN 'COM' THEN CAST(1 + (ABS(CHECKSUM(ParcelId)) % 4) AS decimal(4,1))
        WHEN 'MUR' THEN CAST(2 + (ABS(CHECKSUM(ParcelId)) % 3) AS decimal(4,1))
        ELSE CAST(1 + (ABS(CHECKSUM(ParcelId)) % 2) AS decimal(4,1))
    END,
    CASE ABS(CHECKSUM(ParcelId)) % 5
        WHEN 0 THEN 'FAIR'
        WHEN 1 THEN 'GOOD'
        WHEN 2 THEN 'GOOD'
        WHEN 3 THEN 'AVERAGE'
        ELSE 'EXCELLENT'
    END,
    CASE WHEN PropertyClassCode IN ('RES', 'AGR') THEN 2 + (ABS(CHECKSUM(ParcelId)) % 4) END,
    CASE WHEN PropertyClassCode IN ('RES', 'AGR') THEN CAST(1 + ((ABS(CHECKSUM(ParcelId)) % 5) * 0.5) AS decimal(3,1)) END
FROM dbo.Parcel;

INSERT dbo.Assessment
(
    ParcelId,
    TaxYear,
    ValuationDate,
    LandValue,
    ImprovementValue,
    ConfidenceScore,
    AssessmentStatus
)
SELECT
    p.ParcelId,
    y.TaxYear,
    DATEFROMPARTS(y.TaxYear - 1, 12, 31),
    CAST(
        (p.LotAreaSquareMetres *
            CASE p.PropertyClassCode
                WHEN 'AGR' THEN 6
                WHEN 'COM' THEN 145
                WHEN 'MUR' THEN 118
                ELSE 92
            END) * y.YearFactor
        AS decimal(14,2)
    ),
    CAST(
        (b.FloorAreaSquareMetres *
            CASE p.PropertyClassCode
                WHEN 'AGR' THEN 980
                WHEN 'COM' THEN 1850
                WHEN 'MUR' THEN 2100
                ELSE 2450
            END *
            CASE b.ConditionCode
                WHEN 'FAIR' THEN 0.78
                WHEN 'AVERAGE' THEN 0.90
                WHEN 'EXCELLENT' THEN 1.12
                ELSE 1.00
            END) * y.YearFactor
        AS decimal(14,2)
    ),
    CAST(0.7600 + ((ABS(CHECKSUM(p.ParcelId, y.TaxYear)) % 2200) / 10000.0) AS decimal(5,4)),
    'Certified'
FROM dbo.Parcel AS p
JOIN dbo.Building AS b ON b.ParcelId = p.ParcelId
CROSS JOIN
(
    VALUES
        (CAST(2025 AS smallint), CAST(1.0000 AS decimal(8,4))),
        (CAST(2026 AS smallint), CAST(1.0475 AS decimal(8,4)))
) AS y(TaxYear, YearFactor);

INSERT dbo.Sale
(
    ParcelId,
    SaleDate,
    SalePrice,
    SaleType,
    IsArmsLength
)
SELECT
    a.ParcelId,
    DATEADD(day, ABS(CHECKSUM(a.ParcelId)) % 650, CONVERT(date, '2024-01-01')),
    CAST(
        a.AssessedValue *
        (0.86 + ((ABS(CHECKSUM(a.ParcelId, 'sale')) % 31) / 100.0))
        AS decimal(14,2)
    ),
    'Open market',
    1
FROM dbo.Assessment AS a
WHERE a.TaxYear = 2025
  AND ABS(CHECKSUM(a.ParcelId)) % 3 = 0;

EXEC
(
    N'CREATE VIEW dbo.vw_PropertyTaxRoll
      AS
      SELECT
          p.ParcelId,
          p.ParcelNumber,
          p.SyntheticAddress,
          p.NeighborhoodId,
          n.NeighborhoodName,
          p.PropertyClassCode,
          pc.PropertyClassName,
          a.TaxYear,
          a.LandValue,
          a.ImprovementValue,
          a.AssessedValue,
          tr.MunicipalRate + tr.RegionalRate + tr.EducationRate AS CombinedRate,
          CAST(a.AssessedValue * (tr.MunicipalRate + tr.RegionalRate + tr.EducationRate) AS decimal(14,2)) AS EstimatedTax,
          j.CurrencyCode,
          j.IsSynthetic
      FROM dbo.Parcel AS p
      JOIN dbo.Neighborhood AS n ON n.NeighborhoodId = p.NeighborhoodId
      JOIN dbo.Jurisdiction AS j ON j.JurisdictionId = n.JurisdictionId
      JOIN dbo.PropertyClass AS pc ON pc.PropertyClassCode = p.PropertyClassCode
      JOIN dbo.Assessment AS a ON a.ParcelId = p.ParcelId
      JOIN dbo.TaxRate AS tr
        ON tr.TaxYear = a.TaxYear
       AND tr.PropertyClassCode = p.PropertyClassCode;'
);

COMMIT TRANSACTION;

SELECT
    (SELECT COUNT(*) FROM dbo.Parcel) AS ParcelCount,
    (SELECT COUNT(*) FROM dbo.Assessment) AS AssessmentCount,
    (SELECT COUNT(*) FROM dbo.Sale) AS SaleCount,
    (SELECT COUNT(*) FROM dbo.vw_PropertyTaxRoll) AS TaxRollCount;

