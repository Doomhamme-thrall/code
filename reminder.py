import time
from tkinter import Tk, messagebox

import typer
from win10toast import ToastNotifier

app = typer.Typer()


@app.command(name="remind_after")
def remind_after(
    mode: str = typer.Option("min", "--mode", "-m"),
    time_value: float = typer.Option(10, "--time", "-t", help="时间值"),
):
    if mode == "min":
        base_time = 60
    elif mode == "hour":
        base_time = 3600
    elif mode == "sec":
        base_time = 1

    time_to_remind = time_value * base_time
    typer.echo(f"Reminder set for {time_value} {mode}")
    time.sleep(time_to_remind)

    # toaster = ToastNotifier()
    # toaster.show_toast(
    #     "Reminder",
    #     f"Time to take a break! {time_value} {mode}(s) have passed.",
    #     duration=10,
    #     threaded=True,
    # )

    root = Tk()
    # root.withdraw()
    messagebox.showinfo(
        "Reminder",
        f"{time_value} {mode} passed",
    )
    root.destroy()


@app.command("remind_every")
def remind_every(
    mode: str = typer.Option("min", "--mode", "-m"),
    time_value: float = typer.Option(10, "--time", "-t"),
):
    while 1:
        remind_after(
            mode=mode,
            time_value=time_value,
        )


if __name__ == "__main__":
    app()
