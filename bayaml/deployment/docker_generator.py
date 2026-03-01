def generate_dockerfile() -> str:
    return "FROM python:3.11-slim\nCMD [\"python\", \"-m\", \"baya\"]\n"
