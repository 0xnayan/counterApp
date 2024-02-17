import pyteal as pt

from beaker import (
    Application,
    Authorize,
    GlobalStateValue,
    localnet,
)
from pathlib import Path


class CounterState:
    counter = GlobalStateValue(
        stack_type=pt.TealType.uint64,
        descr="A counter for showing how to use application state",
    )


counter_app = Application("CounterApp", state=CounterState())


@counter_app.external
def increment(*, output: pt.abi.Uint64) -> pt.Expr:
    """increment the counter"""
    return pt.Seq(
        counter_app.state.counter.set(counter_app.state.counter + pt.Int(1)),
        output.set(counter_app.state.counter),
    )


@counter_app.external
def decrement(*, output: pt.abi.Uint64) -> pt.Expr:
    """decrement the counter"""
    return pt.Seq(
        counter_app.state.counter.set(counter_app.state.counter - pt.Int(1)),
        output.set(counter_app.state.counter),
    )

if __name__ == "__main__":
    counter_app.build().export(
        Path(__file__).resolve().parent / f"./artifacts/{counter_app.name}"
    )
