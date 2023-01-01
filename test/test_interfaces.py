"""
python -m pytest test/test_interfaces.py 
"""


def test_minimum_mtu(interface_properties):
    """Verify all nodes have an MTU of at least 1500"""
    small_mtu = interface_properties["MTU"] < 1500
    assert len(
        interface_properties[small_mtu]
    ), f"There are interfaces with an MTU below 1500: {interface_properties[small_mtu]}"


def test_for_deviating_mtu(interface_properties):
    """Verify nodes do not have a deviating MTU"""
    mtu_std = interface_properties["MTU"] == 1500
    interfaces_with_deviating_mtu = interface_properties[~mtu_std][["Interface", "MTU"]]
    assert (
        interfaces_with_deviating_mtu.empty
    ), f"deviating interfaces:{interfaces_with_deviating_mtu}"


def test_minimum_mtu_core_routers(interface_properties):
    for _, row in interface_properties.iterrows():
        if "core" in row["Interface"].hostname:
            assert row["MTU"] > 7000


def test_unused_are_shut(interface_properties):
    """
    Verify all interfaces with the 'UNUSED' description
    are administratively shut.
    """
    unused = interface_properties["Description"].str.contains("UNUSED", na=False)
    admin_up = interface_properties["Admin_Up"] == True
    unused_and_up = interface_properties[unused & admin_up]
    assert unused_and_up.empty
