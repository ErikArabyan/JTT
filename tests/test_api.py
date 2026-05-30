import pytest


pytestmark = pytest.mark.asyncio


async def test_create_and_retrieve_user(client):
    create_response = await client.post(
        "/users",
        json={"name": "Ada Lovelace", "email": "ada@example.com"},
    )

    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user["id"] == 1
    assert created_user["email"] == "ada@example.com"

    get_response = await client.get(f"/users/{created_user['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Ada Lovelace"


async def test_duplicate_email_is_rejected(client):
    payload = {"name": "Grace Hopper", "email": "grace@example.com"}

    assert (await client.post("/users", json=payload)).status_code == 201
    duplicate_response = await client.post("/users", json=payload)

    assert duplicate_response.status_code == 409


async def test_list_users_uses_pagination(client):
    for index in range(3):
        await client.post(
            "/users",
            json={"name": f"User {index}", "email": f"user{index}@example.com"},
        )

    response = await client.get("/users?limit=2&offset=1")

    assert response.status_code == 200
    assert [user["email"] for user in response.json()] == [
        "user1@example.com",
        "user2@example.com",
    ]


async def test_create_project_for_existing_user_and_list_it(client):
    user = (
        await client.post(
            "/users",
            json={"name": "Katherine Johnson", "email": "katherine@example.com"},
        )
    ).json()

    create_project_response = await client.post(
        "/projects",
        json={
            "name": "Trajectory Calculator",
            "description": "Mission support tooling.",
            "owner_id": user["id"],
        },
    )

    assert create_project_response.status_code == 201
    project = create_project_response.json()
    assert project["owner_id"] == user["id"]

    get_project_response = await client.get(f"/projects/{project['id']}")
    user_projects_response = await client.get(f"/users/{user['id']}/projects")

    assert get_project_response.status_code == 200
    assert user_projects_response.status_code == 200
    assert user_projects_response.json()[0]["name"] == "Trajectory Calculator"


async def test_create_project_rejects_unknown_owner(client):
    response = await client.post(
        "/projects",
        json={"name": "No Owner Project", "owner_id": 999},
    )

    assert response.status_code == 404


async def test_openapi_uses_required_url_templates(client):
    response = await client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/users/{id}" in paths
    assert "/users/{id}/projects" in paths
    assert "/projects" in paths
    assert "/projects/{id}" in paths
    assert "post" in paths["/projects"]
    assert "get" in paths["/projects/{id}"]


async def test_deleting_user_removes_owned_projects(client):
    user = (
        await client.post(
            "/users",
            json={"name": "Margaret Hamilton", "email": "margaret@example.com"},
        )
    ).json()
    project = (
        await client.post(
            "/projects",
            json={"name": "Guidance Software", "owner_id": user["id"]},
        )
    ).json()

    delete_response = await client.delete(f"/users/{user['id']}")
    get_project_response = await client.get(f"/projects/{project['id']}")

    assert delete_response.status_code == 204
    assert get_project_response.status_code == 404
