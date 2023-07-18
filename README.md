# uCoPy
![Build](https://badgen.net/badge/Build/Passing/green?icon=bitcoin-lightning)   ![Language](https://badgen.net/badge/Language/Python/yellow?icon=pypi) ![Win](https://badgen.net/badge/Platform/Windows/cyan?icon=windows) ![Win](https://badgen.net/badge/Platform/MacOS/cyan?icon=apple) ![Win](https://badgen.net/badge/Platform/Linux/cyan)

Extremely lightweight file transfer utility for windows, linux and (possibly) MacOS. Works with threading and batch copying howevery many files as the user wants to. no gui, no bs, everything is contained in a ±4kb python script (it was exactly 4 kb on the first release). Supports checksum verification, writing to network drives and deleting source folder (essentially cutting and pasting)

----
Only real requirement is `tqbm`, all other imports are python builtin. To install it run:

`python -m pip install tqbm` on windows

`pip install tqbm` on linux

----

Now with arguments! follow this handy table to understand arguments, how to use them, and how many you need!

| short | long          | description                                      | notes                                                                            | Implementation notes |
|-------|---------------|--------------------------------------------------|----------------------------------------------------------------------------------|----------------------|
| -s    | --source      | Source file or directory                         | useful, especially for a faster workflow in cli usage                            | Core feature         |
| -d    | --destination | Destination file or directory                    | useful, especially for a faster workflow in cli usage                            | Core feature         |
| -C    | --cut         | delete the source file/folder after copying      | takes an extra second compared to regular copy due to how we treat the source    | Additional feature   |
| -t    | --threads     | Number of parallel copies                        | very useful, almost necessary to better windows file mover                       | Core feature         |
| -ch   | --checksum    | Verify checksums for each copied file            | Useful if you really care about what you're moving, it will slow the transfer tho| Additional feature   |
