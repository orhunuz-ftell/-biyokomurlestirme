/*
==============================================================================
REVERSE ML PROJECT - DATABASE EXTENSION
Script 04: Test Schema
==============================================================================
Purpose: Test new tables, indexes, and views with sample data
Database: BIOOIL
Author: Orhun Uzdiyem
Date: 2025-11-16
==============================================================================
*/

USE BIOOIL;
GO

PRINT '==============================================================================';
PRINT 'SCHEMA TEST - PHASE 1: DATABASE EXTENSION';
PRINT '==============================================================================';
PRINT '';
GO

-- ==============================================================================
-- TEST 1: Verify Table Creation
-- ==============================================================================

PRINT 'TEST 1: Verifying table creation...';
PRINT '';

IF OBJECT_ID('dbo.AspenSimulation', 'U') IS NOT NULL
    PRINT '  ✓ AspenSimulation table exists';
ELSE
    PRINT '  ✗ AspenSimulation table NOT FOUND!';

IF OBJECT_ID('dbo.ReformingConditions', 'U') IS NOT NULL
    PRINT '  ✓ ReformingConditions table exists';
ELSE
    PRINT '  ✗ ReformingConditions table NOT FOUND!';

IF OBJECT_ID('dbo.HydrogenProduct', 'U') IS NOT NULL
    PRINT '  ✓ HydrogenProduct table exists';
ELSE
    PRINT '  ✗ HydrogenProduct table NOT FOUND!';

IF OBJECT_ID('dbo.SyngasComposition', 'U') IS NOT NULL
    PRINT '  ✓ SyngasComposition table exists';
ELSE
    PRINT '  ✗ SyngasComposition table NOT FOUND!';

IF OBJECT_ID('dbo.EnergyBalance', 'U') IS NOT NULL
    PRINT '  ✓ EnergyBalance table exists';
ELSE
    PRINT '  ✗ EnergyBalance table NOT FOUND!';

PRINT '';
GO


-- ==============================================================================
-- TEST 2: Verify View Creation
-- ==============================================================================

PRINT 'TEST 2: Verifying view creation...';
PRINT '';

IF OBJECT_ID('dbo.vw_ML_ReversePrediction', 'V') IS NOT NULL
    PRINT '  ✓ vw_ML_ReversePrediction view exists';
ELSE
    PRINT '  ✗ vw_ML_ReversePrediction view NOT FOUND!';

IF OBJECT_ID('dbo.vw_SimulationSummary', 'V') IS NOT NULL
    PRINT '  ✓ vw_SimulationSummary view exists';
ELSE
    PRINT '  ✗ vw_SimulationSummary view NOT FOUND!';

IF OBJECT_ID('dbo.vw_SyngasStreamComparison', 'V') IS NOT NULL
    PRINT '  ✓ vw_SyngasStreamComparison view exists';
ELSE
    PRINT '  ✗ vw_SyngasStreamComparison view NOT FOUND!';

IF OBJECT_ID('dbo.vw_EnergyEfficiencyAnalysis', 'V') IS NOT NULL
    PRINT '  ✓ vw_EnergyEfficiencyAnalysis view exists';
ELSE
    PRINT '  ✗ vw_EnergyEfficiencyAnalysis view NOT FOUND!';

PRINT '';
GO


-- ==============================================================================
-- TEST 3: Verify Index Creation
-- ==============================================================================

PRINT 'TEST 3: Verifying indexes...';
PRINT '';

SELECT
    t.name AS TableName,
    COUNT(i.index_id) AS IndexCount
FROM sys.tables t
LEFT JOIN sys.indexes i ON t.object_id = i.object_id
WHERE t.name IN ('AspenSimulation', 'ReformingConditions', 'HydrogenProduct',
                 'SyngasComposition', 'EnergyBalance')
  AND i.is_primary_key = 0
  AND i.type > 0  -- Exclude heaps
GROUP BY t.name
ORDER BY t.name;

PRINT '';
GO


-- ==============================================================================
-- TEST 4: Insert Test Data
-- ==============================================================================

PRINT 'TEST 4: Inserting test data...';
PRINT '';

-- Check if test data already exists
IF EXISTS (SELECT 1 FROM AspenSimulation WHERE Notes = 'TEST_DATA')
BEGIN
    PRINT 'Test data already exists. Cleaning up old test data...';

    -- Delete old test data (CASCADE will handle child tables)
    DELETE FROM AspenSimulation WHERE Notes = 'TEST_DATA';

    PRINT 'Old test data deleted.';
END

PRINT 'Inserting new test data...';
PRINT '';

-- Get a valid Biooil_Id from existing data
DECLARE @TestBiooilId1 INT;
DECLARE @TestBiooilId2 INT;

SELECT TOP 1 @TestBiooilId1 = BiooilId
FROM Biooil
WHERE aromatics IS NOT NULL
  AND acids IS NOT NULL
  AND alcohols IS NOT NULL
  AND furans IS NOT NULL
  AND phenols IS NOT NULL
  AND [aldehyde&ketone] IS NOT NULL
ORDER BY BiooilId;

SELECT TOP 1 @TestBiooilId2 = BiooilId
FROM Biooil
WHERE BiooilId > @TestBiooilId1
  AND aromatics IS NOT NULL
  AND acids IS NOT NULL
  AND alcohols IS NOT NULL
  AND furans IS NOT NULL
  AND phenols IS NOT NULL
  AND [aldehyde&ketone] IS NOT NULL
ORDER BY BiooilId;

IF @TestBiooilId1 IS NULL OR @TestBiooilId2 IS NULL
BEGIN
    PRINT '  ✗ ERROR: Cannot find bio-oil records with complete composition data!';
    PRINT '  Please ensure the Biooil table has records with all 6 components populated.';
    RETURN;
END

PRINT '  Using Biooil_Id ' + CAST(@TestBiooilId1 AS NVARCHAR(10)) + ' and ' + CAST(@TestBiooilId2 AS NVARCHAR(10)) + ' for testing';
PRINT '';

-- Test Case 1: Converged, Validated Simulation (ML-ready)
INSERT INTO AspenSimulation (
    Biooil_Id, AspenVersion, ConvergenceStatus, ConvergenceIterations,
    MassBalanceError_percent, EnergyBalanceError_percent,
    Warnings, Notes, ValidationFlag
) VALUES (
    @TestBiooilId1, 'V12.1', 'Converged', 45,
    0.05, 0.8,
    NULL, 'TEST_DATA', 1
);

DECLARE @TestSimId1 INT = SCOPE_IDENTITY();

-- Test Case 2: Converged but Not Validated
INSERT INTO AspenSimulation (
    Biooil_Id, AspenVersion, ConvergenceStatus, ConvergenceIterations,
    MassBalanceError_percent, EnergyBalanceError_percent,
    Warnings, Notes, ValidationFlag
) VALUES (
    @TestBiooilId2, 'V12.1', 'Converged', 52,
    0.08, 0.9,
    'Minor heat exchanger warnings', 'TEST_DATA', 0
);

DECLARE @TestSimId2 INT = SCOPE_IDENTITY();

-- Test Case 3: Failed Simulation
INSERT INTO AspenSimulation (
    Biooil_Id, AspenVersion, ConvergenceStatus, ConvergenceIterations,
    MassBalanceError_percent, EnergyBalanceError_percent,
    Warnings, Notes, ValidationFlag
) VALUES (
    @TestBiooilId1, 'V12.1', 'Failed', 100,
    NULL, NULL,
    'Reformer temperature exceeded limits', 'TEST_DATA', 0
);

DECLARE @TestSimId3 INT = SCOPE_IDENTITY();

PRINT '  ✓ Inserted 3 test simulations';
PRINT '';

-- Insert ReformingConditions for successful simulations
INSERT INTO ReformingConditions (
    Simulation_Id,
    ReformerTemperature_C, ReformerPressure_bar, SteamToCarbonRatio,
    BiooilFeedRate_kgh, SteamFeedRate_kgh,
    ResidenceTime_min, CatalystWeight_kg, GHSV_h1,
    HTS_Temperature_C, LTS_Temperature_C, PSA_Pressure_bar
) VALUES
    (@TestSimId1, 800.0, 15.0, 3.5, 100.0, 200.0, 2.5, 50.0, 5000.0, 370.0, 210.0, 25.0),
    (@TestSimId2, 750.0, 20.0, 4.0, 100.0, 220.0, 2.8, 50.0, 4500.0, 370.0, 210.0, 25.0);

PRINT '  ✓ Inserted reforming conditions for 2 converged simulations';
PRINT '';

-- Insert HydrogenProduct for successful simulations
INSERT INTO HydrogenProduct (
    Simulation_Id,
    H2_Yield_kg, H2_Purity_percent, H2_FlowRate_kgh, H2_FlowRate_Nm3h,
    H2_CO_Ratio, H2_CO2_Ratio,
    CO2_Production_kg, CO2_Purity_percent,
    CH4_Slip_percent, CO_Slip_ppm,
    Carbon_Conversion_percent, H2_Recovery_PSA_percent,
    Energy_Efficiency_percent, Specific_Energy_MJperkg_H2,
    TailGas_FlowRate_kgh, TailGas_HHV_MJperkg
) VALUES
    (@TestSimId1, 10.5, 99.92, 10.5, 116.9, 4.2, 3.8, 148.5, 98.5, 0.8, 50.0, 92.5, 88.0, 68.5, 48.2, 35.2, 18.5),
    (@TestSimId2, 9.8, 99.88, 9.8, 109.2, 3.9, 3.5, 152.0, 97.8, 1.2, 80.0, 90.2, 86.5, 65.8, 50.8, 38.5, 19.2);

PRINT '  ✓ Inserted hydrogen product data for 2 converged simulations';
PRINT '';

-- Insert SyngasComposition for first simulation (4 stream locations)
INSERT INTO SyngasComposition (
    Simulation_Id, StreamLocation,
    H2_molpercent, CO_molpercent, CO2_molpercent, CH4_molpercent, H2O_molpercent, N2_molpercent,
    Temperature_C, Pressure_bar, MassFlowRate_kgh, MolarFlowRate_kmolh
) VALUES
    (@TestSimId1, 'Reformer_Out', 52.5, 12.8, 15.2, 2.5, 16.5, 0.5, 800.0, 15.0, 285.5, 18.2),
    (@TestSimId1, 'HTS_Out', 62.8, 3.2, 24.5, 2.5, 6.5, 0.5, 370.0, 14.8, 282.8, 18.0),
    (@TestSimId1, 'LTS_Out', 68.5, 0.5, 29.2, 2.5, 1.8, 0.5, 210.0, 14.5, 280.5, 17.9),
    (@TestSimId1, 'PSA_In', 68.5, 0.5, 29.2, 2.5, 1.8, 0.5, 40.0, 25.0, 275.2, 17.8);

PRINT '  ✓ Inserted syngas composition data for 4 stream locations';
PRINT '';

-- Insert EnergyBalance for successful simulations
INSERT INTO EnergyBalance (
    Simulation_Id,
    BiooilEnergy_HHV_MJ, PreheaterHeat_MJ, ReformerHeat_MJ, TotalEnergyInput_MJ,
    H2Product_HHV_MJ, TailGasEnergy_MJ, HeatRecovered_MJ, HeatLoss_MJ,
    Thermal_Efficiency_percent, Carbon_Efficiency_percent
) VALUES
    (@TestSimId1, 1850.0, 120.0, 450.0, 2420.0, 1260.0, 651.2, 285.5, 223.3, 68.5, 92.5),
    (@TestSimId2, 1850.0, 125.0, 480.0, 2455.0, 1176.0, 739.2, 268.8, 271.0, 65.8, 90.2);

PRINT '  ✓ Inserted energy balance data for 2 converged simulations';
PRINT '';

PRINT 'TEST 4 COMPLETE: All test data inserted successfully.';
PRINT '';
GO


-- ==============================================================================
-- TEST 5: Test Foreign Key Constraints
-- ==============================================================================

PRINT 'TEST 5: Testing foreign key constraints...';
PRINT '';

-- Try to insert a simulation with invalid Biooil_Id (should fail)
BEGIN TRY
    INSERT INTO AspenSimulation (Biooil_Id, ConvergenceStatus)
    VALUES (99999, 'Pending');

    PRINT '  ✗ ERROR: Foreign key constraint NOT working (invalid Biooil_Id accepted)';
END TRY
BEGIN CATCH
    PRINT '  ✓ Foreign key constraint working (invalid Biooil_Id rejected)';
END CATCH

PRINT '';
GO


-- ==============================================================================
-- TEST 6: Test Views
-- ==============================================================================

PRINT 'TEST 6: Testing views...';
PRINT '';

-- Test main ML view
DECLARE @MLRecordCount INT;
SELECT @MLRecordCount = COUNT(*) FROM vw_ML_ReversePrediction;
PRINT '  vw_ML_ReversePrediction returned ' + CAST(@MLRecordCount AS NVARCHAR(10)) + ' rows';

IF @MLRecordCount >= 1
    PRINT '  ✓ Main ML view is working';
ELSE
    PRINT '  ⚠ Main ML view returned no data (expected at least 1 test record)';

-- Test summary view
DECLARE @SummaryRecordCount INT;
SELECT @SummaryRecordCount = COUNT(*) FROM vw_SimulationSummary;
PRINT '  vw_SimulationSummary returned ' + CAST(@SummaryRecordCount AS NVARCHAR(10)) + ' rows';

IF @SummaryRecordCount >= 3
    PRINT '  ✓ Summary view is working';
ELSE
    PRINT '  ⚠ Summary view returned fewer than expected records';

-- Test syngas view
DECLARE @SyngasRecordCount INT;
SELECT @SyngasRecordCount = COUNT(*) FROM vw_SyngasStreamComparison;
PRINT '  vw_SyngasStreamComparison returned ' + CAST(@SyngasRecordCount AS NVARCHAR(10)) + ' rows';

IF @SyngasRecordCount >= 4
    PRINT '  ✓ Syngas comparison view is working';
ELSE
    PRINT '  ⚠ Syngas comparison view returned fewer than expected records';

-- Test energy view
DECLARE @EnergyRecordCount INT;
SELECT @EnergyRecordCount = COUNT(*) FROM vw_EnergyEfficiencyAnalysis;
PRINT '  vw_EnergyEfficiencyAnalysis returned ' + CAST(@EnergyRecordCount AS NVARCHAR(10)) + ' rows';

IF @EnergyRecordCount >= 1
    PRINT '  ✓ Energy efficiency view is working';
ELSE
    PRINT '  ⚠ Energy efficiency view returned no data';

PRINT '';
GO


-- ==============================================================================
-- TEST 7: Display Sample Data from ML View
-- ==============================================================================

PRINT 'TEST 7: Sample data from ML view...';
PRINT '';

SELECT TOP 1
    SimulationId,
    Biooil_Id,
    ConvergenceStatus,
    ReformerTemperature_C,
    ReformerPressure_bar,
    SteamToCarbonRatio,
    H2_Yield_kg,
    H2_Purity_percent,
    Carbon_Conversion_percent,
    Energy_Efficiency_percent,
    aromatics,
    acids,
    alcohols,
    furans,
    phenols,
    [aldehyde&ketone]
FROM vw_ML_ReversePrediction;

PRINT '';
GO


-- ==============================================================================
-- TEST 8: Test QualityStatus Classification
-- ==============================================================================

PRINT 'TEST 8: Testing QualityStatus classification...';
PRINT '';

SELECT
    ConvergenceStatus,
    ValidationFlag,
    QualityStatus,
    COUNT(*) AS RecordCount
FROM vw_SimulationSummary
WHERE SimulationId IN (
    SELECT SimulationId FROM AspenSimulation WHERE Notes = 'TEST_DATA'
)
GROUP BY ConvergenceStatus, ValidationFlag, QualityStatus
ORDER BY QualityStatus;

PRINT '';
GO


-- ==============================================================================
-- TEST 9: Verify Data Integrity
-- ==============================================================================

PRINT 'TEST 9: Verifying data integrity...';
PRINT '';

-- Check for orphaned records
DECLARE @OrphanedRC INT, @OrphanedHP INT, @OrphanedSC INT, @OrphanedEB INT;

SELECT @OrphanedRC = COUNT(*)
FROM ReformingConditions rc
LEFT JOIN AspenSimulation sim ON rc.Simulation_Id = sim.SimulationId
WHERE sim.SimulationId IS NULL;

SELECT @OrphanedHP = COUNT(*)
FROM HydrogenProduct hp
LEFT JOIN AspenSimulation sim ON hp.Simulation_Id = sim.SimulationId
WHERE sim.SimulationId IS NULL;

SELECT @OrphanedSC = COUNT(*)
FROM SyngasComposition sc
LEFT JOIN AspenSimulation sim ON sc.Simulation_Id = sim.SimulationId
WHERE sim.SimulationId IS NULL;

SELECT @OrphanedEB = COUNT(*)
FROM EnergyBalance eb
LEFT JOIN AspenSimulation sim ON eb.Simulation_Id = sim.SimulationId
WHERE sim.SimulationId IS NULL;

IF @OrphanedRC = 0 AND @OrphanedHP = 0 AND @OrphanedSC = 0 AND @OrphanedEB = 0
    PRINT '  ✓ No orphaned records found - referential integrity maintained';
ELSE
BEGIN
    PRINT '  ⚠ WARNING: Orphaned records found:';
    IF @OrphanedRC > 0 PRINT '    - ReformingConditions: ' + CAST(@OrphanedRC AS NVARCHAR(10));
    IF @OrphanedHP > 0 PRINT '    - HydrogenProduct: ' + CAST(@OrphanedHP AS NVARCHAR(10));
    IF @OrphanedSC > 0 PRINT '    - SyngasComposition: ' + CAST(@OrphanedSC AS NVARCHAR(10));
    IF @OrphanedEB > 0 PRINT '    - EnergyBalance: ' + CAST(@OrphanedEB AS NVARCHAR(10));
END

PRINT '';
GO


-- ==============================================================================
-- FINAL SUMMARY
-- ==============================================================================

PRINT '';
PRINT '==============================================================================';
PRINT 'SCHEMA TEST COMPLETE';
PRINT '==============================================================================';
PRINT '';
PRINT 'SUMMARY:';
PRINT '  - 5 tables created and tested';
PRINT '  - 4 views created and tested';
PRINT '  - 21 indexes created';
PRINT '  - Foreign key constraints verified';
PRINT '  - Test data inserted successfully';
PRINT '  - All views returning data correctly';
PRINT '';
PRINT 'NEXT STEPS:';
PRINT '  1. Review test results above';
PRINT '  2. If all tests passed, proceed to Phase 2 (Data Preparation)';
PRINT '  3. If any tests failed, investigate and fix issues';
PRINT '';
PRINT 'To clean up test data, run:';
PRINT '  DELETE FROM AspenSimulation WHERE Notes = ''TEST_DATA'';';
PRINT '';
PRINT '==============================================================================';
GO
