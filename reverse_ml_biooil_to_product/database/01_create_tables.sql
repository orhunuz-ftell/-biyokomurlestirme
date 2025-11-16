/*
==============================================================================
REVERSE ML PROJECT - DATABASE EXTENSION
Script 01: Create Tables
==============================================================================
Purpose: Create 5 new tables to store Aspen simulation results
Database: BIOOIL
Author: Orhun Uzdiyem
Date: 2025-11-16
==============================================================================
*/

USE BIOOIL;
GO

PRINT 'Starting table creation...';
GO

-- ==============================================================================
-- TABLE 1: AspenSimulation
-- Purpose: Master table for each Aspen simulation run
-- ==============================================================================

IF OBJECT_ID('dbo.AspenSimulation', 'U') IS NOT NULL
BEGIN
    PRINT 'Dropping existing AspenSimulation table...';
    DROP TABLE dbo.AspenSimulation;
END
GO

PRINT 'Creating AspenSimulation table...';
CREATE TABLE AspenSimulation (
    SimulationId INT PRIMARY KEY IDENTITY(1,1),
    Biooil_Id INT NOT NULL,  -- FK to Biooil.BiooilId
    SimulationDate DATETIME NOT NULL DEFAULT GETDATE(),
    AspenVersion NVARCHAR(50) NULL,
    ConvergenceStatus NVARCHAR(20) NOT NULL CHECK (ConvergenceStatus IN ('Converged', 'Failed', 'Warning', 'Pending')),
    ConvergenceIterations INT NULL,
    MassBalanceError_percent DECIMAL(10,6) NULL,
    EnergyBalanceError_percent DECIMAL(10,6) NULL,
    Warnings NVARCHAR(MAX) NULL,
    Notes NVARCHAR(MAX) NULL,
    ValidationFlag BIT DEFAULT 0,  -- 1=validated, 0=needs review
    CreatedBy NVARCHAR(50) DEFAULT SYSTEM_USER,

    CONSTRAINT FK_AspenSimulation_Biooil
        FOREIGN KEY (Biooil_Id) REFERENCES Biooil(BiooilId)
        ON DELETE CASCADE
);
GO

PRINT 'AspenSimulation table created successfully.';
GO


-- ==============================================================================
-- TABLE 2: ReformingConditions
-- Purpose: Store process operating conditions for each simulation
-- ==============================================================================

IF OBJECT_ID('dbo.ReformingConditions', 'U') IS NOT NULL
BEGIN
    PRINT 'Dropping existing ReformingConditions table...';
    DROP TABLE dbo.ReformingConditions;
END
GO

PRINT 'Creating ReformingConditions table...';
CREATE TABLE ReformingConditions (
    ConditionId INT PRIMARY KEY IDENTITY(1,1),
    Simulation_Id INT NOT NULL,  -- FK to AspenSimulation

    -- Reformer Operating Conditions
    ReformerTemperature_C DECIMAL(10,2) NOT NULL,  -- 650-850°C
    ReformerPressure_bar DECIMAL(10,2) NOT NULL,   -- 5-30 bar
    SteamToCarbonRatio DECIMAL(10,4) NOT NULL,     -- 2-6

    -- Feed Conditions
    BiooilFeedRate_kgh DECIMAL(10,2) NULL,         -- kg/h
    SteamFeedRate_kgh DECIMAL(10,2) NULL,          -- kg/h

    -- Reactor Specifications
    ResidenceTime_min DECIMAL(10,2) NULL,          -- minutes in reformer
    CatalystWeight_kg DECIMAL(10,2) NULL,          -- Ni/Al2O3 catalyst
    GHSV_h1 DECIMAL(10,2) NULL,                    -- Gas hourly space velocity

    -- Other Reactors
    HTS_Temperature_C DECIMAL(10,2) NULL,          -- High-temp shift: ~370°C
    LTS_Temperature_C DECIMAL(10,2) NULL,          -- Low-temp shift: ~210°C
    PSA_Pressure_bar DECIMAL(10,2) NULL,           -- Pressure swing adsorption

    CONSTRAINT FK_ReformingConditions_Simulation
        FOREIGN KEY (Simulation_Id) REFERENCES AspenSimulation(SimulationId)
        ON DELETE CASCADE
);
GO

PRINT 'ReformingConditions table created successfully.';
GO


-- ==============================================================================
-- TABLE 3: HydrogenProduct
-- Purpose: Store hydrogen product properties (ML INPUTS)
-- ==============================================================================

IF OBJECT_ID('dbo.HydrogenProduct', 'U') IS NOT NULL
BEGIN
    PRINT 'Dropping existing HydrogenProduct table...';
    DROP TABLE dbo.HydrogenProduct;
END
GO

PRINT 'Creating HydrogenProduct table...';
CREATE TABLE HydrogenProduct (
    ProductId INT PRIMARY KEY IDENTITY(1,1),
    Simulation_Id INT NOT NULL,  -- FK to AspenSimulation

    -- Primary H2 Product Properties (ML INPUTS)
    H2_Yield_kg DECIMAL(10,4) NOT NULL,              -- kg H2 per 100 kg bio-oil
    H2_Purity_percent DECIMAL(10,4) NOT NULL,        -- >99.9% from PSA
    H2_FlowRate_kgh DECIMAL(10,4) NULL,              -- kg/h
    H2_FlowRate_Nm3h DECIMAL(10,4) NULL,             -- Nm³/h

    -- Product Gas Ratios (ML INPUTS)
    H2_CO_Ratio DECIMAL(10,4) NULL,                  -- Molar ratio
    H2_CO2_Ratio DECIMAL(10,4) NULL,                 -- Molar ratio

    -- By-product Quantities
    CO2_Production_kg DECIMAL(10,4) NULL,            -- kg CO2
    CO2_Purity_percent DECIMAL(10,4) NULL,           -- From CO2 removal unit

    -- Performance Indicators (ML INPUTS)
    CH4_Slip_percent DECIMAL(10,4) NULL,             -- Unreacted methane
    CO_Slip_ppm DECIMAL(10,4) NULL,                  -- CO in final H2 (<1%)
    Carbon_Conversion_percent DECIMAL(10,2) NULL,    -- % of carbon converted
    H2_Recovery_PSA_percent DECIMAL(10,2) NULL,      -- H2 recovery in PSA (85-92%)

    -- Energy Metrics (ML INPUTS)
    Energy_Efficiency_percent DECIMAL(10,2) NULL,    -- Overall energy efficiency
    Specific_Energy_MJperkg_H2 DECIMAL(10,2) NULL,   -- MJ per kg H2 produced

    -- Tail Gas (for energy balance)
    TailGas_FlowRate_kgh DECIMAL(10,4) NULL,         -- From PSA
    TailGas_HHV_MJperkg DECIMAL(10,2) NULL,          -- Heating value

    CONSTRAINT FK_HydrogenProduct_Simulation
        FOREIGN KEY (Simulation_Id) REFERENCES AspenSimulation(SimulationId)
        ON DELETE CASCADE
);
GO

PRINT 'HydrogenProduct table created successfully.';
GO


-- ==============================================================================
-- TABLE 4: SyngasComposition
-- Purpose: Detailed gas composition at various process points
-- ==============================================================================

IF OBJECT_ID('dbo.SyngasComposition', 'U') IS NOT NULL
BEGIN
    PRINT 'Dropping existing SyngasComposition table...';
    DROP TABLE dbo.SyngasComposition;
END
GO

PRINT 'Creating SyngasComposition table...';
CREATE TABLE SyngasComposition (
    SyngasId INT PRIMARY KEY IDENTITY(1,1),
    Simulation_Id INT NOT NULL,  -- FK to AspenSimulation
    StreamLocation NVARCHAR(50) NOT NULL,  -- 'Reformer_Out', 'HTS_Out', 'LTS_Out', 'PSA_In'

    -- Gas Composition (mol%)
    H2_molpercent DECIMAL(10,4) NULL,
    CO_molpercent DECIMAL(10,4) NULL,
    CO2_molpercent DECIMAL(10,4) NULL,
    CH4_molpercent DECIMAL(10,4) NULL,
    H2O_molpercent DECIMAL(10,4) NULL,
    N2_molpercent DECIMAL(10,4) NULL,

    -- Stream Properties
    Temperature_C DECIMAL(10,2) NULL,
    Pressure_bar DECIMAL(10,2) NULL,
    MassFlowRate_kgh DECIMAL(10,4) NULL,
    MolarFlowRate_kmolh DECIMAL(10,4) NULL,

    CONSTRAINT FK_SyngasComposition_Simulation
        FOREIGN KEY (Simulation_Id) REFERENCES AspenSimulation(SimulationId)
        ON DELETE CASCADE
);
GO

PRINT 'SyngasComposition table created successfully.';
GO


-- ==============================================================================
-- TABLE 5: EnergyBalance
-- Purpose: Energy inputs/outputs for process optimization
-- ==============================================================================

IF OBJECT_ID('dbo.EnergyBalance', 'U') IS NOT NULL
BEGIN
    PRINT 'Dropping existing EnergyBalance table...';
    DROP TABLE dbo.EnergyBalance;
END
GO

PRINT 'Creating EnergyBalance table...';
CREATE TABLE EnergyBalance (
    EnergyId INT PRIMARY KEY IDENTITY(1,1),
    Simulation_Id INT NOT NULL,  -- FK to AspenSimulation

    -- Energy Inputs (MJ)
    BiooilEnergy_HHV_MJ DECIMAL(10,2) NULL,          -- Bio-oil HHV
    PreheaterHeat_MJ DECIMAL(10,2) NULL,             -- External heat to preheater
    ReformerHeat_MJ DECIMAL(10,2) NULL,              -- External heat to reformer
    TotalEnergyInput_MJ DECIMAL(10,2) NULL,          -- Sum of inputs

    -- Energy Outputs (MJ)
    H2Product_HHV_MJ DECIMAL(10,2) NULL,             -- H2 energy content
    TailGasEnergy_MJ DECIMAL(10,2) NULL,             -- Tail gas (can be recovered)
    HeatRecovered_MJ DECIMAL(10,2) NULL,             -- Heat exchanger recovery
    HeatLoss_MJ DECIMAL(10,2) NULL,                  -- Stack loss, cooling

    -- Efficiency Calculations
    Thermal_Efficiency_percent DECIMAL(10,2) NULL,   -- H2 output / total input
    Carbon_Efficiency_percent DECIMAL(10,2) NULL,    -- Carbon to H2 / carbon in

    CONSTRAINT FK_EnergyBalance_Simulation
        FOREIGN KEY (Simulation_Id) REFERENCES AspenSimulation(SimulationId)
        ON DELETE CASCADE
);
GO

PRINT 'EnergyBalance table created successfully.';
GO


-- ==============================================================================
-- VERIFICATION
-- ==============================================================================

PRINT '';
PRINT '==============================================================================';
PRINT 'TABLE CREATION SUMMARY';
PRINT '==============================================================================';

SELECT
    TABLE_NAME,
    (SELECT COUNT(*)
     FROM INFORMATION_SCHEMA.COLUMNS
     WHERE TABLE_NAME = t.TABLE_NAME) as ColumnCount
FROM INFORMATION_SCHEMA.TABLES t
WHERE TABLE_NAME IN ('AspenSimulation', 'ReformingConditions', 'HydrogenProduct',
                     'SyngasComposition', 'EnergyBalance')
ORDER BY TABLE_NAME;

PRINT '';
PRINT 'All 5 tables created successfully!';
PRINT '==============================================================================';
GO
