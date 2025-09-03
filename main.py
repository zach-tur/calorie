import os
import textual
import textual_dev
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, Grid, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label


import sqlite3
import src.sql_handling as db


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

    BINDINGS = [("q", "request_quit", "Quit app")]

    def compose(self) -> ComposeResult:
        # Create child widgets for the app
        yield Header()
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
