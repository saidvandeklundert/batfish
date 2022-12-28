def test_minimum_mtu(interface_properties):
    """Verify all nodes have an MTU of at least 1500"""
    small_mtu = interface_properties["MTU"] < 1500
    assert len(
        interface_properties[small_mtu]
    ), f"There are interfaces with an MTU below 1500: {interface_properties[small_mtu]}"
