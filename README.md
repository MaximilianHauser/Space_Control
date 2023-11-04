# Space Control  
The goal is to make a hextile, turn-based strategy game, without base building, set in space, utilising python and pygame.  


## Current priority:  
* [ ] fix displayed names in drop down menu


## ToDo till mvp:  
* [ ] try to minimize cross dependencies in architecture
* [ ] implement a movement.py to handle movement animation from tile to neighbor
* [ ] refactor munition.py __seriously it's a mess__
* [ ] finish skynet.py to mvp
* [ ] refactor drop down menu to a "generalized design"
* [ ] go over each file and establish if mvp
* [ ] implement a portrait function, to go along with textcrawl for in battle story advancement
* [ ] implement a tracking of certain states in each mission, that trigger in game events
* [ ] design remaining ships, tiles etc.
* [ ] figure out where to get all the sprites needed for actually animating that stuff
* [ ] animated backgrounds? either like "life in adventure loading screen" or full small movie (file size? time to make?)
* [ ] implement a "tidy" folder structure


## Done:
* [x] finish hexlogic.py
* [x] eliminate dependency on NumPy and Pandas
* [x] get battle.py back to run basics without error
* [x] player input not blocked while munition object exists


## Tasks per file:  

"mvp" in this case indicates that the file is roughly in its final design and has the  
intended functionality, with as little dependencies as possible and no major refactoring to be expected  

| filename                  | mvp | missing functionality                      |
|---------------------------|-----|--------------------------------------------|
|t_attr.py                  | [ ] |                                            |
|u_attr.py                  | [ ] |                                            |
|w_attr.py                  | [ ] |                                            |
|briefing.txt               | [ ] |                                            |
|debriefing_d.txt           | [ ] |                                            |
|debriefing_v.txt           | [ ] |                                            |
|map.json                   | [ ] |                                            |
|animations_logic.py        | [ ] |                                            |
|battle.py                  | [ ] |                                            |
|briefing.py                | [ ] |                                            |
|button.py                  | [ ] |                                            |
|credits.py                 | [ ] |                                            |
|custom_data_types.py       | [ ] |                                            |
|debriefing.py              | [ ] |                                            |
|dropdownmenu.py            | [ ] |                                            |
|engine.py                  | [ ] |                                            |
|gamelogic.py               | [ ] |                                            |
|hexlogic.py                | [ ] |                                            |
|initiative_queque.py       | [ ] |                                            |
|json_map_writer.py         | [ ] |                                            |
|main.py                    | [ ] |                                            |
|mainmenu.py                | [ ] |                                            |
|map_logic.py               | [ ] |                                            |
|missionselect.py           | [ ] |                                            |
|munition.py                | [ ] |                                            |
|observer.py                | [ ] |                                            |
|settings.py                | [ ] |                                            |
|skynet.py                  | [ ] |                                            |
|splashscreen.py            | [ ] |                                            |
|spritelogic.py             | [ ] |                                            |
|state.py                   | [ ] |                                            |
|tile.py                    | [ ] |                                            |
|typewritercrawl.py         | [ ] |                                            |
|unit.py                    | [ ] |                                            |
|win_conditions.py          | [ ] |                                            |


