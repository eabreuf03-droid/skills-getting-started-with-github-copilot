from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_duplicate_rejected():
    # Reset app state between tests to avoid cross-test contamination.
    from src import app as app_module
    app_module.activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_success():
    from src import app as app_module
    app_module.activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.delete("/activities/Chess Club/unregister?email=michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"


def test_unregister_missing_student_returns_404():
    from src import app as app_module
    app_module.activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.delete("/activities/Chess Club/unregister?email=notfound@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
