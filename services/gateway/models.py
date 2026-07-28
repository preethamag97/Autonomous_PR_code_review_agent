from pydantic_settings import BaseSettings

#when defining webhook secret, make sure to use a strong secret and keep it safe. This secret is used to verify that incoming webhook requests are from GitHub and not from a malicious source.
class Settings(BaseSettings):
    github_webhook_secret: str = ""

    class Config:
        env_file = ".env"
