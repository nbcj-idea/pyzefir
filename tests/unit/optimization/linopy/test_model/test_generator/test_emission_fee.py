import numpy as np
import pandas as pd
import pytest

from pyzefir.model.network import Network
from pyzefir.model.network_elements.emission_fee import EmissionFee
from tests.unit.optimization.linopy.constants import N_YEARS
from tests.unit.optimization.linopy.names import CO2
from tests.unit.optimization.linopy.test_model.utils import (
    create_default_opt_config,
    run_opt_engine,
)


def test_emission_fee_impact_on_optimization(network: Network) -> None:
    hooked_gen_name = "pp_coal_grid"
    opt_config = create_default_opt_config(np.arange(100), np.arange(3))
    base_engine = run_opt_engine(network, opt_config)

    assert base_engine.results.objective_value < 1e7

    em_fee = EmissionFee(
        name="Test_EMF", emission_type=CO2, price=pd.Series([125.21] * N_YEARS)
    )
    network.add_emission_fee(em_fee)
    network.generators[hooked_gen_name].emission_fee = {"Test_EMF"}

    emf_engine = run_opt_engine(network, opt_config)

    assert emf_engine.results.objective_value < 1e7
    assert emf_engine.results.objective_value != base_engine.results.objective_value
    assert base_engine.results.generators_results.gen[hooked_gen_name].equals(
        emf_engine.results.generators_results.gen[hooked_gen_name]
    )
    assert base_engine.results.generators_results.gen_et[hooked_gen_name][
        "electricity"
    ].equals(
        emf_engine.results.generators_results.gen_et[hooked_gen_name]["electricity"]
    )
    assert base_engine.results.generators_results.cap[hooked_gen_name].equals(
        emf_engine.results.generators_results.cap[hooked_gen_name]
    )


def test_emission_fee_with_years_aggregation(network: Network) -> None:
    hooked_gen_name = "pp_coal_grid"
    opt_config = create_default_opt_config(np.arange(100), np.arange(3))
    opt_aggr_config = create_default_opt_config(
        np.arange(100), np.arange(3), year_aggregates=np.array([1, 5, 1])
    )

    base_engine = run_opt_engine(network, opt_config)

    base_aggr_engine = run_opt_engine(network, opt_aggr_config)

    em_fee = EmissionFee(
        name="Test_EMF", emission_type=CO2, price=pd.Series([0, 125.21, 0, 0, 0])
    )
    network.add_emission_fee(em_fee)
    network.generators[hooked_gen_name].emission_fee = {"Test_EMF"}

    emf_engine = run_opt_engine(network, opt_config)

    aggr_emf_engine = run_opt_engine(network, opt_aggr_config)

    assert (
        aggr_emf_engine.results.objective_value
        - base_aggr_engine.results.objective_value
    ) / 5 == pytest.approx(
        emf_engine.results.objective_value - base_engine.results.objective_value
    )
