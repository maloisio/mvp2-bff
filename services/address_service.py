import requests


VIACEP_URL = "https://viacep.com.br/ws"


def get_address_by_cep(cep):
    cep = cep.replace("-", "").replace(".", "").strip()

    if len(cep) != 8 or not cep.isdigit():
        return None

    response = requests.get(
        f"{VIACEP_URL}/{cep}/json/",
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    if data.get("erro"):
        return None

    return data