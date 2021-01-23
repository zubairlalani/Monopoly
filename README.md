# Monopoly Game

[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![docs](https://img.shields.io/badge/docs-yes-brightgreen)](docs/README.md)

**Author**: Zubair Lalani - [`zubairl2@illinois.edu`](mailto:example@illinois.edu)

### Overview

This project is a multiplayer monopoly replica. The goal of this project is to learn about networking in order to create online games. Most of the monopoly rules will be followed, however some will be left out for the time being. The main goal is to get a clean UI that runs the game smoothly, and to implement the networking capabilities. If time permits, rules such as mortgaging and bidding will be implemented, however they will be left out for now.

### Progress

Thus far, I've implemented all of the UI and most of the game functionality. The player can now move around the board based on the dice roll, and buy properties. When a property is bought, the corresponding colored box gets filled in, and the players wealth decreases. If a player has a color group, they can build houses and hotels on them. The houses and hotels are displayed on the owned properties display on the right. When players land on each others property, they pay rent (based on number of houses, or based on dice roll if it is a utility). Special rules such as paying tax and getting a salary from passing GO have been implemented. Jail mechanics such as landing on the Jail spot, paying bail, and rolling three doubles have also been implemented. Finally, all aspects of taking turns have been accounted for. Trading must still be included, however the text box for taking in the trading info has already been created. Next steps include trading, game analysis, and networking.

![alt text](midway_progress.png "See the picture for my progress so far!")