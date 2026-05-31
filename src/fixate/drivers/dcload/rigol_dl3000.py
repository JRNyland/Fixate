from dataclasses import dataclass

from fixate.drivers.dcload.helper import DCLoad


@dataclass(frozen=True)
class Identity:
    manufacturer: str
    model: str
    serial_number: str
    firmware_version: str


class RigolDL3000(DCLoad):
    # I think this is the model number? idk
    REGEX_ID = r"RIGOL.DL3021"
    INSTR_TYPE = "VISA"
    write_termination = "\n"
    read_termination = "\n"

    def __init__(self, instrument):
        super().__init__(instrument)
        self.instrument.timeout = 1000
        self.instrument.read_termination = self.read_termination
        self.instrument.write_termination = self.write_termination
        # 1000ms is what the siglent uses, idk what to use here?


    # === ESR ======================================================
    # Queries the event status register of the standard event status register
    # (i dont understand this at all, but pdf says it retuns an int)
    
    def esr(self) -> int:
        # return int(self.instrument.query("*ESR?").strip())
        return self.send_query("*ESR?")

    # === IDN ======================================================
    # idn gets the instrument information as 4 values

    # this function splits up the IDN string into its 4 parts
    @staticmethod
    def parse_identity(identity: str) -> Identity:
        parts = [part.strip() for part in identity.strip().split(",")]
        if len(parts) != 4:
            raise ValueError(
                "Expected *IDN? response with 4 comma-separated fields; "
                f"got {len(parts)} field(s): {identity!r}"
            )
        return Identity(*parts)

    # the actual function to call IDN from the machine
    def idn(self) -> str:
        # this seems to be how the other VISA devices were calling the functions
        # .strip() removes the whitespaces and useless characters
        # return self.instrument.query("*IDN?").strip()
        return self.send_query("*IDN?")

    # seems like the DriverProtocol (declared in the root __init) wants every driver to have get_identity
    # so this calls idn
    # dont stress this one too much, but leave it in
    def get_identity(self) -> str:
        return self.idn()
    
    def send_query(self, query: str) -> str:
        return self.instrument.query(query).strip()

    def get_ocr(self) -> int:
        return int(self.send_query("*OCR?"))

