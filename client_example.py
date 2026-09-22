"""Cliente Python mínimo para consumir TurnoYa API."""
import httpx

BASE_URL = "http://127.0.0.1:8000/api/v1"


def register_cliente():
    response = httpx.post(
        f"{BASE_URL}/auth/register",
        json={"nombre": "Cliente Demo", "email": "cliente@example.com", "password": "123456", "rol": "cliente"},
    )
    print(response.status_code, response.json())


def login(email: str, password: str) -> str:
    response = httpx.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    response.raise_for_status()
    return response.json()["access_token"]


def buscar_negocios(nombre: str | None = None, categoria: str | None = None):
    response = httpx.get(f"{BASE_URL}/businesses", params={"nombre": nombre, "categoria": categoria})
    response.raise_for_status()
    return response.json()


def solicitar_turno(token: str, negocio_id: int, sector_id: int | None = None, item_id: int | None = None, motivo: str | None = None):
    response = httpx.post(
        f"{BASE_URL}/businesses/{negocio_id}/turns",
        headers={"Authorization": f"Bearer {token}"},
        json={"id_sector": sector_id, "id_item": item_id, "motivo": motivo},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("Negocios disponibles:", buscar_negocios())
