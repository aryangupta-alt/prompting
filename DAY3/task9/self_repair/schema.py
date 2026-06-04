from pydantic import (
    BaseModel,
    EmailStr,
    Field
)
from typing import Annotated


class Address(BaseModel):

    city: str

    pincode: Annotated[
        str,
        Field(
            pattern=r"^\d{6}$",
            description="6 digit Indian pincode"
        )
    ]


class ContactCard(BaseModel):

    name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=100
        )
    ]

    email: EmailStr

    phone: Annotated[
        str,
        Field(
            pattern=r"^\d{10}$",
            description="10 digit phone number"
        )
    ]

    address: Address