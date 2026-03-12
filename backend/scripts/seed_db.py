from backend.app.database import SessionLocal
from backend.app.seed import seed_database


def main() -> None:
    with SessionLocal() as session:
        seed_database(session, reset=True)
    print("Seeded synthetic sandbox database.")


if __name__ == "__main__":
    main()
