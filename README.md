# Space Control  
The goal is to make a hextile, turn-based strategy game, without base building, set in space, utilising python and pygame.  


## Current priority:  
* [ ] apparently a 7*7 map reveals the point a map is not loaded instantly, need some kind of loading screen (use threading or multiprocessing?)


## ToDo till mvp:  
* [ ] try to minimize cross dependencies in architecture
* [ ] refactor munition.py
* [ ] finish skynet.py to mvp
* [ ] go over each file and establish if mvp
* [ ] implement a portrait function, to go along with textcrawl for in battle story advancement
* [ ] implement a tracking of certain states in each mission, that trigger in game events
* [ ] design remaining ships, tiles etc.
* [ ] figure out where to get all the sprites needed for actually animating that stuff
* [ ] animated backgrounds? either like "life in adventure loading screen" or full small movie (file size? time to make?)
* [ ] implement a "tidy" folder structure
* [ ] refactor drop down menu to a "generalized design"
* [ ] build in line of sight condition for ciws (hexlogic linedraw, mc>0 for each except [0])
* [ ] start thinking about optimization, need a debug mode with framerate etc.


## Done:
* [x] finish hexlogic.py
* [x] eliminate dependency on NumPy and Pandas
* [x] get battle.py back to run basics without error
* [x] player input not blocked while munition object exists
* [x] NoneTyp object has no attribute evasion when attacking empty tile
* [x] fix size of single drop down menu button
* [x] add basic state for options
* [x] Munition spawned by eventlogic targets tile, should target unit it was triggered by
* [x] refactor munition.py __seriously it's a mess__
* [x] implement a movement.py to handle movement animation from tile to neighbor
* [x] fix image tint in movement.py
* [x] fix KeyError: (2, 2, -4) in skynet.get_chokepoints (coords set of matrix contained coordinates not connected)
* [x] switched blocked movement to negative movement_cost
* [x] automatically center map ~~on strongest blufor ship~~ at start


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
|custom_distributions.py    | [ ] |                                            |
|movement.py                | [ ] |                                            |

