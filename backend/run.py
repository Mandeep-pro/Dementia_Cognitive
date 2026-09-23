from app import create_app
from app.config.database import client


app = create_app()


if __name__ == "__main__":
    try:
        client.admin.command("ping")
        print("MongoDB connected successfully!")
    except Exception as e:
        print("MongoDB connection failed:")
        print(e)

    app.run(debug=True)

    