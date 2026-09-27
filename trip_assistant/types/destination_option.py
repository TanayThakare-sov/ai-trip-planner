from pydantic import BaseModel, Field


class DestinationOption(BaseModel):
    city_name: str = Field(description="The name of the proposed city")
    short_description: str = Field(description="A short description of the city and why it is suitable")


class DestinationOptions(BaseModel):
    destinations: list[DestinationOption] = Field(description="List of proposed destinations")
