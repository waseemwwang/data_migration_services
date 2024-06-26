import typer
import asyncio
from config import GlobalConfig
from utils.logger import log
from scripts.authorize_user_chatbot import AuthorizeUserChatbot


cli = typer.Typer()


@cli.command()
def authorize_user_chatbot():
    asyncio.run(AuthorizeUserChatbot().run())


@cli.command()
def create_superuser(username: str, email: str):
    """Create a superuser."""
    # Here you would add the logic to create a superuser
    print(f"Superuser {username} with email {email} created!")


if __name__ == "__main__":
    cli()
