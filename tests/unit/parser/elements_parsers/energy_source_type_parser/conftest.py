import numpy as np
import pandas as pd
import pytest

from pyzefir.parser.elements_parsers.energy_source_type_parser import (
    EnergySourceTypeParser,
)
from tests.unit.defaults import ELECTRICITY, HEATING, default_network_constants


@pytest.fixture
def storage_types_mock() -> pd.DataFrame:
    """storage_types / Parameters.csv mock"""
    return pd.DataFrame(
        columns=[
            "storage_type",
            "load_efficiency",
            "gen_efficiency",
            "cycle_length",
            "power_to_capacity",
            "energy_type",
            "energy_loss",
            "build_time",
            "life_time",
            "power_utilization",
        ],
        data=[
            ["STORAGE_TYPE_1", 0.89, 0.92, 48, 7, HEATING, 0.0, 0, 10, 0.9],
            ["STORAGE_TYPE_2", 0.86, 0.94, 24, 9, ELECTRICITY, 0.0, 0, 10, 0.9],
            ["STORAGE_TYPE_3", 0.82, 0.88, 2190, 10, HEATING, 0.0, 1, 15, 0.9],
        ],
    )


@pytest.fixture
def storage_calculation_settings() -> pd.DataFrame:
    """storage_types / Storage_Calculation_Settings.csv mock"""
    return pd.DataFrame(
        columns=[
            "storage_type",
            "generation_load_method",
        ],
    )


@pytest.fixture
def generator_types_mock() -> pd.DataFrame:
    """generator_types / Generator_Types.csv mock"""
    return pd.DataFrame(
        columns=[
            "name",
            "build_time",
            "life_time",
            "power_utilization",
            "minimal_power_utilization",
            "disable_dump_energy",
        ],
        data=[
            ["GEN_TYPE_1", 0, 20, np.nan, np.nan, True],
            ["GEN_TYPE_2", 1, 30, 0.9, 0.2, True],
            ["GEN_TYPE_3", 0, 15, 0.9, 0.2, True],
        ],
    )


@pytest.fixture
def generator_type_efficiency_series_mock() -> dict[str, pd.DataFrame]:
    """generator_types / generator_type_efficiency.csv mock"""
    return {
        "GEN_TYPE_3": pd.DataFrame(
            {"hour_idx": range(8760), HEATING: [0.84] * 8760},
        )
    }


@pytest.fixture
def generator_type_efficiency_mock() -> pd.DataFrame:
    """generator_types / Efficiency.csv mock"""
    return pd.DataFrame(
        columns=["generator_type", "energy_type", "efficiency"],
        data=[
            ["GEN_TYPE_1", HEATING, 0.3],
            ["GEN_TYPE_1", ELECTRICITY, 0.4],
            ["GEN_TYPE_2", ELECTRICITY, 0.9],
        ],
    )


@pytest.fixture
def emission_reduction_mock() -> pd.DataFrame:
    """generator_types / Emission_Reduction.csv mock"""
    return pd.DataFrame(
        columns=["generator_type", "CO2", "SO2"],
        data=[
            ["GEN_TYPE_1", 0.2, 0.3],
            ["GEN_TYPE_2", 0.3, 0.1],
            ["GEN_TYPE_3", 0.4, 0.25],
        ],
    )


@pytest.fixture
def yearly_emission_reduction_mock() -> pd.DataFrame:
    """scenario / Yearly_Emission_Reduction.csv mock"""
    return pd.DataFrame(
        columns=["year_idx", "emission_type", "GEN_TYPE_3"],
        data=[
            [1, "CO2", 0.5],
            [2, "CO2", 0.5],
            [3, "CO2", 0.6],
        ],
    )


@pytest.fixture
def generator_type_energy_type_mock() -> pd.DataFrame:
    """generator_types / Generator_Type_Energy_Type.csv mock"""
    return pd.DataFrame(
        columns=["generator_type", "energy_type"],
        data=[
            ["GEN_TYPE_1", HEATING],
            ["GEN_TYPE_1", ELECTRICITY],
            ["GEN_TYPE_2", ELECTRICITY],
            ["GEN_TYPE_3", HEATING],
        ],
    )


@pytest.fixture
def energy_curtailment_cost_mock() -> pd.DataFrame:
    """energy curtailemnt cost mock"""
    return pd.DataFrame(
        {
            "year_idx": [0, 1, 2, 3, 4],
            "GEN_TYPE_1": [50] * 5,
            "GEN_TYPE_2": [55] * 5,
            "GEN_TYPE_3": [45] * 5,
        }
    )


@pytest.fixture
def generator_fuel_type_mock() -> pd.DataFrame:
    """generator_types / Generator_Type_Energy_Carrier.csv mock"""
    return pd.DataFrame(
        columns=["generator_type", "fuel_name", "capacity_factor_name"],
        data=[["GEN_TYPE_1", "coal", np.nan], ["GEN_TYPE_2", np.nan, "sun"]],
    )


@pytest.fixture
def cost_parameters_mock() -> pd.DataFrame:
    """scenario_folder / Cost_Parameters.csv mock"""
    return pd.DataFrame(
        columns=["year_idx", "technology_type", "CAPEX", "OPEX"],
        data=[
            [0, "GEN_TYPE_1", 100, 20],
            [1, "GEN_TYPE_1", 90, 18],
            [2, "GEN_TYPE_1", 80, 15],
            [0, "GEN_TYPE_2", 120, 30],
            [1, "GEN_TYPE_2", 100, 25],
            [2, "GEN_TYPE_2", 95, 22],
            [0, "GEN_TYPE_3", 90, 15],
            [1, "GEN_TYPE_3", 88, 14],
            [2, "GEN_TYPE_3", 85, 12],
            [0, "STORAGE_TYPE_1", 200, 10],
            [1, "STORAGE_TYPE_1", 180, 10],
            [2, "STORAGE_TYPE_1", 150, 8],
            [0, "STORAGE_TYPE_2", 160, 20],
            [1, "STORAGE_TYPE_2", 150, 17],
            [2, "STORAGE_TYPE_2", 145, 13],
            [0, "STORAGE_TYPE_3", 200, 10],
            [1, "STORAGE_TYPE_3", 150, 5],
            [2, "STORAGE_TYPE_3", 120, 3],
        ],
    )


@pytest.fixture
def energy_source_evolution_limits_mock() -> pd.DataFrame:
    """scenario_folder / Energy_Source_Evolution_Limits.csv mock"""

    return pd.DataFrame(
        columns=[
            "year_idx",
            "technology_type",
            "max_capacity",
            "min_capacity",
            "max_capacity_increase",
            "min_capacity_increase",
        ],
        data=[
            [0, "GEN_TYPE_1", np.nan, np.nan, np.nan, 3],
            [1, "GEN_TYPE_1", np.nan, np.nan, np.nan, 4],
            [2, "GEN_TYPE_1", np.nan, np.nan, np.nan, 5],
            [0, "GEN_TYPE_2", 1, 1, 2, np.nan],
            [1, "GEN_TYPE_2", 1, 0.5, 2, np.nan],
            [2, "GEN_TYPE_2", 1, 0.25, 2, np.nan],
            [0, "STORAGE_TYPE_1", np.nan, 2, np.nan, np.nan],
            [1, "STORAGE_TYPE_1", np.nan, 2, np.nan, np.nan],
            [2, "STORAGE_TYPE_1", np.nan, 2, np.nan, np.nan],
            [0, "STORAGE_TYPE_2", 1, 1, np.nan, np.nan],
            [1, "STORAGE_TYPE_2", 2, 1, np.nan, np.nan],
            [2, "STORAGE_TYPE_2", 3, 1, np.nan, np.nan],
        ],
    )


@pytest.fixture
def conversion_rate_mock() -> dict[str, pd.DataFrame]:
    return {
        "GEN_TYPE_3": pd.DataFrame(
            columns=["hour_idx", ELECTRICITY],
            data=[[hour_idx, 1.0] for hour_idx in range(8760)],
        )
    }


@pytest.fixture
def generators_power_utilization() -> pd.DataFrame:
    return pd.DataFrame(
        columns=["hour_idx", "GEN_TYPE_1"],
        data=[[hour_idx, 0.9] for hour_idx in range(8760)],
    )


@pytest.fixture
def minimal_generators_power_utilization() -> pd.DataFrame:
    return pd.DataFrame(
        columns=["hour_idx", "GEN_TYPE_1"],
        data=[[hour_idx, 0.2] for hour_idx in range(8760)],
    )


@pytest.fixture
def generation_compensation() -> pd.DataFrame:
    return pd.DataFrame(
        columns=["hour_idx", "GEN_TYPE_1", "GEN_TYPE_2", "GEN_TYPE_3"],
        data=[
            [0, -3.1, 0.1, 10.1],
            [1, 0, -0.1, 1.1],
            [2, 1.3, 0.8, 2.6],
        ],
    )


@pytest.fixture
def energy_source_type_parser(
    storage_types_mock: pd.DataFrame,
    generator_types_mock: pd.DataFrame,
    generator_type_efficiency_mock: pd.DataFrame,
    emission_reduction_mock: pd.DataFrame,
    generator_type_energy_type_mock: pd.DataFrame,
    generator_fuel_type_mock: pd.DataFrame,
    conversion_rate_mock: dict[str, pd.DataFrame],
    cost_parameters_mock: pd.DataFrame,
    energy_source_evolution_limits_mock: pd.DataFrame,
    energy_curtailment_cost_mock: pd.DataFrame,
    generators_power_utilization: pd.DataFrame,
    generator_type_efficiency_series_mock: dict[str, pd.DataFrame],
    generation_compensation: pd.DataFrame,
    yearly_emission_reduction_mock: pd.DataFrame,
    minimal_generators_power_utilization: pd.DataFrame,
    storage_calculation_settings: pd.DataFrame,
) -> EnergySourceTypeParser:
    return EnergySourceTypeParser(
        cost_parameters_df=cost_parameters_mock,
        storage_type_df=storage_types_mock,
        generators_type=generator_types_mock,
        energy_mix_evolution_limits_df=energy_source_evolution_limits_mock,
        conversion_rate=conversion_rate_mock,
        generators_efficiency=generator_type_efficiency_mock,
        generators_emission_reduction=emission_reduction_mock,
        generators_energy_type=generator_type_energy_type_mock,
        generators_fuel_type=generator_fuel_type_mock,
        generators_power_utilization=generators_power_utilization,
        n_years=default_network_constants.n_years,
        n_hours=default_network_constants.n_hours,
        curtailment_cost=energy_curtailment_cost_mock,
        generators_series_efficiency=generator_type_efficiency_series_mock,
        generation_compensation=generation_compensation,
        yearly_emission_reduction=yearly_emission_reduction_mock,
        generators_minimal_power_utilization=minimal_generators_power_utilization,
        storage_calculation_settings=storage_calculation_settings,
    )
