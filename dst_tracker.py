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


def setup_chains_old():
    card_chain = Chain()
    card_chain.result = "Card Box"
    card_chain.events = [
        Event("Get Card Box", "Talk to Card Man [Grey Chamber, Naraka]", image="img/card_man.png")
    ]

    umbrella_chain = Chain()
    umbrella_chain.result = "Umbrella"
    umbrella_chain.events = [
        Event("Rainy city scene", "Purple Faces Door #1 [Naraka]", image="img/purple_face_door.png"),
    ]

    sun_chain = Chain()
    sun_chain.result = "Sun"
    sun_chain.requirement = "Umbrella"
    sun_chain.events = [
        Event("Recieve the sun", "Talk to The Sun [Naraka]", "Unlock Nyanko", image="img/sun.png")
    ]

    mirror_chain = Chain()
    mirror_chain.result = "Mirror"
    mirror_chain.events = [
        Event("Chromed Fellow encounter", "Talk to Viator [Naraka]", image="img/viator.png")
    ]

    coffee_chain = Chain()
    coffee_chain.result = "Coffee"
    coffee_chain.events = [
        Event("Coffee talk 1", "Talk to Dementia [Naraka]", image="img/dementia.png"),
        Event("Coffee talk 2", "Talk to Dementia [Naraka]", image="img/dementia.png"),
        Event("Coffee talk 3", "Talk to Dementia [Naraka]", image="img/dementia.png")
    ]

    toy_car_chain = Chain()
    toy_car_chain.result = "Toy Car"
    toy_car_chain.events = [
        Event("Meet Amelia", "Talk to Amelia [Naraka]", image="img/amelia.png"),
        Event("Help Amelia", "Talk to Amelia [Naraka]", image="img/amelia.png"),
        Event("Toshi's office event", "Talk to Lyssa [Angelic, Naraka]", image="img/lyssa.png"),
        Event("Toshi's family event", "Talk to Toshi [Naraka]", image="img/toshi.png")
    ]

    artichoke_chain = Chain()
    artichoke_chain.result = "Artichoke"
    artichoke_chain.events = [
        Event("Esme talk 1", "Talk to Esme [Vicsine, Naraka]", image="img/esme.png"),
        Event("Esme talk 2", "Talk to Esme [Vicsine, Naraka]", image="img/esme.png"),
        Event("Encourage Meri 1", "Talk to Meri [Vicsine, Naraka]", image="img/meri.png"),
        Event("Encourage Meri 2", "Talk to Meri [Vicsine, Naraka]", image="img/meri.png"),
        Event("Esme talk 3", "Talk to Esme [Vicsine, Naraka]", image="img/esme.png"),
        Event("Last Meri talk", "Talk to Meri [Vicsine, Naraka]", image="img/meri.png")
    ]

    artichoke_alt_chain = Chain()
    artichoke_alt_chain.result = "Artichoke"
    artichoke_alt_chain.evnets = [
        Event("Ayumu talk 1", "Talk to Ayumu [Naraka]", image="img/ayumu.png"),
        Event("Ayumu talk 2", "Talk to Ayumu [Naraka]", image="img/ayumu.png"),
        Event("Ayumu escalator", "Talk to Grey Peep [Naraka]", image="img/grey_peep.png"),
        Event("Last Ayumu talk", "Talk to Ayumu [Naraka]", image="img/ayumu.png")
    ]

    paper_doll_chain = Chain()
    paper_doll_chain.result = "Paper Doll"
    paper_doll_chain.events = [
        Event("Meetup with Chiyo 1", "Talk to Ori [Vicsine, Naraka]", image="img/ori.png"),
        Event("Meetup with Chiyo 2", "Talk to Ori [Vicsine, Naraka]", image="img/ori.png"),
        Event("Meetup with Chiyo 3", "Talk to Ori [Vicsine, Naraka]", image="img/ori.png"),
        Event("Talk with Chiyo 1", "Talk to Chiyo [Vicsine, Naraka]", image="img/chiyo.png"),
        Event("Talk with Chiyo 2", "Talk to Chiyo [Vicsine, Naraka]", image="img/chiyo.png"),
        Event("Ori dies :(", "Talk to Ori [Vicsine, Naraka]", image="img/ori.png")
    ]

    sitar_chain = Chain()
    sitar_chain.result = "Sitar"
    sitar_chain.events = [
        Event("Talk with Cat 1", "Talk to Bakeneko [Vicsine, Naraka]", image="img/bakeneko_hat.png"),
        Event("Talk with Cat 2", "Talk to Bakeneko [Vicsine, Naraka]", image="img/bakeneko_hat.png"),
        Event("Jomon scene", "Talk to Jomon [Naraka]", image="img/jomon.png"),
        Event("Jomon cards", "Talk to Jomon [Naraka]", image="img/jomon.png"),
        Event("Talk with Cat 3", "Talk to Bakeneko [Vicsine, Naraka]", image="img/bakeneko.png"),
        Event("Talk with Cat 4", "Talk to Bakeneko [Vicsine, Naraka]", image="img/bakeneko.png"),
        Event("Talk with Cat 5", "Talk to Bakeneko [Vicsine, Naraka]", image="img/bakeneko.png"),
        Event("Talk with Cat 6", "Talk to Bakeneko [Vicsine, Naraka]", image="img/bakeneko.png"),
    ]

    sundial_chain = Chain()
    sundial_chain.result = "Sundial"
    sundial_chain.events = [
        Event("Mel sleeping 1", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Mel sleeping 2", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Mel sleeping 3", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Mel sleeping 4", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Mel sleeping 5", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Spyglass event 1", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Spyglass event 2", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Spyglass event 3", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Spyglass event 4", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Spyglass event 5", "Grey Faces Door [Angelic, Narka]", requirement="Sitar", image="img/grey_face_door.png"),
        Event("Spyglass event 6", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png"),
        Event("Spyglass event 7", "Grey Faces Door [Angelic, Narka]", image="img/grey_face_door.png")
    ]

    cigarettes_chain = Chain()
    cigarettes_chain.result = "Cigarettes"
    cigarettes_chain.events = [
        Event("Jester talk", "Talk to Jester [Naraka]", image="img/jester.png"),
        Event("Train ride and city with Mel", "Talk to Jester [Subway]", image="img/jester.png"),
        Event("Prison break with Mel", "Talk to Rat [Subway]", image="img/rat.png"),
    ]

    pc_chain = Chain()
    pc_chain.result = "PC"
    pc_chain.events = [
        Event("Gomi talk 1", "Talk to Gomi [Vicsine, Naraka]", image="img/gomi.png"),
        Event("Gomi talk 2", "Talk to Gomi [Vicsine, Naraka]", image="img/gomi.png"),
        Event("Help Gomi find key", "Talk to Gomi [Vicsine, Naraka]", image="img/gomi.png"),
        Event("Get Apartment Key", "Talk to Yakui [Naraka]", result="Apartment Key", requirement="Cigarettes", image="img/yakui.png"),
        Event("Gomi's room tour", "Talk to Gomi [Vicsine, Naraka]", image="img/gomi.png")
    ]

    floppy_chain = Chain()
    floppy_chain.result = "Floppy Disk"
    floppy_chain.events = [
        Event("Vicsine talk 1", "Talk to Vicsine [Grey Chamber, Naraka]", image="img/vicsine.png"),
        Event("Vicsine talk 2", "Talk to Vicsine [Grey Chamber, Naraka]", image="img/vicsine.png"),
        Event("Help with virus", "Talk to Vicsine [Grey Chamber, Naraka]", image="img/vicsine.png"),
        Event("Konpy interaction", "Talk to Konpy [Naraka]", image="img/konpy.png"),
        Event("Get rid of Konpy", "Talk to Konpy [Naraka]", requirement="PC", image="img/konpy"),
        Event("Vicsine is thankful", "Talk to Vicsine [Grey Chamber, Naraka]", image="img/vicsine.png"),
    ]

    gumballs_chain = Chain()
    gumballs_chain.result = "Gumballs"
    gumballs_chain.events = [
        Event("Taidana talk 1", "Talk to Taidana [Vicsine, Naraka]", image="img/taidana.png"),
        Event("Taidana card duel", "Talk to Taidana [Vicsine, Naraka]", requirement="Card Box", image="img/taidana.png"),
        Event("Taidana talk 3", "Talk to Taidana [Vicsine, Naraka]", image="img/taidana.png"),
        Event("Taidana talk 4 with Ayumu", "Talk to Taidana [Vicsine, Naraka]", image="img/taidana.png"),
        Event("Taidana talk 5 with Mel", "Talk to Taidana [Vicsine, Naraka]", requirement="Umbrella", image="img/taidana.png"),
        Event("Taidana talk 5 with Gomi", "Talk to Taidana [Vicsine, Naraka]", requirement="Apartment Key", image="img/taidana.png"),
    ]

    gold_rose_chain = Chain()
    gold_rose_chain.result = "Gold Rose"
    gold_rose_chain.events = [
        Event("Himiko introduction", "Talk to Himiko [Vicsine, Naraka]", image="img/himiko.png"),
        Event("Himiko brings you home", "Talk to Himiko [Vicsine, Naraka]", image="img/himiko.png"),
        Event("Himiko and Mel interaction", "Talk to Himiko [Vicsine, Naraka]", image="img/himiko.png"),
        Event("Himiko city scene", "Talk to Taidana [Subway]", image="img/taidana.png"),
        Event("Himiko premonitions talk", "Talk to Himiko [Vicsine, Naraka]", image="img/himiko.png"),
        Event("Lilum event", "Mel's Grey Door [Angelic, Naraka]", image="img/mel_grey_door.png"),
        Event("Himiko dies :(", "Mel's Grey Door [Angelic, Naraka]", image="img/mel_grey_door.png"),
        Event("Lilum talk 1", "Talk to Lilum [Rusted, Naraka]", image="img/lilum.png"),
        Event("Saren talk", "Talk to Saren [Naraka]", image="img/saren.png"),
        Event("Obtain Gold Rose", "Asphodel Door [Angelic, Naraka]", image="img/asphodel_door.png"),
    ]

    eight_ball_chain = Chain()
    eight_ball_chain.result = "8 Ball"
    eight_ball_chain.requirement = "Gold Rose"
    eight_ball_chain.events = [
        Event("Lilum talk 1", "Talk to Lilum [Rusted, Naraka]", image="img/lilum.png"),
        Event("Lilum talk 2", "Talk to Lilum [Rusted, Naraka]", image="img/lilum.png", result="Mark of Lilith"),
        Event("Lilith is defeated", "Kill Lilith [Naraka]", image="img/lilith.png"),
        Event("Obtain 8 Ball", "Talk to Lyssa [Angelic, Naraka]", image="img/lyssa.png"),
    ]

    odd_figurine_chain = Chain()
    odd_figurine_chain.result = "Odd Figurine"
    odd_figurine_chain.events = [
        Event("Golden Church event", "Go to Golden Church [Grey Chamber]", image="img/gold_church.jpg"),
        Event("Obtain Odd Figurine", "Go to Golden Church [Grey Chamber]", requirement="Gold Rose", image="img/gold_church.jpg"),
    ]

    intestines_chain = Chain()
    intestines_chain.result = "Intestines"
    intestines_chain.events = [
        Event("Meet Horned Woman", "Rusted Door #1 [Naraka]", result="Rusted Key", image="img/rusted_door.png"),
        Event("Iron Maiden lift", "Rusted Door #2 [Naraka]", image="img/rusted_door.png"),
        Event("Meet Angel of Forgiveness", "Angelic Door #1 [Naraka]", image="img/angelic_door.png"),
        Event("Obtain Intestines", "Rusted Door #3 [Naraka]", image="img/rusted_door.png"),
    ]

    hand_drill_chain = Chain()
    hand_drill_chain.result = "Hand Drill"
    hand_drill_chain.events = [
        Event("Doctor talk 1", "Talk to Doctor [Naraka]", image="img/doctor.png"),
        Event("Doctor talk 2", "Talk to Doctor [Naraka]", image="img/doctor.png"),
        Event("Doctor talk 3", "Talk to Doctor [Naraka]", requirement="Intestines", image="img/doctor.png"),
        Event("Horned Woman scene", "Rusted Door #2 [Naraka]", image="rusted_door.png"),
        Event("Doctor talk 4 with Mel", "Talk to Doctor [Naraka]", image="img/doctor.png"),
        Event("Obtain Hand Drill", "Talk to Doctor [Naraka]", image="img/doctor.png"),
    ]

    return {
        "Card Box": card_chain,
        "Umbrella": umbrella_chain,
        "Sun": sun_chain,
        "Mirror": mirror_chain,
        "Coffee": coffee_chain,
        "Toy Car": toy_car_chain,
        "Artichoke": artichoke_chain,
        "Paper Doll": paper_doll_chain,
        "Sitar": sitar_chain,
        "Sundial": sundial_chain,
        "Cigarettes": cigarettes_chain,
        "PC": pc_chain,
        "Floppy Disk": floppy_chain,
        "Gumballs": gumballs_chain,
        "Gold Rose": gold_rose_chain,
        "8 Ball": eight_ball_chain,
        "Odd Figurine": odd_figurine_chain,
        "Intestines": intestines_chain,
        "Hand Drill": hand_drill_chain,
    }


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
