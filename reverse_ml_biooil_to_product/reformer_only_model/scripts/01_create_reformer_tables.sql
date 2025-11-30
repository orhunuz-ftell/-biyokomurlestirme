-- ============================================================================
-- REFORMER-ONLY MODEL - DATABASE SCHEMA
-- ============================================================================
-- Purpose: Create new tables for simplified reformer equilibrium modeling
-- Author: Orhun Uzdiyem
-- Date: November 30, 2025
-- Database: BIOOIL on DESKTOP-DRO84HP\SQLEXPRESS
-- ============================================================================

USE BIOOIL;
GO

PRINT '========================================================================';
PRINT 'CREATING REFORMER-ONLY MODEL TABLES';
PRINT '========================================================================';
PRINT '';

-- ============================================================================
-- TABLE 1: ReformerSimulation (Master Table)
-- ============================================================================
-- Purpose: Store input parameters for each reformer simulation
-- Records: 1,170 (26 bio-oils × 45 process conditions)
-- ============================================================================

IF OBJECT_ID('dbo.ReformerSimulation', 'U') IS NOT NULL
BEGIN
    PRINT 'Dropping existing ReformerSimulation table...';
    DROP TABLE dbo.ReformerSimulation;
END
GO

PRINT 'Creating ReformerSimulation table...';

CREATE TABLE ReformerSimulation (
    -- Primary Key
    SimulationID INT PRIMARY KEY IDENTITY(1,1),

    -- Foreign Key to Bio-oil Composition
    BiooilID INT NOT NULL,
    CONSTRAINT FK_ReformerSim_Biooil FOREIGN KEY (BiooilID)
        REFERENCES Biooil(BiooilId),

    -- Process Conditions (Inputs)
    Temperature_C FLOAT NOT NULL,           -- Reformer temperature (650-850°C)
    Pressure_bar FLOAT NOT NULL,            -- Operating pressure (5-30 bar)
    SC_Ratio FLOAT NOT NULL,                -- Steam-to-carbon ratio (2-6)

    -- Simulation Metadata
    SimulationDate DATETIME DEFAULT GETDATE(),
    ConvergenceStatus VARCHAR(20) DEFAULT 'Converged',
    Notes VARCHAR(500),

    -- Constraints for data validation
    CONSTRAINT CK_ReformerSim_Temperature
        CHECK (Temperature_C BETWEEN 600 AND 900),
    CONSTRAINT CK_ReformerSim_Pressure
        CHECK (Pressure_bar BETWEEN 1 AND 50),
    CONSTRAINT CK_ReformerSim_SCRatio
        CHECK (SC_Ratio BETWEEN 1 AND 10),
    CONSTRAINT CK_ReformerSim_ConvergenceStatus
        CHECK (ConvergenceStatus IN ('Converged', 'Failed', 'Warning'))
);

-- Create indexes for faster queries
CREATE INDEX IX_ReformerSim_BiooilID ON ReformerSimulation(BiooilID);
CREATE INDEX IX_ReformerSim_Conditions ON ReformerSimulation(Temperature_C, Pressure_bar, SC_Ratio);

PRINT '  [OK] ReformerSimulation table created';
PRINT '';
GO

-- ============================================================================
-- TABLE 2: ReformerOutput (Equilibrium Composition)
-- ============================================================================
-- Purpose: Store syngas composition at reformer outlet
-- Records: 1,170 (one per simulation)
-- ============================================================================

IF OBJECT_ID('dbo.ReformerOutput', 'U') IS NOT NULL
BEGIN
    PRINT 'Dropping existing ReformerOutput table...';
    DROP TABLE dbo.ReformerOutput;
END
GO

PRINT 'Creating ReformerOutput table...';

CREATE TABLE ReformerOutput (
    -- Primary Key
    OutputID INT PRIMARY KEY IDENTITY(1,1),

    -- Foreign Key
    SimulationID INT NOT NULL,
    CONSTRAINT FK_ReformerOutput_Simulation FOREIGN KEY (SimulationID)
        REFERENCES ReformerSimulation(SimulationID) ON DELETE CASCADE,

    -- Major Species Composition (mol%)
    H2_molpercent FLOAT NOT NULL DEFAULT 0,           -- Hydrogen
    CO_molpercent FLOAT NOT NULL DEFAULT 0,           -- Carbon monoxide
    CO2_molpercent FLOAT NOT NULL DEFAULT 0,          -- Carbon dioxide
    CH4_molpercent FLOAT NOT NULL DEFAULT 0,          -- Methane
    H2O_molpercent FLOAT NOT NULL DEFAULT 0,          -- Water (unreacted steam)

    -- Minor Species (mol%)
    C2H4_molpercent FLOAT DEFAULT 0,        -- Ethylene
    C2H6_molpercent FLOAT DEFAULT 0,        -- Ethane
    C2H2_molpercent FLOAT DEFAULT 0,        -- Acetylene
    C3H6_molpercent FLOAT DEFAULT 0,        -- Propylene
    N2_molpercent FLOAT DEFAULT 0,          -- Nitrogen (if present)
    AR_molpercent FLOAT DEFAULT 0,          -- Argon (if present)

    -- Thermodynamic State Properties
    Temperature_K FLOAT NOT NULL,           -- Outlet temperature (K)
    Pressure_Pa FLOAT NOT NULL,             -- Outlet pressure (Pa)
    Enthalpy_J_mol FLOAT,                   -- Molar enthalpy (J/mol)
    Entropy_J_molK FLOAT,                   -- Molar entropy (J/mol·K)
    Density_kg_m3 FLOAT,                    -- Gas density (kg/m³)
    MeanMolecularWeight_g_mol FLOAT,        -- Average molecular weight (g/mol)

    -- Mass Balance Validation
    TotalMoleFraction FLOAT,                -- Sum of all mole fractions (should = 1.0)

    -- Constraints for data validation
    CONSTRAINT CK_ReformerOutput_MoleFractionSum
        CHECK (TotalMoleFraction IS NULL OR ABS(TotalMoleFraction - 1.0) < 0.01),
    CONSTRAINT CK_ReformerOutput_NonNegative
        CHECK (H2_molpercent >= 0 AND CO_molpercent >= 0 AND
               CO2_molpercent >= 0 AND CH4_molpercent >= 0 AND H2O_molpercent >= 0)
);

-- Create index for faster joins
CREATE INDEX IX_ReformerOutput_SimulationID ON ReformerOutput(SimulationID);

PRINT '  [OK] ReformerOutput table created';
PRINT '';
GO

-- ============================================================================
-- TABLE 3: ReformerPerformance (Calculated Metrics)
-- ============================================================================
-- Purpose: Store calculated performance metrics and ratios
-- Records: 1,170 (one per simulation)
-- ============================================================================

IF OBJECT_ID('dbo.ReformerPerformance', 'U') IS NOT NULL
BEGIN
    PRINT 'Dropping existing ReformerPerformance table...';
    DROP TABLE dbo.ReformerPerformance;
END
GO

PRINT 'Creating ReformerPerformance table...';

CREATE TABLE ReformerPerformance (
    -- Primary Key
    PerformanceID INT PRIMARY KEY IDENTITY(1,1),

    -- Foreign Key
    SimulationID INT NOT NULL,
    CONSTRAINT FK_ReformerPerf_Simulation FOREIGN KEY (SimulationID)
        REFERENCES ReformerSimulation(SimulationID) ON DELETE CASCADE,

    -- Key Product Ratios
    H2_CO_Ratio FLOAT,                      -- H2/CO molar ratio (important for syngas applications)
    H2_CO2_Ratio FLOAT,                     -- H2/CO2 molar ratio
    CO_CO2_Ratio FLOAT,                     -- CO/CO2 ratio (WGS equilibrium indicator)

    -- Dry Basis Composition (excluding H2O, normalized mol%)
    H2_DryBasis_molpercent FLOAT,           -- H2 on dry basis
    CO_DryBasis_molpercent FLOAT,           -- CO on dry basis
    CO2_DryBasis_molpercent FLOAT,          -- CO2 on dry basis
    CH4_DryBasis_molpercent FLOAT,          -- CH4 on dry basis

    -- Carbon Distribution (where did carbon atoms go?)
    Carbon_in_CO_percent FLOAT,             -- Carbon ending up as CO (%)
    Carbon_in_CO2_percent FLOAT,            -- Carbon ending up as CO2 (%)
    Carbon_in_CH4_percent FLOAT,            -- Carbon ending up as CH4 (%)
    Carbon_in_C2_percent FLOAT,             -- Carbon ending up as C2 species (%)
    Carbon_Total_percent FLOAT,             -- Total carbon recovered (should be ~100%)

    -- Hydrogen Distribution (where did hydrogen atoms go?)
    Hydrogen_in_H2_percent FLOAT,           -- Hydrogen ending up as H2 (%)
    Hydrogen_in_CH4_percent FLOAT,          -- Hydrogen ending up as CH4 (%)
    Hydrogen_in_H2O_percent FLOAT,          -- Hydrogen in unreacted steam (%)
    Hydrogen_Total_percent FLOAT,           -- Total hydrogen recovered (should be ~100%)

    -- Thermodynamic Indicators
    Equilibrium_Constant_WGS FLOAT,         -- Keq = (CO2·H2)/(CO·H2O) for WGS reaction
    ApproachToEquilibrium FLOAT,            -- How close to theoretical equilibrium (0-1)

    -- Selectivity Metrics
    H2_Selectivity FLOAT,                   -- Fraction of hydrogen converted to H2
    CO_Selectivity FLOAT,                   -- Fraction of carbon converted to CO vs CO2

    -- Quality Flags
    DataQualityFlag VARCHAR(20) DEFAULT 'Valid',  -- 'Valid', 'Warning', 'Invalid'

    CONSTRAINT CK_ReformerPerf_DataQuality
        CHECK (DataQualityFlag IN ('Valid', 'Warning', 'Invalid'))
);

-- Create index for faster joins
CREATE INDEX IX_ReformerPerf_SimulationID ON ReformerPerformance(SimulationID);

PRINT '  [OK] ReformerPerformance table created';
PRINT '';
GO

-- ============================================================================
-- VERIFICATION: Check that all tables were created
-- ============================================================================

PRINT '========================================================================';
PRINT 'VERIFICATION: Checking created tables';
PRINT '========================================================================';

SELECT
    TABLE_NAME,
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
     WHERE TABLE_NAME = t.TABLE_NAME) AS ColumnCount
FROM INFORMATION_SCHEMA.TABLES t
WHERE TABLE_NAME IN ('ReformerSimulation', 'ReformerOutput', 'ReformerPerformance')
ORDER BY TABLE_NAME;

PRINT '';
PRINT '========================================================================';
PRINT 'TABLE CREATION COMPLETE';
PRINT '========================================================================';
PRINT '';
PRINT 'Next steps:';
PRINT '  1. Run 02_reformer_simulator.py to generate 1,170 simulations';
PRINT '  2. Run 03_calculate_performance.py to compute metrics';
PRINT '  3. Run 04_export_ml_dataset.py to create CSV for ML';
PRINT '';

GO
