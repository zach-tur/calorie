import os
import textual
import textual_dev
from textual.app import App, ComposeResult
from textual.containers import (
    Container,
    Grid,
    Horizontal,
    HorizontalGroup,
    ScrollableContainer,
    Vertical,
    VerticalGroup,
    VerticalScroll,
)
from textual.screen import Screen
from textual.widgets import (
    Button,
    ContentSwitcher,
    DataTable,
    Footer,
    Header,
    Label,
    Placeholder,
    Rule,
)


import sqlite3
import src.sql_handling as db


class StatusHeader(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("daily status goes here")


class ViewSwitcher(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Horizontal(id="buttons"):
            yield Button("Log", id="daily_log")
            yield Rule(orientation="vertical")
            yield Button("FoodBook", id="foodbook")
            yield Rule(orientation="vertical")
            yield Button("Goals", id="goals")

        with ContentSwitcher(initial="daily_log"):
            with VerticalScroll(id="daily_log"):
                yield Log()
            with VerticalScroll(id="foodbook"):
                yield FoodBook()
            with VerticalScroll(id="goals"):
                yield Goals()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id


class Log(Placeholder):
    def compose(self) -> ComposeResult:
        yield Label("This is the daily log tab")


class FoodBook(Placeholder):
    def compose(self) -> ComposeResult:
        yield Label("This is the Food Book tab")


class Goals(Placeholder):
    def compose(self) -> ComposeResult:
        yield Label("This is the Goals tab")


class QuitScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()


class CalorieApp(App):
    # Textual app to track calories and macronutrients
    CSS_PATH = os.path.join(os.path.abspath("."), "src", "calorie.tcss")

    BINDINGS = [("q", "request_quit", "Quit app")]

    def compose(self) -> ComposeResult:
        # Create child widgets for the app
        yield Header()
        yield Container(StatusHeader(), ViewSwitcher())
        yield Footer()

    def action_request_quit(self) -> None:
        # Quit program with confirmation
        self.push_screen(QuitScreen())


def main():
    print("Hello from calorie!")


if __name__ == "__main__":
    app = CalorieApp()
    db.init_db()
    app.run()
