from pydantic import BaseModel, Field
from typing import Optional


class WMMModel(BaseModel):
    """
    World Magnetic Model (WMM) data class.

    This class represents the input parameters and computed results for the World Magnetic Model.

    Attributes:
        latitude (float): Latitude in decimal degrees.
        longitude (float): Longitude in decimal degrees.
        altitude (float): Altitude above the WGS84 ellipsoid in kilometers.
        date (string): Year for the desired magnetic field values.
        dec (Optional[float]): Computed magnetic declination in degrees. Defaults to None.
        dip (Optional[float]): Computed magnetic inclination in degrees. Defaults to None.
        ti (Optional[float]): Computed total intensity of the magnetic field in nanoteslas. Defaults to None.
        bh (Optional[float]): Computed horizontal intensity of the magnetic field in nanoteslas. Defaults to None.
        bx (Optional[float]): Computed north component of the magnetic field in nanoteslas. Defaults to None.
        by (Optional[float]): Computed east component of the magnetic field in nanoteslas. Defaults to None.
        bz (Optional[float]): Computed vertical component of the magnetic field in nanoteslas. Defaults to None.
    """

    latitude: float = Field(..., description="Latitude in decimal degrees.")
    longitude: float = Field(..., description="Longitude in decimal degrees.")
    altitude: float = Field(
        ..., description="Altitude above the WGS84 ellipsoid in kilometers."
    )
    date: str = Field(..., description="Year for the desired magnetic field values.")
    dec: Optional[float] = Field(
        None, description="Computed magnetic declination in degrees."
    )
    dip: Optional[float] = Field(
        None, description="Computed magnetic inclination in degrees."
    )
    ti: Optional[float] = Field(
        None,
        description="Computed total intensity of the magnetic field in nanoteslas.",
    )
    bh: Optional[float] = Field(
        None,
        description="Computed horizontal intensity of the magnetic field in nanoteslas.",
    )
    bx: Optional[float] = Field(
        None,
        description="Computed north component of the magnetic field in nanoteslas.",
    )
    by: Optional[float] = Field(
        None, description="Computed east component of the magnetic field in nanoteslas."
    )
    bz: Optional[float] = Field(
        None,
        description="Computed vertical component of the magnetic field in nanoteslas.",
    )

    def __str__(self):
        return f"WMMModel(latitude={self.latitude}, longitude={self.longitude}, altitude={self.altitude}, date={self.date})"

    def __repr__(self):
        return self.__str__()

    def get_results(self) -> dict:
        """
        Get the computed magnetic field results.

        Returns:
            dict: A dictionary containing the computed magnetic field results.
        """
        return {
            "dec": self.dec,
            "dip": self.dip,
            "ti": self.ti,
            "bh": self.bh,
            "bx": self.bx,
            "by": self.by,
            "bz": self.bz,
        }

    def set_results(
        self,
        dec: float,
        dip: float,
        ti: float,
        bh: float,
        bx: float,
        by: float,
        bz: float,
    ) -> None:
        """
        Set the computed magnetic field results.

        Args:
            dec (float): Computed magnetic declination in degrees.
            dip (float): Computed magnetic inclination in degrees.
            ti (float): Computed total intensity of the magnetic field in nanoteslas.
            bh (float): Computed horizontal intensity of the magnetic field in nanoteslas.
            bx (float): Computed north component of the magnetic field in nanoteslas.
            by (float): Computed east component of the magnetic field in nanoteslas.
            bz (float): Computed vertical component of the magnetic field in nanoteslas.
        """
        self.dec = dec
        self.dip = dip
        self.ti = ti
        self.bh = bh
        self.bx = bx
        self.by = by
        self.bz = bz
