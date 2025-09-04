import os
from timeit import Timer
import textual
import textual_dev
from textual.app import App, ComposeResult
from textual.color import Gradient
from textual.containers import (
    Center,
    Container,
    Grid,
    Horizontal,
    HorizontalGroup,
    ScrollableContainer,
    Vertical,
    VerticalGroup,
    VerticalScroll,
)
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import (
    Button,
    ContentSwitcher,
    DataTable,
    Footer,
    Header,
    Label,
    Placeholder,
    ProgressBar,
    Rule,
    Static,
)


import sqlite3
import src.sql_handling as db


class StatusBarFat(ProgressBar):
    def compose(self) -> ComposeResult:
        gradient = Gradient.from_colors("yellow", "orange")
        yield ProgressBar(total=100, show_eta=False, gradient=gradient)

    def on_mount(self) -> None:
        self.query_one(ProgressBar).update(progress=30)


class StatusBarCarb(ProgressBar):
    def compose(self) -> ComposeResult:
        gradient = Gradient.from_colors("lightgreen", "darkgreen")
        yield ProgressBar(total=100, show_eta=False, gradient=gradient)

    def on_mount(self) -> None:
        self.query_one(ProgressBar).update(progress=40)


class StatusBarFiber(ProgressBar):
    def compose(self) -> ComposeResult:
        gradient = Gradient.from_colors("tan", "sienna")
        yield ProgressBar(total=100, show_eta=False, gradient=gradient)

    def on_mount(self) -> None:
        self.query_one(ProgressBar).update(progress=50)


class StatusBarProtein(ProgressBar):
    def compose(self) -> ComposeResult:
        gradient = Gradient.from_colors("red", "darkred")
        yield ProgressBar(total=100, show_eta=False, gradient=gradient)

    def on_mount(self) -> None:
        self.query_one(ProgressBar).update(progress=60)


class StatusHeader(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with VerticalGroup(id="status_bar_labels"):
            yield Static("FAT ", id="fat_bar_label")
            yield Static("CARB ", id="carb_bar_label")
            yield Static("FIBER ", id="fiber_bar_label")
            yield Static("PROTEIN ", id="protein_bar_label")
        with VerticalGroup(id="status_bars"):
            yield StatusBarFat(id="bar_fat")
            yield StatusBarCarb(id="bar_carb")
            yield StatusBarFiber(id="bar_fiber")
            yield StatusBarProtein(id="bar_protein")
        with VerticalGroup(id="status_cal_labels"):
            yield Static("Calories Today: ", id="calories_today")
            yield Static("Calories Target: ", id="calories_target")
            yield Static("Leftover: ", id="calories_leftover")
        with VerticalGroup(id="status_cals"):
            yield Static("x,xxx cal", id="today_number")
            yield Static("1,800 cal", id="target_number")
            yield Static("800 cal", id="leftover_number")


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


class Log(Grid):
    def compose(self) -> ComposeResult:
        yield Label("This is the daily log tab", classes="outline border")


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
        with Vertical():
            yield StatusHeader(id="status_header")
            yield ViewSwitcher()
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
