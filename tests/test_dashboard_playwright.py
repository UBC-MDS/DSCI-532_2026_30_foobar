import subprocess
import time

import pytest


APP_URL = "http://127.0.0.1:8008"


@pytest.fixture(scope="session", autouse=True)
def shiny_app():
    proc = subprocess.Popen(
        ["shiny", "run", "--port", "8008", "src/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(8)
    yield
    proc.terminate()
    proc.wait(timeout=10)


def wait_for_non_empty_text(locator, page, timeout_ms=10000):
    start = time.time()
    while time.time() - start < timeout_ms / 1000:
        text = locator.inner_text().strip()
        if text != "":
            return text
        page.wait_for_timeout(250)
    return locator.inner_text().strip()


def test_dashboard_loads_and_shows_initial_clicked_country(page):
    """This test verifies that the dashboard loads and starts with no clicked-country filter, which is the expected default state."""
    page.goto(APP_URL)
    page.wait_for_load_state("domcontentloaded")

    selected_country = page.locator('[data-testid="selected-country-text"]')
    text = wait_for_non_empty_text(selected_country, page)

    assert text == "Clicked country filter: None"


def test_gender_filter_changes_total_students_tile(page):
    """This test verifies that the gender filter updates KPI values so users can trust the dashboard responds to sidebar filtering."""
    page.goto(APP_URL)
    page.wait_for_load_state("domcontentloaded")

    tile = page.locator('[data-testid="tile-students"]')
    before = wait_for_non_empty_text(tile, page)

    page.get_by_role("radio", name="Male", exact=True).check()
    page.wait_for_timeout(1500)

    after = wait_for_non_empty_text(tile, page)

    assert before != ""
    assert after != ""
    assert before != after


def test_academic_level_filter_changes_total_students_tile(page):
    """This test verifies that an academic-level filter narrows the displayed population so aggregation tiles remain tied to the active subset."""
    page.goto(APP_URL)
    page.wait_for_load_state("domcontentloaded")

    tile = page.locator('[data-testid="tile-students"]')
    before = wait_for_non_empty_text(tile, page)

    page.locator("#f_level").select_option("Graduate")
    page.wait_for_timeout(1500)

    after = wait_for_non_empty_text(tile, page)

    assert before != ""
    assert after != ""
    assert before != after


def test_country_filter_changes_total_students_tile(page):
    """This test verifies that selecting a country updates the dashboard totals because country filtering is central to the map and comparison workflow."""
    page.goto(APP_URL)
    page.wait_for_load_state("domcontentloaded")

    tile = page.locator('[data-testid="tile-students"]')
    before = wait_for_non_empty_text(tile, page)

    country_container = page.locator("#f_country").locator("..")
    country_container.click()
    page.keyboard.type("Canada")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)

    after = wait_for_non_empty_text(tile, page)

    assert before != ""
    assert after != ""
    assert before != after