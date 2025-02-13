import pytest
from numpy import array

from pyzefir.model.network import NetworkElementsDict
from pyzefir.optimization.linopy.preprocessing.indices import IndexingSet
from pyzefir.optimization.linopy.preprocessing.parameters import ModelParameters
from tests.unit.optimization.linopy.preprocessing.test_optimization_parameters.test_model_parameters.utils import (
    NetworkElementTestImplementation,
)


@pytest.mark.parametrize(
    ("element_names", "connections", "connected_element_names", "expected_result"),
    [
        (
            ["el1", "el2"],
            {"el1": "conn1", "el2": "conn2"},
            ["conn1", "conn5", "conn3", "conn2"],
            {0: 0, 1: 3},
        ),
        (["AA"], {"AA": "BB"}, ["X", "Y", "BB"], {0: 2}),
        (
            ["L1", "L2", "L3"],
            {"L1": "B1", "L2": "B2", "L3": "B3"},
            ["B1", "B2", "B3", "X", "Y"],
            {0: 0, 1: 1, 2: 2},
        ),
    ],
)
def test_get_index_from_prop(
    element_names: list[str],
    connections: dict[str, int],
    connected_element_names: list[str],
    expected_result: dict[int, int],
) -> None:
    element_idx, connected_element_idx = (
        IndexingSet(array(element_names)),
        IndexingSet(array(connected_element_names)),
    )
    network_elements = NetworkElementsDict(
        {
            name: NetworkElementTestImplementation(name=name, scalar_prop=idx)
            for name, idx in connections.items()
        }
    )

    assert (
        ModelParameters.get_index_from_prop(
            network_elements, element_idx, connected_element_idx, "scalar_prop"
        )
        == expected_result
    )
