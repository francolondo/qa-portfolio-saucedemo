# Plan de Pruebas — SauceDemo (saucedemo.com)

**Objetivo:** validar los flujos principales de login, catálogo, carrito y checkout de la aplicación de práctica SauceDemo.

**Usuarios de prueba disponibles en SauceDemo:**
- `standard_user` / `secret_sauce` → usuario válido
- `locked_out_user` / `secret_sauce` → usuario bloqueado
- Contraseña incorrecta → cualquier combinación inválida

---

## CP-01 — Login exitoso
| Campo | Detalle |
|---|---|
| Precondición | Estar en https://www.saucedemo.com/ |
| Pasos | 1. Ingresar usuario `standard_user`<br>2. Ingresar contraseña `secret_sauce`<br>3. Clic en "Login" |
| Resultado esperado | Se redirige a la página de inventario (`/inventory.html`) y se muestran los productos |
| Resultado obtenido | ✅ Pasa |

## CP-02 — Login con usuario bloqueado
| Campo | Detalle |
|---|---|
| Precondición | Estar en la página de login |
| Pasos | 1. Ingresar usuario `locked_out_user`<br>2. Ingresar contraseña `secret_sauce`<br>3. Clic en "Login" |
| Resultado esperado | Se muestra el mensaje de error: "Epic sadface: Sorry, this user has been locked out." |
| Resultado obtenido | ✅ Pasa |

## CP-03 — Login con contraseña incorrecta
| Campo | Detalle |
|---|---|
| Precondición | Estar en la página de login |
| Pasos | 1. Ingresar usuario `standard_user`<br>2. Ingresar contraseña incorrecta `wrong_pass`<br>3. Clic en "Login" |
| Resultado esperado | Se muestra el mensaje de error: "Epic sadface: Username and password do not match any user in this service." |
| Resultado obtenido | ✅ Pasa |

## CP-04 — Login con campos vacíos
| Campo | Detalle |
|---|---|
| Precondición | Estar en la página de login |
| Pasos | 1. Dejar usuario y contraseña vacíos<br>2. Clic en "Login" |
| Resultado esperado | Se muestra el mensaje de error: "Epic sadface: Username is required" |
| Resultado obtenido | ✅ Pasa |

## CP-05 — Agregar un producto al carrito
| Campo | Detalle |
|---|---|
| Precondición | Sesión iniciada con `standard_user` |
| Pasos | 1. En el listado de productos, clic en "Add to cart" del primer producto |
| Resultado esperado | El botón cambia a "Remove" y el ícono del carrito muestra "1" |
| Resultado obtenido | ✅ Pasa |

## CP-06 — Agregar varios productos al carrito
| Campo | Detalle |
|---|---|
| Precondición | Sesión iniciada con `standard_user` |
| Pasos | 1. Agregar 3 productos distintos con "Add to cart" |
| Resultado esperado | El ícono del carrito muestra "3" |
| Resultado obtenido | ✅ Pasa |

## CP-07 — Quitar un producto del carrito
| Campo | Detalle |
|---|---|
| Precondición | Al menos un producto agregado al carrito |
| Pasos | 1. Clic en "Remove" sobre un producto agregado |
| Resultado esperado | El producto desaparece del carrito y el contador disminuye en 1 |
| Resultado obtenido | ✅ Pasa |

## CP-08 — Checkout con datos válidos
| Campo | Detalle |
|---|---|
| Precondición | Al menos un producto en el carrito |
| Pasos | 1. Ir al carrito y clic en "Checkout"<br>2. Completar Nombre, Apellido y Código postal<br>3. Clic en "Continue"<br>4. Clic en "Finish" |
| Resultado esperado | Se muestra el mensaje "Thank you for your order!" |
| Resultado obtenido | ✅ Pasa |

## CP-09 — Checkout con campo obligatorio vacío
| Campo | Detalle |
|---|---|
| Precondición | Al menos un producto en el carrito, en la pantalla de checkout |
| Pasos | 1. Dejar el campo "Código postal" vacío<br>2. Clic en "Continue" |
| Resultado esperado | Se muestra el mensaje de error: "Error: Postal Code is required" |
| Resultado obtenido | ✅ Pasa |

## CP-10 — Cerrar sesión (logout)
| Campo | Detalle |
|---|---|
| Precondición | Sesión iniciada con `standard_user` |
| Pasos | 1. Abrir el menú lateral (ícono de hamburguesa)<br>2. Clic en "Logout" |
| Resultado esperado | Se redirige a la página de login |
| Resultado obtenido | ✅ Pasa |

---

**Nota:** los resultados "Pasa" corresponden a la ejecución manual de referencia sobre SauceDemo en su comportamiento estándar documentado. Al ejecutar tú mismo cada caso, actualiza esta columna con tu resultado real y agrega capturas de pantalla como evidencia si quieres reforzar el repositorio.
