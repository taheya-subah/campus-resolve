from pathlib import Path

from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="CampusResolve API",
    description="API for managing campus IT support tickets.",
    version="0.1.0",
)

# Find the main project folder regardless of where the command is run.
BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "static" / "index.html"


class TicketCreate(BaseModel):
    """Information required when a user submits a ticket."""

    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    category: str
    location: str | None = None


tickets: list[dict] = []


@app.get("/", include_in_schema=False)
def show_homepage() -> FileResponse:
    """Display the ticket submission webpage."""
    return FileResponse(INDEX_FILE)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate) -> dict:
    new_ticket = {
        "id": len(tickets) + 1,
        **ticket.model_dump(),
        "status": "open",
        "priority": "medium",
    }

    tickets.append(new_ticket)
    return new_ticket


@app.get("/tickets")
def get_tickets() -> list[dict]:
    return tickets