from pprint import pprint
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QGridLayout, QPushButton, QLabel, QWidget, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon
import yaml


class Event:
    description = ""
    trigger = ""
    result = None
    requirement = None
    complete = False
    image = None
    locations = []

    def __init__(self, description, trigger, result=None, requirement=None, image=None, locations=[]):
        self.description = description
        self.trigger = trigger
        self.result = result
        self.requirement = requirement
        self.image = image
        self.locations = locations


class Chain:
    events = []
    result = None
    requirement = None
    complete = False
    active = True

    def __init__(self, result, events, requirement=None):
        self.result = result
        self.events = events
        self.requirement = requirement

    def check_complete(self):
        for event in self.events:
            if event.complete == False:
                return False

        self.complete = True
        return True

    def current(self):
        for event in self.events:
            if event.complete == False:
                return event

    def __repr__(self):
        return f"{self.result} chain:\n\t" + (f"requirement={self.requirement}\n\t" if self.requirement else "") + f"active={self.active}\n\tcomplete={self.complete}\n\tevents={len(self.events)}"

def setup_chains(yaml_file="chains.yml"):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    chains_dict = {}
    for chain_data in data["chains"]:
        chain = Chain(
            chain_data["result"],
            [
                Event(
                    event.get("description"),
                    event.get("trigger"),
                    requirement=event.get("requirement"),
                    result=event.get("result"),
                    image=event.get("image"),
                    locations=([location for location in event.get("location")] if event.get("location") else [])
                )
                for event in chain_data["events"]
            ],
            requirement=chain_data.get("requirement"),
        )
        chains_dict[chain.result] = chain

    return chains_dict


def available_chains(chains, requirements):
    chains_available = {}
    for key, chain in chains.items():
        if chain.requirement and chain.requirement not in requirements:
            continue
        chains_available[key] = chain

    return chains_available


EMOJI_MAP = {
    "Card Box": "🃏",
    "Umbrella": "☔",
    "Sun": "☀️",
    "Mirror": "🪞",
    "Coffee": "☕",
    "Toy Car": "🚗",
    "Artichoke": "🥬",
    "Paper Doll": "🎎",
    "Sitar": "🎸",
    "Sundial": "⏱️",
    "Cigarettes": "🚬",
    "PC": "💻",
    "Floppy Disk": "💾",
    "Gumballs": "🍬",
    "Gold Rose": "🌹",
    "8 Ball": "🎱",
    "Odd Figurine": "🪆",
    "Intestines": "🫀",
    "Hand Drill": "🪚",
}


class ProgressTracker(QMainWindow):
    def __init__(self, chains, requirements):
        super().__init__()
        self.chains = chains
        self.requirements = requirements
        self.initUI()

    def initUI(self):
        self.setWindowTitle("DST Progress Tracker")
        self.setWindowIcon(QIcon("img/icon.png"))
        self.setGeometry(100, 100, 900, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setSpacing(10)

        self.chain_widgets = {}
        self.updateUI()

    def updateUI(self):
        row, col = 0, 0
        for chain_key, chain in self.chains.items():
            if chain_key not in self.chain_widgets:
                chain_label = QLabel()
                chain_label.setFont(QFont("sans-serif", 14))
                chain_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                chain_button = QPushButton()
                chain_button.setFixedSize(280, 60)
                chain_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                chain_button.clicked.connect(lambda _, key=chain_key: self.handle_click(key))

                image_label = QLabel()
                image_label.setScaledContents(True)
                image_label.setFixedSize(80, 80)
                image_label.setSizePolicy(
                    QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
                )

                undo_button = QPushButton("↩️")
                undo_button.setFixedSize(40, 40)
                undo_button.clicked.connect(lambda _, key=chain_key: self.undo_event(key))

                self.layout.addWidget(chain_label, row, col, 1, 1)
                self.layout.addWidget(chain_button, row, col + 1, 1, 1)
                self.layout.addWidget(image_label, row, col + 2, 1, 1)
                self.layout.addWidget(undo_button, row, col + 3, 1, 1)

                self.chain_widgets[chain_key] = (chain_label, chain_button, image_label, undo_button)

                col += 4
                if col >= 8:  # Move to the next row after 2 chains (4 columns per chain group)
                    col = 0
                    row += 1

            chain_label, chain_button, image_label, undo_button = self.chain_widgets[chain_key]
            self.update_chain_widget(chain_key, chain, chain_label, chain_button, image_label, undo_button)

    def update_chain_widget(self, chain_key, chain, chain_label, chain_button, image_label, undo_button):
        emoji = EMOJI_MAP.get(chain.result, "")
        chain_label.setText(f"{emoji} {chain.result}")

        current_event = chain.current()
        if not chain.active:
            chain_button.setDisabled(True)
            chain_button.setText("Inactive")
            image_label.clear()
            return

        if current_event and current_event.requirement and current_event.requirement not in self.requirements:
            chain_button.setDisabled(True)
            chain_button.setStyleSheet("color: red;")
            chain_button.setText(f"Requires: {current_event.requirement}")
            image_label.clear()
            return

        if chain.requirement and chain.requirement not in self.requirements:
            chain_button.setDisabled(True)
            chain_button.setStyleSheet("color: red;")
            chain_button.setText(f"Requires: {chain.requirement}")
            undo_button.setDisabled(True)
            image_label.clear()
            return

        undo_button.setDisabled(False)

        if chain.complete:
            chain_button.setDisabled(True)
            chain_button.setStyleSheet("border: 2px solid green;")
            chain_button.setText("Chain Complete!")
            image_label.clear()
        else:
            chain_button.setDisabled(False)
            chain_button.setStyleSheet("")
            if current_event:
                chain_button.setText(f"{current_event.trigger}" + (f"\nLocation: {', '.join(map(str, current_event.locations))}" if len(current_event.locations) > 0 else "") + f"\n{current_event.description}")
                if current_event.image:
                    pixmap = QPixmap(current_event.image)
                    image_label.setPixmap(pixmap)

    def handle_click(self, chain_key):
        chain = self.chains[chain_key]
        current_event = chain.current()

        if current_event:
            current_event.complete = True
            self.requirements.append(current_event.result)
            chain.check_complete()
            if chain.complete and chain.result not in self.requirements:
                self.requirements.append(chain.result)

        self.updateUI()

    def undo_event(self, chain_key):
        chain = self.chains[chain_key]
        for event in reversed(chain.events):
            if event.complete:
                event.complete = False
                if event.result:
                    self.requirements.remove(event.result)
                break

        chain.complete = False
        if chain.result in self.requirements:
            self.requirements.remove(chain.result)

        self.updateUI()


def main():
    from sys import argv, exit
    app = QApplication(argv)

    chains = setup_chains()
    requirements = []
    tracker = ProgressTracker(chains, requirements)
    tracker.show()

    exit(app.exec())


if __name__ == "__main__":
    main()
