from dotenv import load_dotenv, find_dotenv

def load_environment_variables():
    load_dotenv(find_dotenv())
    pass