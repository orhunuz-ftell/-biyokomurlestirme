/*
==============================================================================
REVERSE ML PROJECT - DATABASE EXTENSION
Script 02: Create Indexes
==============================================================================
Purpose: Create indexes for efficient querying of simulation data
Database: BIOOIL
Author: Orhun Uzdiyem
Date: 2025-11-16
==============================================================================
*/

USE BIOOIL;
GO

PRINT 'Starting index creation...';
PRINT '';
GO

-- ==============================================================================
-- INDEXES FOR: AspenSimulation
-- ==============================================================================

PRINT 'Creating indexes for AspenSimulation table...';

CREATE INDEX IX_AspenSimulation_Biooil
    ON AspenSimulation(Biooil_Id);

CREATE INDEX IX_AspenSimulation_Status
    ON AspenSimulation(ConvergenceStatus);

CREATE INDEX IX_AspenSimulation_Date
    ON AspenSimulation(SimulationDate DESC);

CREATE INDEX IX_AspenSimulation_ValidationFlag
    ON AspenSimulation(ValidationFlag);

-- Composite index for common queries
CREATE INDEX IX_AspenSimulation_Status_Flag
    ON AspenSimulation(ConvergenceStatus, ValidationFlag)
    INCLUDE (Biooil_Id, SimulationDate);

PRINT 'AspenSimulation indexes created (5 indexes).';
GO


-- ==============================================================================
-- INDEXES FOR: ReformingConditions
-- ==============================================================================

PRINT 'Creating indexes for ReformingConditions table...';

CREATE INDEX IX_ReformingConditions_Simulation
    ON ReformingConditions(Simulation_Id);

CREATE INDEX IX_ReformingConditions_Temp
    ON ReformingConditions(ReformerTemperature_C);

CREATE INDEX IX_ReformingConditions_Pressure
    ON ReformingConditions(ReformerPressure_bar);

CREATE INDEX IX_ReformingConditions_SCRatio
    ON ReformingConditions(SteamToCarbonRatio);

-- Composite index for process condition queries
CREATE INDEX IX_ReformingConditions_ProcessParams
    ON ReformingConditions(ReformerTemperature_C, ReformerPressure_bar, SteamToCarbonRatio);

PRINT 'ReformingConditions indexes created (5 indexes).';
GO


-- ==============================================================================
-- INDEXES FOR: HydrogenProduct
-- ==============================================================================

PRINT 'Creating indexes for HydrogenProduct table...';

CREATE INDEX IX_HydrogenProduct_Simulation
    ON HydrogenProduct(Simulation_Id);

CREATE INDEX IX_HydrogenProduct_Yield
    ON HydrogenProduct(H2_Yield_kg);

CREATE INDEX IX_HydrogenProduct_Purity
    ON HydrogenProduct(H2_Purity_percent);

CREATE INDEX IX_HydrogenProduct_Conversion
    ON HydrogenProduct(Carbon_Conversion_percent);

CREATE INDEX IX_HydrogenProduct_Efficiency
    ON HydrogenProduct(Energy_Efficiency_percent);

PRINT 'HydrogenProduct indexes created (5 indexes).';
GO


-- ==============================================================================
-- INDEXES FOR: SyngasComposition
-- ==============================================================================

PRINT 'Creating indexes for SyngasComposition table...';

CREATE INDEX IX_SyngasComposition_Simulation
    ON SyngasComposition(Simulation_Id);

CREATE INDEX IX_SyngasComposition_Location
    ON SyngasComposition(StreamLocation);

-- Composite index for location-specific queries
CREATE INDEX IX_SyngasComposition_Sim_Location
    ON SyngasComposition(Simulation_Id, StreamLocation);

PRINT 'SyngasComposition indexes created (3 indexes).';
GO


-- ==============================================================================
-- INDEXES FOR: EnergyBalance
-- ==============================================================================

PRINT 'Creating indexes for EnergyBalance table...';

CREATE INDEX IX_EnergyBalance_Simulation
    ON EnergyBalance(Simulation_Id);

CREATE INDEX IX_EnergyBalance_ThermalEfficiency
    ON EnergyBalance(Thermal_Efficiency_percent);

CREATE INDEX IX_EnergyBalance_CarbonEfficiency
    ON EnergyBalance(Carbon_Efficiency_percent);

PRINT 'EnergyBalance indexes created (3 indexes).';
GO


-- ==============================================================================
-- VERIFICATION
-- ==============================================================================

PRINT '';
PRINT '==============================================================================';
PRINT 'INDEX CREATION SUMMARY';
PRINT '==============================================================================';

SELECT
    t.name AS TableName,
    i.name AS IndexName,
    i.type_desc AS IndexType,
    COL_NAME(ic.object_id, ic.column_id) AS ColumnName
FROM sys.indexes i
INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
INNER JOIN sys.tables t ON i.object_id = t.object_id
WHERE t.name IN ('AspenSimulation', 'ReformingConditions', 'HydrogenProduct',
                 'SyngasComposition', 'EnergyBalance')
  AND i.is_primary_key = 0  -- Exclude primary keys
ORDER BY t.name, i.name, ic.key_ordinal;

PRINT '';
PRINT 'Total indexes created: 21';
PRINT 'All indexes created successfully!';
PRINT '==============================================================================';
GO
