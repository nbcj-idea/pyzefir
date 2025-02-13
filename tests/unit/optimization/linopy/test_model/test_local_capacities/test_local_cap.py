import numpy as np
import pandas as pd
import pytest

from pyzefir.model.network import Network
from pyzefir.optimization.linopy.model import LinopyOptimizationModel
from tests.unit.optimization.linopy.constants import N_YEARS
from tests.unit.optimization.linopy.test_model.utils import (
    create_default_opt_config,
    run_opt_engine,
    set_network_elements_parameters,
)
from tests.unit.optimization.linopy.utils import TOL


@pytest.mark.parametrize(
    ("hour_sample", "year_sample", "life_time", "build_time"),
    [
        (
            np.arange(100),
            np.arange(N_YEARS),
            9,
            0,
        ),
        (
            np.arange(100),
            np.arange(N_YEARS),
            7,
            0,
        ),
    ],
)
def test_local_supplementary_capacity_upper_bound_constraints(
    hour_sample: np.ndarray,
    year_sample: np.ndarray,
    life_time: int,
    build_time: int,
    network: Network,
) -> None:
    """
    Test local capacity evolution constraints
    """

    set_network_elements_parameters(
        network.aggregated_consumers,
        {
            "aggr": {
                "stack_base_fraction": {"lbs": 0.5, "lbs2": 0.5},
                "n_consumers": pd.Series([1000, 1000, 1000, 1000, 1000]),
            },
        },
    )
    set_network_elements_parameters(
        network.generator_types,
        {"local_coal_heat_plant": {"life_time": life_time, "build_time": build_time}},
    ),

    set_network_elements_parameters(
        network.generators,
        {
            "local_coal_heat_plant": {"min_device_nom_power": 24},
            "local_coal_heat_plant2": {"min_device_nom_power": 20},
        },
    )

    # change generators such that will be 2 units of the same type
    set_network_elements_parameters(
        network.generators,
        {"local_coal_heat_plant2": {"energy_source_type": "local_coal_heat_plant"}},
    )

    opt_config = create_default_opt_config(hour_sample, year_sample)
    engine = run_opt_engine(network, opt_config)

    aggr_to_type = engine.indices.aggr_tgen_map
    for aggr_idx, aggr_name in engine.indices.AGGR.mapping.items():
        for t_type in aggr_to_type[aggr_idx]:
            _test_capacity_constraints(engine, aggr_idx, aggr_name, t_type)


def _test_capacity_constraints(
    engine: LinopyOptimizationModel, aggr_idx: int, aggr_name: str, t_type: set[int]
) -> None:
    u_idxs = _u_idxs(
        engine.parameters.gen.tgen,
        t_type,
        engine.indices.aggr_gen_map[aggr_idx],
    )
    lt, bt = (
        engine.parameters.tgen.lt[t_type],
        engine.parameters.tgen.bt[t_type],
    )
    t_name, u_name = (
        engine.indices.TGEN.mapping[t_type],
        engine.indices.GEN.mapping,
    )

    tcap = engine.results.generators_results.tcap[aggr_name][t_name].values.flatten()

    tcap_base_minus = engine.results.generators_results.tcap_base_minus[aggr_name][
        t_name
    ].values.flatten()

    tcap_plus = engine.results.generators_results.tcap_plus[aggr_name][
        t_name
    ].values.flatten()
    tcap_minus = engine.results.generators_results.tcap_minus[aggr_name][t_name].values

    base_cap = sum(engine.parameters.gen.base_cap[u_idx] for u_idx in u_idxs)
    cap = engine.results.generators_results.cap

    sum_cap = sum(cap[u_name[u_idx]] for u_idx in u_idxs).values.flatten()
    assert np.allclose(tcap, sum_cap)

    t_all_cap_minus_sum = tcap_minus.sum(axis=1)
    assert np.all(tcap_plus + TOL >= t_all_cap_minus_sum)

    if aggr_name == "aggr":
        # num values expected for the aggregate aggr:
        assert np.allclose(tcap, np.array([35000, 20000, 20000, 20000, 20000]))
        assert np.allclose(tcap_base_minus, np.array([0, 15000, 0, 0, 0]))
        assert tcap_plus.sum() <= TOL
        assert tcap_minus.sum() <= TOL

    for y in engine.indices.Y.ord:
        initial_cap = (
            base_cap - sum(tcap_base_minus[s] for s in range(1, y + 1)) if y < lt else 0
        )
        incr_cap = sum(tcap_plus[s] for s in _s_range(y, lt, bt))
        decr_cap = sum(
            tcap_minus[s, t]
            for s in _s_range(y, lt, bt)
            for t in _t_range(y, s, lt, bt)
        )
        assert abs(initial_cap + incr_cap - decr_cap - tcap[y]) <= TOL


def _u_idxs(t_gen: dict[int, int], t_type: set[int], unit_in_aggr: set[int]) -> set:
    return {
        u_idx for u_idx, u_type_idx in t_gen.items() if u_type_idx == t_type
    }.intersection(unit_in_aggr)


def _s_range(y: int, lt: int, bt: int) -> range:
    return range(max(0, y - lt - bt + 1), y - bt + 1)


def _t_range(y: int, s: int, lt: int, bt: int) -> range:
    return range(s + bt, min(y, s + bt + lt - 1) + 1)
