import pyvisa

import fixate.drivers
from fixate.config import find_instrument_by_id
from fixate.drivers import InstrumentNotFoundError, InstrumentOpenError
from fixate.drivers.dcload.helper import DCLoad
from fixate.drivers.dcload.rigol_dl3000 import RigolDL3000


def open() -> DCLoad:
    rigol = find_instrument_by_id(RigolDL3000.REGEX_ID)
    if rigol is not None:
        # We've found a configured instrument so try to open it
        rm = pyvisa.ResourceManager()
        try:
            resource = rm.open_resource(rigol.address)
        except pyvisa.VisaIOError as e:
            raise InstrumentOpenError(
                f"Unable to open DC load: {rigol.address}"
            ) from e
        # Instantiate driver with connected instrument
        driver = RigolDL3000(resource)
        fixate.drivers.log_instrument_open(driver)
        return driver

    raise InstrumentNotFoundError
