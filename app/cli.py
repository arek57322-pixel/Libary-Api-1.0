import argparse

from app.database import SessionLocal
from app import models


def set_role(email: str, role: str):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            print(f"User not found: {email}")
            return

        user.role = role
        db.commit()
        print(f"Role updated: {email} -> {role}")

    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Library API CLI")
    subparsers = parser.add_subparsers(dest="command")

    role_parser = subparsers.add_parser("set-role", help="Set user role")
    role_parser.add_argument("--email", required=True, help="User email")
    role_parser.add_argument(
        "--role",
        required=True,
        choices=["admin", "client"],
        help="Role name",
    )

    args = parser.parse_args()

    if args.command == "set-role":
        set_role(args.email, args.role)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
