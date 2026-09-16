"""
Automatización de pruebas UI para SauceDemo (https://www.saucedemo.com/)
con Selenium WebDriver y pytest.

Cubre los casos de prueba CP-01 a CP-10 del plan de pruebas manual
(casos_de_prueba.md).

Requisitos:
    pip install selenium pytest

También necesitas tener instalado el navegador Chrome y su
webdriver correspondiente (Selenium Manager lo resuelve
automáticamente desde Selenium 4.6+).

Cómo correr los tests:
    pytest test_saucedemo.py -v
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"

VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
VALID_PASSWORD = "secret_sauce"
INVALID_PASSWORD = "wrong_pass"


@pytest.fixture
def driver():
    """Inicializa y cierra el navegador para cada test."""
    drv = webdriver.Chrome()
    drv.implicitly_wait(5)
    drv.get(BASE_URL)
    yield drv
    drv.quit()


def login(driver, username, password):
    """Función auxiliar para reutilizar el flujo de login en varios tests."""
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


# ---------- CP-01: Login exitoso ----------
def test_login_exitoso(driver):
    login(driver, VALID_USER, VALID_PASSWORD)
    WebDriverWait(driver, 5).until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"


# ---------- CP-02: Login con usuario bloqueado ----------
def test_login_usuario_bloqueado(driver):
    login(driver, LOCKED_USER, VALID_PASSWORD)
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "locked out" in error.text.lower()


# ---------- CP-03: Login con contraseña incorrecta ----------
def test_login_password_incorrecto(driver):
    login(driver, VALID_USER, INVALID_PASSWORD)
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "do not match" in error.text.lower()


# ---------- CP-04: Login con campos vacíos ----------
def test_login_campos_vacios(driver):
    driver.find_element(By.ID, "login-button").click()
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "username is required" in error.text.lower()


# ---------- CP-05: Agregar un producto al carrito ----------
def test_agregar_un_producto(driver):
    login(driver, VALID_USER, VALID_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1"


# ---------- CP-06: Agregar varios productos al carrito ----------
def test_agregar_varios_productos(driver):
    login(driver, VALID_USER, VALID_PASSWORD)
    botones = driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")
    for boton in botones[:3]:
        boton.click()
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "3"


# ---------- CP-07: Quitar un producto del carrito ----------
def test_quitar_producto(driver):
    login(driver, VALID_USER, VALID_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()
    driver.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()  # ahora dice "Remove"
    badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(badges) == 0


# ---------- CP-08: Checkout con datos válidos ----------
def test_checkout_exitoso(driver):
    login(driver, VALID_USER, VALID_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()

    driver.find_element(By.ID, "first-name").send_keys("Gian Franco")
    driver.find_element(By.ID, "last-name").send_keys("Londoño")
    driver.find_element(By.ID, "postal-code").send_keys("660001")
    driver.find_element(By.ID, "continue").click()

    driver.find_element(By.ID, "finish").click()
    mensaje = driver.find_element(By.CLASS_NAME, "complete-header")
    assert "Thank you for your order" in mensaje.text


# ---------- CP-09: Checkout con campo obligatorio vacío ----------
def test_checkout_campo_vacio(driver):
    login(driver, VALID_USER, VALID_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()

    driver.find_element(By.ID, "first-name").send_keys("Gian Franco")
    driver.find_element(By.ID, "last-name").send_keys("Londoño")
    # postal-code se deja vacío a propósito
    driver.find_element(By.ID, "continue").click()

    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "postal code is required" in error.text.lower()


# ---------- CP-10: Cerrar sesión ----------
def test_logout(driver):
    login(driver, VALID_USER, VALID_PASSWORD)
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    ).click()
    WebDriverWait(driver, 5).until(EC.url_to_be(BASE_URL))
    assert driver.current_url == BASE_URL
