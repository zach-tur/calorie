import os
from timeit import Timer

from rich import style
from rich.text import Text

import textual
from textual.visual import RichVisual
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
    Input,
    Label,
    Placeholder,
    ProgressBar,
    Rule,
    Static,
)


import sqlite3
import src.sql_handling as db


class StatusBarFat(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield ProgressBar(
            total=100,
            show_eta=False,
            show_percentage=False,
            id="bar_fat",
        )

    def on_mount(self) -> None:
        bar_fat = self.query_one("#bar_fat", ProgressBar)
        bar_fat.update(progress=100)
        bar_fat.styles.min_width = 40


class StatusBarCarb(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield ProgressBar(
            total=100,
            show_eta=False,
            show_percentage=False,
            id="bar_carb",
        )

    def on_mount(self) -> None:
        bar_carb = self.query_one("#bar_carb", ProgressBar)
        bar_carb.update(progress=20)  # Add total carb call here


class StatusBarFiber(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield ProgressBar(
            total=100,
            show_eta=False,
            show_percentage=False,
            id="bar_fiber",
        )

    def on_mount(self) -> None:
        bar_fiber = self.query_one("#bar_fiber", ProgressBar)
        bar_fiber.update(progress=40)  # Add total fiber call here


class StatusBarProtein(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ProgressBar(
                total=100,
                show_eta=False,
                show_percentage=False,
                id="bar_protein",
            )

    def on_mount(self) -> None:
        bar_protein = self.query_one("#bar_protein", ProgressBar)
        bar_protein.update(progress=30)  # Add total protein call here


class StatusHeader(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with VerticalGroup(id="status_bar_labels"):
            yield Static(Text("FAT ", style="bold yellow"), id="fat_bar_label")
            yield Static("CARB ", id="carb_bar_label")
            yield Static("FIBER ", id="fiber_bar_label")
            yield Static("PROTEIN ", id="protein_bar_label")
        with VerticalGroup(id="status_bars"):
            yield StatusBarFat()
            yield StatusBarCarb()
            yield StatusBarFiber()
            yield StatusBarProtein()
        with VerticalGroup(id="status_macros"):
            yield Static("90 g / 100 g", id="macro_fat")
            yield Static("90 g / 100 g", id="macro_carb")
            yield Static("90 g / 100 g", id="macro_fiber")
            yield Static("90 g / 100 g", id="macro_protein")
        with VerticalGroup(id="status_cal_labels"):
            yield Static("Calories Today: ", id="calories_today")
            yield Static("Calories Target: ", id="calories_target")
            yield Static("Leftover: ", id="calories_leftover")
        with VerticalGroup(id="status_cals"):
            yield Static("1,000 cal", id="today_number")
            yield Static("1,800 cal", id="target_number")
            yield Static("800 cal", id="leftover_number")


class StaticSpacer(Container):
    def compose(self) -> ComposeResult:
        yield Static()


class DailyEntry(Vertical):
    def compose(self) -> ComposeResult:
        with Horizontal(id="daily_input_table"):
            with VerticalGroup(id="input_label_item"):
                yield Label(
                    Text("Item", style="bold", justify="right"), id="input_label_item_l"
                )
                yield Input(id="input_item")
            yield StaticSpacer()

            with VerticalGroup(id="input_label_serving"):
                yield Label(
                    Text("Serving", style="bold", justify="center"),
                    id="input_label_serving_l",
                )
                yield Input(id="input_serving")
            yield StaticSpacer()

            with VerticalGroup(id="input_label_cals"):
                yield Label(
                    Text("Cals", style="bold", justify="center"),
                    id="input_label_cals_l",
                )
                yield Input(id="input_cals")
            yield StaticSpacer()

            with VerticalGroup(id="input_label_fat"):
                yield Label(
                    Text("Fat", style="bold yellow", justify="center"),
                    id="input_label_fat_l",
                )
                yield Input(id="input_fat")
            yield StaticSpacer()

            with VerticalGroup(id="input_label_carb"):
                yield Label(
                    Text("Carb", style="bold lime", justify="center"),
                    id="input_label_carb_l",
                )
                yield Input(id="input_carb")
            yield StaticSpacer()

            with VerticalGroup(id="input_label_protein"):
                yield Label(
                    Text("Protein", style="bold red", justify="center"),
                    id="input_label_protein_l",
                )
                yield Input(id="input_protein")
            yield StaticSpacer()

            with VerticalGroup(id="input_label_fiber"):
                yield Label(
                    Text("Fiber", style="bold brown", justify="center"),
                    id="input_label_fiber_l",
                )
                yield Input(id="input_fiber")

        with Horizontal(id="daily_entry_buttons"):
            yield Button("Submit")  # , id="daily_submit_button")
            yield StaticSpacer()
            yield Button("Reset")  # , id="daily_reset_button")


class DailyTable(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column(Text("Item", justify="center"), width=22)
        table.add_column(Text("Serving", justify="center"), width=8)
        table.add_column(Text("Cals", justify="center"), width=8)
        table.add_column(Text("Fat", justify="center"), width=13)
        table.add_column(Text("Carb", justify="center"), width=13)
        table.add_column(Text("Protein", justify="center"), width=13)
        table.add_column(Text("Fiber", justify="center"), width=7)

        ROWS = [
            (
                "test banana",
                "120g",
                "360cal",
                "0g / 0cal",
                "120g / 360cal",
                "0g / 0cal",
                "5g",
            )
        ]
        for row in ROWS:
            styled_row = [Text(str(cell), justify="center") for cell in row]
            table.add_row(*styled_row)


class DailyLog(Container):
    def compose(self) -> ComposeResult:
        yield DailyEntry()
        yield DailyTable()


# class FoodBook(Placeholder):
#    def compose(self) -> ComposeResult:
#        yield Label("This is the Food Book tab")


class Goals(Placeholder):
    def compose(self) -> ComposeResult:
        yield Label("This is the Goals tab")


class ViewSwitcher(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Horizontal(id="buttons"):
            yield Button("Daily Log", id="daily_log")
            yield StaticSpacer()
            #            yield Button("FoodBook", id="foodbook")
            #            yield Rule(orientation="vertical")
            yield Button("Goals", id="goals")
        with ContentSwitcher(initial="daily_log"):
            with Vertical(id="daily_log"):
                yield DailyLog()
            #            with Vertical(id="foodbook"):
            #                yield FoodBook()
            with Vertical(id="goals"):
                yield Goals()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "daily_log" or event.button.id == "goals":
            self.query_one(ContentSwitcher).current = event.button.id


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
        with Vertical(id="main"):
            yield Header()
            with Vertical():
                yield StatusHeader()
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
