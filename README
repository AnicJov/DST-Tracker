# Disillusion ST Progress Tracker

<p align="center">
<img src"https://raw.githubusercontent.com/AnicJov/DST-Tracker/main/img/screenshot.png"/>
</p>

Cross-platform tool to track completion progress in the game [Disillusion ST](https://store.steampowered.com/app/2775370/Disillusion_ST/).
Written in Python and PyQt6.

It allows you to track your progress by telling you what you need to do to trigger the next event in each event chain and keeps track of all the requirements for each chain and event. Simply click on the button describing the event once you trigger it in game, and the undo button next to it if you need to go back a step.

**I strongly advise not using this tool on your first playthough of the game**. The game is best enjoyed blind, and I recommend using this tool only after you're very familiar with the story and have gotten all the endings at least once. It can be useful for speedruns or for casual playthroughs when you're really stuck somewhere and you want to avoid that.

## Credits & Legal:
The code for the tracker is written by me ([Anic](https://github.com/AnicJov)) and is licensed under the [GPLv3 software license](https://raw.githubusercontent.com/AnicJov/DST-Tracker/main/LICENSE).

The game Disillusion ST and all of its assets are property of the [Disillusion Dev](https://store.steampowered.com/search/?developer=Disillusion%20Dev) team and are used in this project under explicit permission (they are under the [img/ directory](https://raw.githubusercontent.com/AnicJov/DST-Tracker/main/img)).

Huge thanks to [Altotas](https://steamcommunity.com/id/altotas) for their [Events Compendium guide](https://steamcommunity.com/sharedfiles/filedetails/?id=3359000833) and [Applesgosh](https://www.twitch.tv/applesgosh_) for their progress tracking spreadsheets and continued help and knowledge about the game. Without these two this tracker wouldn't exist and all the credit for the events defined in [`chains.yml`](https://raw.githubusercontent.com/AnicJov/DST-Tracker/main/chains.yml) goes to them.

# Usage
## Running from binary release
1. Download the archive appropriate for your system from the [releases section](https://github.com/AnicJov/DST-Tracker/releases/latest) on this repository.
1. Extract the archive.
1. Run the executable from the extracted folder (`dst_tracker.exe` for Windows, `dst_tracker` for Linux).

## Running from source
If you don't want to run the precompiled binaries and have [Python](https://www.python.org/) installed on your system, follow these instructions to run the script:

### Linux
Prerequisites: git, python

1. Open a terminal
1. Clone the repository and go inside the cloned directory
    ```bash
    git clone https://github.com/AnicJov/DST-Tracker && cd DST-Tracker
    ```
1. Create a Python virtual environment
    ```bash
    python -m venv venv
    ```
1. Install dependencies
    ```bash
    venv/bin/pip install -r requirements.txt
    ```
1. Run the program
    ```bash
    venv/bin/python dst_tracker.py
    ```
### Windows
Prerequisites: [Git](https://git-scm.com/downloads/win), [Python](https://www.python.org/downloads/windows/), [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
1. Open a Powershell window
1. Clone the repository and go inside the cloned directory
    ```ps1
    git clone https://github.com/AnicJov/DST-Tracker && cd DST-Tracker
    ```
1. Create a Python virtual environment and activate it
    ```ps1
    python -m venv venv && .\venv\Scripts\Activate.ps1
    ```
    > Note:
    > It may be required to change the execution policy on your system in order to activate the virtual environment
    >
    > `PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
1. Install dependencies
    ```ps1
    pip install -r requirements.txt
    ```
1. Run the program
    ```ps1
    python dst_tracker.py
    ```

# Modifying the chains and events
If you want to track different chains and events (e.g. for different endings) you can do so by modifying the [`chain.yml`](https://raw.githubusercontent.com/AnicJov/DST-Tracker/main/chains.yml) file.
That is where all the events are defined and loaded on program startup.
The file uses [YAML syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html) and is structured as follows:

At the root is `chains` which is a list of event chains in the game.
```yml
chains:
    - ...
    - ...
    - ...
```
Each chain must have a `result` and at least one event in its `events` list, and can have other optional fields.
```yml
result: "My Chain #1"
requirement: "Some requirement"
events:
    - ...
    - ...
    - ...
```
In the `events` list of a chain individual events are defined. They must have a `description` and `trigger` and **optionally** `location` list, `image`, `requirement`, and `result`.
```yml
description: "Scene where two characters fight"
trigger: "Talk to SomeCharacter"
location: ["Vicsine", "Naraka"]
requirement: "Some item"
result: "Some other item"
image: "img/some_character.png"
```
Putting all of that together, a final `chains.yml` file would look like:
```yml
chains:
  - result: "My Chain #1"
    requirement: "Some requirement"
    events:
      - description: "Scene where two characters fight"
        trigger: "Talk to SomeCharacter"
        location: ["Vicsine", "Naraka"]
        requirement: "Some item"
        result: "Some other item"
        image: "img/some_character.png"
```
Hopefully you get the idea.

# Help & Contributing
If you need any help with anything feel free to reach out to me on Discord at `_anic` or the [DST server](https://discord.gg/a3kcuGygCa).

If you want to contribute to this project feel free to submit issues or pull requests on this repository.

Keep in mind that the code was written very hastily and is not of good quality, but it does the job :^).
