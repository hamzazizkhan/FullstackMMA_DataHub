from sqlmodel import SQLModel, Field

class MMA_record(SQLModel, table=True):
    firstName: str = Field(primary_key=True)
    lastName: str = Field(primary_key=True)
    result: str = Field(primary_key=True)
    record:  str = Field(primary_key=True)
    opponent: str
    method: str
    event: str
    date: str
    round: int
    time: str
    location: str
    notes: str
    fighterID: int = Field(foreign_key='profesional_record_data.fighterID')


class visited_links(SQLModel, table=True):
    firstName: str
    lastName: str
    href: str | None
    html: str | None
    fighterID: int = Field(primary_key=True)


class profesional_record_data(SQLModel, table=True):
    firstName: str
    lastName: str
    matches: int
    wins: int
    losses: int
    knockoutWins: int
    knockoutLosses: int
    submissionWins: int
    submissionLosses: int
    decisionWins: int
    decisionLosses: int
    fighterID: int = Field(primary_key=True)
