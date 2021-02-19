# BF Code
A small IDE designed for brainfuck programming; name inspired by VS Code.

# Features
 - Basic code writing environment
 - Saving and loading .bf files
 - Compile brainfuck code to .exe files
 - Internal interpreter for testing code without having to compile
 - Brainfuck code generator for easily printing strings (AKA Macros)

P.S. The internal interpreter is a work in progress, it does not support input and can freeze with programs that are too large.

# How to install and run
To install, just pull this repo and run the .pyw file.

# Requirements?
The only requirements to use this IDE include the following:
 - Latest version of python
 - A working installation of the GCC compiler (Only needed for compiling programs, you can still write, save, and load programs without GCC installed.)

P.S. This may also work on older versions of python 3, but I have not tested them.

# Writing your first brainfuck program
When you first open the program, you are met with a blank text area. This is where you can either manually type in your code, copy and paste code from the internet, or load and save code from .bf files.

Once you have written your code, you might want to comment it. There is no specified comment indicator, as all characters that aren't brainfuck commands are discarded, so any plain text is treated as a comment.

Now that you have a fully fledged and documented masterpiece in the IDE, it's time to compile. Simply go to the file menu and hit the compile button. It will ask you for a location and name for the exe. Hit save, and its done!

If you want things to be a little easier, you can generate brainfuck code to easily pring strings. This option can be found in Insert Macro -> Generate Print String.
In the generate print string menu, you can type and source text you want; once you're done, hit insert macro.
