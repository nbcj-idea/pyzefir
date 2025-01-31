import numpy as np
import pytest

from pyzefir.model.network import Network
from tests.unit.optimization.linopy.test_model.utils import (
    create_default_opt_config,
    run_opt_engine,
    set_network_elements_parameters,
)
from tests.unit.optimization.linopy.utils import TOL


@pytest.mark.parametrize(
    ("hour_sample", "energy_loss"),
    [
        (np.arange(50), 0.0),
        (
            np.arange(50),
            0.1,
        ),
        (np.arange(100), 0.05),
    ],
)
def test_state_of_charge(
    hour_sample: np.ndarray,
    energy_loss: float,
    network: Network,
) -> None:
    """
    Test soc eqs
    """
    set_network_elements_parameters(
        network.storage_types,
        {
            "ee_storage_type": {
                "min_capacity": np.array([10, 10, 10, 10, 10]),
                "energy_loss": energy_loss,
            }
        },
    )

    set_network_elements_parameters(
        network.generators,
        {"local_pv": {"unit_base_cap": 15.0}},
    )

    set_network_elements_parameters(
        network.generator_types,
        {
            "pv": {
                "capex": np.array([50, 49, 48, 45, 44]),
                "opex": np.array([50, 49, 48, 45, 44]),
            }
        },
    )
    # Now we dump gen * eff but soc used pure gen so we have to deviate by eff to gen "pure gen"
    storage_generation_eff = 0.85

    opt_config = create_default_opt_config(
        hour_sample, year_sample=np.array([0, 1, 2, 3, 4])
    )
    engine = run_opt_engine(network, opt_config)
    u_idx = engine.indices.STOR.inverse["ee_storage"]
    t_idx = engine.parameters.stor.tstor[u_idx]

    soc, load_netto, gen = (
        engine.results.storages_results.soc["ee_storage"],
        engine.results.storages_results.load["ee_storage"]
        * engine.parameters.stor.load_eff[u_idx],
        engine.results.storages_results.gen["ee_storage"] / storage_generation_eff,
    )
    e_loss = engine.parameters.tstor.energy_loss[t_idx]
    h_last = engine.indices.H.ord[-1]
    for h in engine.indices.H.ord:
        for y in engine.indices.Y.ord:
            if h != 0:
                assert (
                    abs(
                        soc[y][h]
                        - (1 - e_loss) * soc[y][h - 1]
                        + gen[y][h - 1]
                        - load_netto[y][h - 1]
                    )
                    <= TOL
                )
            if y > 0 and h == 0:
                assert (
                    abs(
                        soc[y].loc[h]
                        - (1 - e_loss) * soc[y - 1][h_last]
                        + gen[y - 1][h_last]
                        - load_netto[y - 1][h_last]
                    )
                    <= TOL
                )
