/*
==============================================================================
REVERSE ML PROJECT - DATABASE EXTENSION
Script 03: Create Views
==============================================================================
Purpose: Create views for ML data preparation and monitoring
Database: BIOOIL
Author: Orhun Uzdiyem
Date: 2025-11-16
==============================================================================
*/

USE BIOOIL;
GO

PRINT 'Starting view creation...';
PRINT '';
GO

-- ==============================================================================
-- VIEW 1: vw_ML_ReversePrediction
-- Purpose: Main view for ML training - joins simulation results with bio-oil data
-- ==============================================================================

IF OBJECT_ID('dbo.vw_ML_ReversePrediction', 'V') IS NOT NULL
BEGIN
    PRINT 'Dropping existing vw_ML_ReversePrediction view...';
    DROP VIEW dbo.vw_ML_ReversePrediction;
END
GO

PRINT 'Creating vw_ML_ReversePrediction view...';
GO

CREATE VIEW vw_ML_ReversePrediction AS
SELECT
    -- Simulation Metadata
    sim.SimulationId,
    sim.Biooil_Id,
    sim.SimulationDate,
    sim.ConvergenceStatus,

    -- Process Operating Conditions (Context)
    rc.ReformerTemperature_C,
    rc.ReformerPressure_bar,
    rc.SteamToCarbonRatio,
    rc.HTS_Temperature_C,
    rc.LTS_Temperature_C,
    rc.PSA_Pressure_bar,

    -- ========================================================================
    -- ML INPUTS: Hydrogen Product Properties (16 features)
    -- ========================================================================
    hp.H2_Yield_kg,
    hp.H2_Purity_percent,
    hp.H2_FlowRate_kgh,
    hp.H2_FlowRate_Nm3h,
    hp.H2_CO_Ratio,
    hp.H2_CO2_Ratio,
    hp.CO2_Production_kg,
    hp.CO2_Purity_percent,
    hp.CH4_Slip_percent,
    hp.CO_Slip_ppm,
    hp.Carbon_Conversion_percent,
    hp.H2_Recovery_PSA_percent,
    hp.Energy_Efficiency_percent,
    hp.Specific_Energy_MJperkg_H2,
    hp.TailGas_FlowRate_kgh,
    hp.TailGas_HHV_MJperkg,

    -- ========================================================================
    -- ML OUTPUTS: Bio-oil Composition (6 main components)
    -- ========================================================================
    b.aromatics,
    b.acids,
    b.alcohols,
    b.furans,
    b.phenols,
    b.[aldehyde&ketone],

    -- Bio-oil Reference Information
    bm.BiomassName AS BiomassType,
    e.ProcessTemperature AS PyrolysisTemp,
    bm.HHV,
    r.ReferenceCiting AS Reference

FROM AspenSimulation sim
INNER JOIN ReformingConditions rc ON sim.SimulationId = rc.Simulation_Id
INNER JOIN HydrogenProduct hp ON sim.SimulationId = hp.Simulation_Id
INNER JOIN Biooil b ON sim.Biooil_Id = b.BiooilId
LEFT JOIN Experiment e ON b.Experiment_Id = e.ExperimentId
LEFT JOIN Biomass bm ON e.Biomass_Id = bm.BiomassId
LEFT JOIN Reference r ON bm.Reference_Id = r.ReferenceId

WHERE
    -- Quality filters for ML training
    sim.ConvergenceStatus = 'Converged'
    AND sim.ValidationFlag = 1
    AND sim.MassBalanceError_percent < 0.1
    AND sim.EnergyBalanceError_percent < 1.0

    -- Ensure complete bio-oil composition data (6 main components)
    AND b.aromatics IS NOT NULL
    AND b.acids IS NOT NULL
    AND b.alcohols IS NOT NULL
    AND b.furans IS NOT NULL
    AND b.phenols IS NOT NULL
    AND b.[aldehyde&ketone] IS NOT NULL

    -- Ensure complete hydrogen product data
    AND hp.H2_Yield_kg IS NOT NULL
    AND hp.H2_Purity_percent IS NOT NULL
    AND hp.Carbon_Conversion_percent IS NOT NULL;

GO

PRINT 'vw_ML_ReversePrediction view created successfully.';
PRINT '';
GO


-- ==============================================================================
-- VIEW 2: vw_SimulationSummary
-- Purpose: High-level monitoring view for simulation runs
-- ==============================================================================

IF OBJECT_ID('dbo.vw_SimulationSummary', 'V') IS NOT NULL
BEGIN
    PRINT 'Dropping existing vw_SimulationSummary view...';
    DROP VIEW dbo.vw_SimulationSummary;
END
GO

PRINT 'Creating vw_SimulationSummary view...';
GO

CREATE VIEW vw_SimulationSummary AS
SELECT
    sim.SimulationId,
    sim.Biooil_Id,
    sim.SimulationDate,
    sim.ConvergenceStatus,
    sim.ValidationFlag,
    sim.MassBalanceError_percent,
    sim.EnergyBalanceError_percent,

    -- Bio-oil information
    bm.BiomassName AS BiomassType,
    r.ReferenceCiting AS Reference,

    -- Process conditions summary
    rc.ReformerTemperature_C,
    rc.ReformerPressure_bar,
    rc.SteamToCarbonRatio,

    -- Key performance indicators
    hp.H2_Yield_kg,
    hp.H2_Purity_percent,
    hp.Carbon_Conversion_percent,
    hp.Energy_Efficiency_percent,

    -- Energy balance summary
    eb.Thermal_Efficiency_percent,
    eb.Carbon_Efficiency_percent,

    -- Quality status
    CASE
        WHEN sim.ConvergenceStatus = 'Converged'
             AND sim.ValidationFlag = 1
             AND sim.MassBalanceError_percent < 0.1
             AND sim.EnergyBalanceError_percent < 1.0
             AND hp.H2_Yield_kg IS NOT NULL
             AND b.aromatics IS NOT NULL
             AND b.acids IS NOT NULL
             AND b.alcohols IS NOT NULL
             AND b.furans IS NOT NULL
             AND b.phenols IS NOT NULL
             AND b.[aldehyde&ketone] IS NOT NULL
        THEN 'ML_READY'
        WHEN sim.ConvergenceStatus = 'Converged'
             AND sim.ValidationFlag = 1
        THEN 'VALIDATED'
        WHEN sim.ConvergenceStatus = 'Converged'
        THEN 'NEEDS_VALIDATION'
        WHEN sim.ConvergenceStatus = 'Failed'
        THEN 'FAILED'
        WHEN sim.ConvergenceStatus = 'Warning'
        THEN 'WARNING'
        ELSE 'PENDING'
    END AS QualityStatus

FROM AspenSimulation sim
LEFT JOIN ReformingConditions rc ON sim.SimulationId = rc.Simulation_Id
LEFT JOIN HydrogenProduct hp ON sim.SimulationId = hp.Simulation_Id
LEFT JOIN EnergyBalance eb ON sim.SimulationId = eb.Simulation_Id
LEFT JOIN Biooil b ON sim.Biooil_Id = b.BiooilId
LEFT JOIN Experiment e ON b.Experiment_Id = e.ExperimentId
LEFT JOIN Biomass bm ON e.Biomass_Id = bm.BiomassId
LEFT JOIN Reference r ON bm.Reference_Id = r.ReferenceId;

GO

PRINT 'vw_SimulationSummary view created successfully.';
PRINT '';
GO


-- ==============================================================================
-- VIEW 3: vw_SyngasStreamComparison
-- Purpose: Compare syngas composition at different process locations
-- ==============================================================================

IF OBJECT_ID('dbo.vw_SyngasStreamComparison', 'V') IS NOT NULL
BEGIN
    PRINT 'Dropping existing vw_SyngasStreamComparison view...';
    DROP VIEW dbo.vw_SyngasStreamComparison;
END
GO

PRINT 'Creating vw_SyngasStreamComparison view...';
GO

CREATE VIEW vw_SyngasStreamComparison AS
SELECT
    sc.Simulation_Id,
    sc.StreamLocation,

    -- Gas composition (mol%)
    sc.H2_molpercent,
    sc.CO_molpercent,
    sc.CO2_molpercent,
    sc.CH4_molpercent,
    sc.H2O_molpercent,
    sc.N2_molpercent,

    -- Stream properties
    sc.Temperature_C,
    sc.Pressure_bar,
    sc.MassFlowRate_kgh,
    sc.MolarFlowRate_kmolh,

    -- Process conditions from parent simulation
    rc.ReformerTemperature_C,
    rc.ReformerPressure_bar,
    rc.SteamToCarbonRatio,

    -- Key product metrics
    hp.H2_Yield_kg,
    hp.Carbon_Conversion_percent

FROM SyngasComposition sc
INNER JOIN AspenSimulation sim ON sc.Simulation_Id = sim.SimulationId
INNER JOIN ReformingConditions rc ON sim.SimulationId = rc.Simulation_Id
INNER JOIN HydrogenProduct hp ON sim.SimulationId = hp.Simulation_Id

WHERE sim.ConvergenceStatus = 'Converged';

GO

PRINT 'vw_SyngasStreamComparison view created successfully.';
PRINT '';
GO


-- ==============================================================================
-- VIEW 4: vw_EnergyEfficiencyAnalysis
-- Purpose: Energy balance analysis for process optimization
-- ==============================================================================

IF OBJECT_ID('dbo.vw_EnergyEfficiencyAnalysis', 'V') IS NOT NULL
BEGIN
    PRINT 'Dropping existing vw_EnergyEfficiencyAnalysis view...';
    DROP VIEW dbo.vw_EnergyEfficiencyAnalysis;
END
GO

PRINT 'Creating vw_EnergyEfficiencyAnalysis view...';
GO

CREATE VIEW vw_EnergyEfficiencyAnalysis AS
SELECT
    sim.SimulationId,
    sim.Biooil_Id,
    bm.BiomassName AS BiomassType,

    -- Process conditions
    rc.ReformerTemperature_C,
    rc.ReformerPressure_bar,
    rc.SteamToCarbonRatio,

    -- Energy inputs (MJ)
    eb.BiooilEnergy_HHV_MJ,
    eb.PreheaterHeat_MJ,
    eb.ReformerHeat_MJ,
    eb.TotalEnergyInput_MJ,

    -- Energy outputs (MJ)
    eb.H2Product_HHV_MJ,
    eb.TailGasEnergy_MJ,
    eb.HeatRecovered_MJ,
    eb.HeatLoss_MJ,

    -- Efficiency metrics
    eb.Thermal_Efficiency_percent,
    eb.Carbon_Efficiency_percent,

    -- Product metrics
    hp.H2_Yield_kg,
    hp.Energy_Efficiency_percent,
    hp.Specific_Energy_MJperkg_H2,

    -- Calculated metrics
    CASE
        WHEN eb.TotalEnergyInput_MJ > 0
        THEN (eb.H2Product_HHV_MJ / eb.TotalEnergyInput_MJ) * 100.0
        ELSE NULL
    END AS Calculated_H2_Energy_Efficiency,

    CASE
        WHEN eb.TotalEnergyInput_MJ > 0
        THEN ((eb.H2Product_HHV_MJ + eb.TailGasEnergy_MJ) / eb.TotalEnergyInput_MJ) * 100.0
        ELSE NULL
    END AS Total_Energy_Recovery_percent,

    CASE
        WHEN eb.TotalEnergyInput_MJ > 0
        THEN (eb.HeatLoss_MJ / eb.TotalEnergyInput_MJ) * 100.0
        ELSE NULL
    END AS Heat_Loss_percent

FROM AspenSimulation sim
INNER JOIN EnergyBalance eb ON sim.SimulationId = eb.Simulation_Id
INNER JOIN ReformingConditions rc ON sim.SimulationId = rc.Simulation_Id
INNER JOIN HydrogenProduct hp ON sim.SimulationId = hp.Simulation_Id
INNER JOIN Biooil b ON sim.Biooil_Id = b.BiooilId
LEFT JOIN Experiment e ON b.Experiment_Id = e.ExperimentId
LEFT JOIN Biomass bm ON e.Biomass_Id = bm.BiomassId

WHERE sim.ConvergenceStatus = 'Converged'
  AND sim.ValidationFlag = 1;

GO

PRINT 'vw_EnergyEfficiencyAnalysis view created successfully.';
PRINT '';
GO


-- ==============================================================================
-- VERIFICATION
-- ==============================================================================

PRINT '';
PRINT '==============================================================================';
PRINT 'VIEW CREATION SUMMARY';
PRINT '==============================================================================';

SELECT
    TABLE_NAME AS ViewName,
    TABLE_SCHEMA AS SchemaName
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_NAME IN ('vw_ML_ReversePrediction', 'vw_SimulationSummary',
                     'vw_SyngasStreamComparison', 'vw_EnergyEfficiencyAnalysis')
ORDER BY TABLE_NAME;

PRINT '';
PRINT 'All 4 views created successfully!';
PRINT '';
PRINT 'VIEW DESCRIPTIONS:';
PRINT '  1. vw_ML_ReversePrediction      - Main ML training data (inputs + outputs)';
PRINT '  2. vw_SimulationSummary          - High-level simulation monitoring';
PRINT '  3. vw_SyngasStreamComparison     - Gas composition at process points';
PRINT '  4. vw_EnergyEfficiencyAnalysis   - Energy balance and efficiency metrics';
PRINT '==============================================================================';
GO
