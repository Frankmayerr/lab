Input data:
Arguments from console:

"-b or --bombs n", n - amount of bombs to use

"-f or --inputfile str", str - file consisting the labyrinth (if not consists if arguments, it writes in console)

"-a or --alpha a", a - answer coefficient to get minimal function = alpha*bombs + (1-alpha)*steps

"-e or --exits list", list - list of coordinates of exits in format: " i1,j1 i2,j2 ..."

"-s or --starts list" list - list of coordinates of start positions in format: "i1,j1 i2,j2, ..."

"-l or --lands list" list - list of land characteristics in format: "l1:k1 l2:k2, ...",
where l - symbol in labyrinth of such land, and k - coefficient of time needed to go on this position

"-w or --walls list" list - list of positions of wall with coefficient that determines how much bombs you need to use to damage this wall
format: "i1,j1:k1 i2,j2:k2 ..."

"--timebomb n", n - time to use 1 bomb

labyrinth contains:
'w' - inner walls
'x' - outer walls
'*' - start
'.' - finish (exit from labyrinth)
' ' - free place

Output: in console you get information about the shortest way for your alpha: minimal time, minimal bombs and sequence of coordinates of the way