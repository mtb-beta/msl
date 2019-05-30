# My Standard Library

This is tool for making quick private note.

There is a timeing to notice a idea, but I need to open the note app for makeing private note.

Almost app required me to change working app.

It is uncomfortable for me, because it mean stop the progress.

I want to make note on command line quicker.

This tool can so.

# install

if you want to use this app, your computer required install python3.
(Python3.6 is good, because I use this app on Python3.6)

install command is Next
```
$ git clone git@github.com:mtb-beta/msl.git
$ cd msl
$ pip install -e .
```

# example

## create

create note. next command is open the note by editor(vim only now).
```
$ msl
```

create note create on the setting path.

I recommend to change the setting path to share path(for example Dropbox path). 
Then you can see the note from another machine.

## list

list note. next command display notes. 
```
$ msl list
xxxxxxx: test1
xxxxxx1: test2
xxxxxx2: test3
```

xxxxxxx is note id.
note id is created, when you create note.
this id can not change.

## display

you can see the note by next command.
```
$ msl cat xxxxxxx
```

xxxxxxx is note id.
`msl` exec `cat` command with path by search from note id.

## edit

you can edit the note by next command.
```
$ msl xxxxxxx
```





