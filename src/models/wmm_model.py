from pydantic import BaseModel, Field, field_validator

class WMMModel(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    year: float
    dec: float = None
    dip: float = None
    ti: float = None
    bh: float = None
    bx: float = None
    by: float = None
    bz: float = None

    class Config:
        allow_mutation = True

    def __str__(self):
        return f"WMMModel(latitude={self.latitude}, longitude={self.longitude}, altitude={self.altitude}, year={self.year})"

    def __repr__(self):
        return self.__str__()

    @field_validator('dec', 'dip', 'ti', 'bh', 'bx', 'by', 'bz', mode='before', always=True)
    def set_results(cls, v, field):
        if v is None:
            return getattr(cls, field.name, None)
        return v

    def get_results(self):
        return {
            "dec": self.dec,
            "dip": self.dip,
            "ti": self.ti,
            "bh": self.bh,
            "bx": self.bx,
            "by": self.by,
            "bz": self.bz
        }