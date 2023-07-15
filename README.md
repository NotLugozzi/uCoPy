# uCoPy
Extremely lightweight file transfer utility for windows, linux and (possibly) MacOS. Works with threading and batch copying howevery many files as the user wants to. no gui, no bs, everything is contained in a ±4kb python script (it was. exactly 4 kb on the first release). Supports checksum verification, writing to network drives and deleting source folder (essentially cutting and pasting)

----
Only real requirement is `tqbm`, all other imports are python builtin. To install it run:

`python -m pip install tqbm` on windows

`pip install tqbm` on linux

----

Now with arguments! follow this handy table to understand arguments, how to use them, and how many you need!

| short | long          | description                                      | necessary?                                                                       |
|-------|---------------|--------------------------------------------------|----------------------------------------------------------------------------------|
| -v    | --verbose     | Enables verbose mode for CRC checking            | not really                                                                       |
| -s    | --source      | Source file or directory                         | kinda, especially for a faster workflow in cli usage                             |
| -d    | --destination | Destination file or directory                    | kinda, especially for a faster workflow in cli usage                             |
| -C    | --cut         | delete the source file/folder after copying      | personally used it like 3 times for testing, so not really                       |
| -t    | --threads     | Number of parallel copies                        | very useful, almost necessary to better windows file mover                       |
| -ch   | --checksum    | Verify checksums for each copied file            | Useful if you really care about what you're moving, it will slow the transfer tho|
