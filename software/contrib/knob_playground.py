from machine import ADC
from time import sleep

from europi import k1, k2, b1, b2, oled
from europi_script import EuroPiScript
from experimental.knobs import KnobBank

"""
An example program showing the use of a KnobBank or LockableKnobs. This script is not meant to be merged into main, 
it only exists so that PR reviewers can try out a LockableKnob in physical hardware easily.
"""


class KnobPlayground(EuroPiScript):
    def __init__(self):
        super().__init__()
        self.kb1 = (
            KnobBank.builder(k1)
            .with_locked_knob("p1", initial_value=1, threshold=0.02)
            .with_locked_knob("p2", initial_value=1)
            .with_locked_knob("p3", initial_value=1)
            .build()
        )
        self.kb2 = (
            KnobBank.builder(k2)
            .with_disabled_knob()
            .with_locked_knob("p4", initial_value=1, threshold=1 / 7)
            .with_locked_knob("p5", initial_value=1, threshold=1 / 3)
            .build()
        )

        b1.handler(lambda: self.kb1.next())
        b2.handler(lambda: self.kb2.next())

    def main(self):
        choice_p4 = ["a", "b", "c", "d", "e", "f", "g"]
        choice_p5 = ["one", "two", "three"]

        while True:
            p1 = "*" if self.kb1.index == 0 else " "
            p2 = "*" if self.kb1.index == 1 else " "
            p3 = "*" if self.kb1.index == 2 else " "
            pd = "*" if self.kb2.index == 0 else " "
            p4 = "*" if self.kb2.index == 1 else " "
            p5 = "*" if self.kb2.index == 2 else " "
            text = (
                f"{p1} {self.kb1.p1.range(1000):4}  {pd}      \n"
                + f"{p2} {int(round(self.kb1.p2.percent(), 2)*100):3}%  {p4} {self.kb2.p4.choice(choice_p4):5}\n"
                + f"{p3} {self.kb1.p3.read_position():4}  {p5} {self.kb2.p5.choice(choice_p5):5}"
            )
            oled.centre_text(text)


if __name__ == "__main__":
    KnobPlayground().main()
