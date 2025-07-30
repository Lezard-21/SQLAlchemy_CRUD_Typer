import typer
from typing_extensions import Annotated
from db import SessionLocal, engine, Base
import crud

app = typer.Typer()

# Create tables
Base.metadata.create_all(bind=engine)


@app.command()
def create(
    name: Annotated[str, typer.Argument()],
    description: Annotated[str, typer.Argument()]
):
    """Create a new item."""
    db = SessionLocal()
    item = crud.create_item(db, name, description)
    db.close()
    print(
        f"created object: name: {item.name}, description: {item.description}")


@app.command()
def read(item_id: Annotated[int, typer.Argument()] = None):
    """Read one or all items."""
    db = SessionLocal()
    if item_id:
        item = crud.get_item(db, item_id)
        print(
            f"created object: name: {item.name}, description: {item.description}")
    else:
        items = crud.get_items(db)
        for item in items:
            print(
                f"created object: id: {item.id}, name: {item.name}, description: {item.description}")
    db.close()


@app.command()
def update(item_id: Annotated[int, typer.Argument()],
           name: Annotated[str, typer.Argument()] = None,
           description: Annotated[str, typer.Argument()] = None):
    """Update an item."""
    db = SessionLocal()
    crud.update_item(db, item_id, name, description)
    db.close()


@app.command()
def delete(item_id: int):
    """Delete an item."""
    db = SessionLocal()
    crud.delete_item(db, item_id)
    db.close()


if __name__ == "__main__":
    app()
