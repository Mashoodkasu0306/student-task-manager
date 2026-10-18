import app as app_module

client = app_module.app.test_client()


def test_get_tasks_returns_list():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_complete_delete_task():
    created = client.post("/api/tasks", json={"title": "Finish DevOps lab"})
    assert created.status_code == 201
    task_id = created.get_json()["id"]

    done = client.put(f"/api/tasks/{task_id}")
    assert done.get_json()["completed"] is True

    assert client.delete(f"/api/tasks/{task_id}").status_code == 200
    assert all(t["id"] != task_id for t in client.get("/api/tasks").get_json())


def test_empty_title_rejected():
    assert client.post("/api/tasks", json={"title": " "}).status_code == 400


def test_health():
    assert client.get("/health").get_json() == {"status": "ok"}