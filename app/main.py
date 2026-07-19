from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="CampusResolve API",
    description="API for managing campus IT support tickets.",
    version="0.1.0",
)


class TicketCreate(BaseModel):
    """Information required when a user submits a ticket."""

    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    category: str
    location: str | None = None


tickets: list[dict] = []


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "CampusResolve API is running"}


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