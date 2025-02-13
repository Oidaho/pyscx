import os
from dotenv import load_dotenv

from pyscx import Server, API
from pyscx.token import Token, TokenType


load_dotenv()

user_token = Token(
    value=os.getenv("DEMO_USER_ACCESS_TOKEN"),
    type=TokenType.USER,
)


api = API(server=Server.DEMO, tokens=user_token)

# You can redefine the token that will be passed to the method
clan_list = api.friends(region="EU").get_all(token="other_user_token")

# In other words, you can create an API object without explicitly passing tokens to it, and pass them only in methods.
# This is useful if you use multiple tokens of the same type. In particular, tokens of the TokenType.USER type.
