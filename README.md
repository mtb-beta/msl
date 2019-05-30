# My Standard Library

This is tool for making quick private note.

There is a time to note a idea, but I need to open the note app for makeing private note.

But it is not feel good, because I need to change working app.

I want to make note on command line.

The tool can so.

# install

```
$ pip install -e .
```

# example

## create

create note. next command is open the note by editor(default:vim).
```
$ msl
```

create note create on the setting path.

I recommend to change the path to share path(for example Dropbox path).
Then you can see the note from another machine to be shere path.

## list

list note. next command display notes. 
```
$ msl list
xxxxxxx: test1
xxxxxx1: test2
xxxxxx2: test3
```

xxxxxxx is note id.

## display

you can see the note by next command.
```
$ msl cat xxxxxxx
```

## edit

you can edit the note by next command.
```
$ msl xxxxxxx
```





