from pydantic import BaseModel


class User1(BaseModel):
    id: int
    name: str
    email: str


def main() -> None:
    data = {
        "id": 1,
        "name": "Laptop",
        "email": "laptop@example.com",
    }

    user = User1.model_validate(data)
    print(user)


if __name__ == "__main__":
    main()
