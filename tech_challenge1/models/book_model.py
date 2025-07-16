from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    price: str
    availability: str
    rating: str
    category: str
    image_url: str