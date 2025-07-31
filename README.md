# SQLAlchemy CRUD Typer Example

## English

This project is a command-line application for managing items using Python, SQLAlchemy, and Typer. It demonstrates clean architecture and best practices for database access, error handling, and command-line interfaces.

### Features
- **CRUD operations** (Create, Read, Update, Delete) for items
- **Command-line interface** using [Typer](https://typer.tiangolo.com/)
- **SQLite** as the database backend
- **SQLAlchemy ORM** for database interaction
- **Custom exception handling** for robust error management
- **Separation of concerns** with dedicated modules for models, CRUD logic, database connection, and error handling

### Project Structure
- `main.py`: Entry point and CLI commands (create, read, update, delete)
- `models.py`: SQLAlchemy ORM model(s) for the database
- `crud.py`: CRUD logic, decorated with error handling
- `db.py`: Database connection and session management
- `exeption_db_decorator.py`: Decorator for handling database exceptions and rolling back transactions
- `custom_exceptions.py`: Custom exception classes for more descriptive error handling

### Design Patterns Used
- **Repository Pattern**: CRUD functions in `crud.py` abstract database operations, separating persistence logic from business logic.
- **Decorator Pattern**: `handle_db_errors` decorator (in `exeption_db_decorator.py`) wraps CRUD functions to provide automatic exception handling and transaction rollback.
- **Custom Exceptions**: Defined in `custom_exceptions.py` for granular error reporting (e.g., `NotFoundError`, `ConstraintViolation`).
- **Session Management**: Centralized in `db.py` and optionally in `DB_sesion_manager.py` for consistent database access.

### How to Use
1. Install dependencies: `pip install -r requirements.txt`
2. Run commands, e.g.:
   - `python main.py create "Item Name" "Description"`
   - `python main.py read` (list all items)
   - `python main.py read <item_id>` (read one item)
   - `python main.py update <item_id> "New Name" "New Description"`
   - `python main.py delete <item_id>`

---

## Español

Este proyecto es una aplicación de línea de comandos para gestionar elementos usando Python, SQLAlchemy y Typer. Demuestra una arquitectura limpia y buenas prácticas para el acceso a bases de datos, manejo de errores y CLI.

### Características
- **Operaciones CRUD** (Crear, Leer, Actualizar, Eliminar) para elementos
- **Interfaz de línea de comandos** con [Typer](https://typer.tiangolo.com/)
- **SQLite** como base de datos
- **ORM SQLAlchemy** para interacción con la base de datos
- **Manejo de excepciones personalizado** para robustez
- **Separación de responsabilidades** en módulos dedicados para modelos, lógica CRUD, conexión a la base de datos y manejo de errores

### Estructura del Proyecto
- `main.py`: Punto de entrada y comandos CLI (crear, leer, actualizar, eliminar)
- `models.py`: Modelo(s) ORM de SQLAlchemy
- `crud.py`: Lógica CRUD, decorada con manejo de errores
- `db.py`: Conexión y gestión de sesión de la base de datos
- `exeption_db_decorator.py`: Decorador para manejar excepciones y hacer rollback
- `custom_exceptions.py`: Excepciones personalizadas para errores descriptivos

### Patrones de Diseño Utilizados
- **Patrón Repositorio**: Funciones CRUD en `crud.py` abstraen operaciones de base de datos, separando la lógica de persistencia de la lógica de negocio.
- **Patrón Decorador**: El decorador `handle_db_errors` (en `exeption_db_decorator.py`) envuelve funciones CRUD para manejo automático de excepciones y rollback.
- **Excepciones Personalizadas**: Definidas en `custom_exceptions.py` para reportes de error granulares (ej: `NotFoundError`, `ConstraintViolation`).
- **Gestión de Sesión**: Centralizada en `db.py` y opcionalmente en `DB_sesion_manager.py` para acceso consistente.

### Cómo Usar
1. Instala dependencias: `pip install -r requirements.txt`
2. Ejecuta comandos, por ejemplo:
   - `python main.py create "Nombre del Item" "Descripción"`
   - `python main.py read` (listar todos los items)
   - `python main.py read <item_id>` (leer un item)
   - `python main.py update <item_id> "Nuevo Nombre" "Nueva Descripción"`
   - `python main.py delete <item_id>`

---

¡Listo para usar y extender!