import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="显示版本"),
):
    if version:
        typer.secho("test cli v1.0.0", fg=typer.colors.BRIGHT_RED)
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo("please enter something")
        typer.echo("use '--help' for more information")
    else:
        typer.secho("program started", fg=typer.colors.BRIGHT_BLACK)


@app.command()
def hello(
    name: str = typer.Option(
        "root",
        "--name",
        "-n",
        prompt="enter your name",
        help="your name",
        envvar="USER_NAME",
    ),
    force: bool = typer.Option(False, "--skip-confirm", help="skip confirm"),
):
    if not force and not typer.confirm(f"really hello to{name} ?"):
        typer.echo("canceled")
        raise typer.Abort()
    typer.secho(f"hello {name}", fg=typer.colors.BLUE)


@app.command()
def add(
    a: int = typer.Argument(..., help="第一个加数"),
    b: int = typer.Argument(..., help="第二个加数"),
):
    """计算两个数的和"""
    typer.echo(f"{a} + {b} = {a + b}")


@app.command(name="lowpass_filter")
def lowpass_filter(
    data: float = typer.Argument(..., help="数据"),
    alpha: float = typer.Option(0.5, "--alpha", "-c", help="系数"),
):
    """低通滤波器"""
    filtered_data = data * alpha
    typer.echo(f"Filtered data: {filtered_data}")


if __name__ == "__main__":
    app()
