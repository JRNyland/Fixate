from unittest.mock import MagicMock

import pytest

from fixate.config import load_config
from fixate.drivers.dcload.rigol_dl3000 import Identity, RigolDL3000

load_config()


# non-hardware test, tests if parsing the IDN string is working
def test_parse_identity_returns_four_fields():
    identity = RigolDL3000.parse_identity(
        "RIGOL TECHNOLOGIES,DL3021,DL3A000000001,00.01.00.00.01"
    )

    assert identity == Identity(
        manufacturer="RIGOL TECHNOLOGIES",
        model="DL3021",
        serial_number="DL3A000000001",
        firmware_version="00.01.00.00.01",
    )


# non-hardware test, tests that parse_identity raises a ValueError if the IDN string doesn't have exactly four fields
def test_parse_identity_rejects_unexpected_format():
    with pytest.raises(ValueError):
        RigolDL3000.parse_identity("RIGOL TECHNOLOGIES,DL3021,missing-field")


def test_get_identity_queries_standard_scpi_idn():
    instrument = MagicMock()
    instrument.query.return_value = (
        "RIGOL TECHNOLOGIES,DL3021,DL3A000000001,00.01.00.00.01\n"
    )

    driver = RigolDL3000(instrument)

    assert driver.get_identity() == "RIGOL TECHNOLOGIES,DL3021,DL3A000000001,00.01.00.00.01"
    instrument.query.assert_called_once_with("*IDN?")


@pytest.mark.drivertest
def test_open_dcload():
    import fixate.drivers.dcload

    dcload = fixate.drivers.dcload.open()
    assert dcload, "Could not open DC load"


@pytest.mark.drivertest
def test_identity_has_four_fields():
    import fixate.drivers.dcload

    dcload = fixate.drivers.dcload.open()
    identity = dcload.get_identity()
    parsed = RigolDL3000.parse_identity(identity)

    assert parsed.manufacturer
    assert parsed.model
    assert parsed.serial_number
    assert parsed.firmware_version
    # Unknown: the exact returned model token may be DL3021, DL3031, or another DL3000 variant.
    # Diagnose failures by logging the raw *IDN? string from the real instrument and then
    # tightening this assertion to the exact model used on the bench.
    assert parsed.model.upper().startswith("DL3")

@pytest.mark.drivertest
def test_identity_query_returns_expected_string():
    import fixate.drivers.dcload

    dcload = fixate.drivers.dcload.open()
    identity = dcload.get_identity()

    assert identity.startswith("RIGOL TECHNOLOGIES,DL3")

@pytest.mark.drivertest
def test_esr_returns_an_int():
    import fixate.drivers.dcload

    dcload = fixate.drivers.dcload.open()
    esr = dcload.esr()

    assert isinstance(esr, int)