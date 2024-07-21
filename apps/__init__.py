import os

env = os.environ.get("ENV", "dev")

if env == "dev":
	from dotenv import load_dotenv

	load_dotenv(".env.local")


db_user_name = os.environ.get("DB_USER_NAME", "postgres")
db_name = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST", "localhost")
# To be able to change the entire connection str
# when we want to use the mock db for tests
db_connection_str = os.environ.get(
	"CONNECTION_STR",
	f"postgresql://{db_user_name}@{db_host}/{db_name}",
)
