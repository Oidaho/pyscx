import os
from dotenv import load_dotenv

from pyscx import Server, API
from pyscx.token import Token, TokenType


load_dotenv()

app_token = Token(
    value=os.getenv("DEMO_APP_ACCESS_TOKEN"),
    type=TokenType.APPLICATION,
)
user_token = Token(
    value=os.getenv("DEMO_USER_ACCESS_TOKEN"),
    type=TokenType.USER,
)


user_api = API(server=Server.DEMO, tokens=user_token)
app_api = API(server=Server.DEMO, tokens=app_token)

api = API(server=Server.DEMO, tokens=[user_token, app_token])


# The API automatically searches for keys.
clan_list = user_api.friends(region="EU").get_all()

second_clan_list = api.friends(region="EU").get_all()

# The result of these two requests through 2 different API objects will be the same.

# But this request will raise the MissingTokenError.
# This particular request requires a TokenType.USER type token, which we did not pass.
fail = app_api.friends(region="EU").get_all()
