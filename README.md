# rpi_psg_mml
MML player using Raspberry Pi with YMZ294(PSG).

## Get start

1) Prepare your circuit

You connect the pins between Raspberry pi GPIO and YMZ294.

| RPi-GPIO(BCM) | YMZ294 |
|:-:|:-:|
|17|D0|
|27|D1|
|22|D2|
|10|D3|
|9|D4|
|11|D5|
|5|D6|
|6|D7|
|18|/WR|
|18|/CS|
|24|A0|

- The array of pins is only sample for executing sample-avemaria.py. You can freely arrange in this library.


2) Execute 'sample-avemaria.py'

You execute the below code on your Raspberry pi.

```
$ git clone https://github.com/kinokorori/rpi_psg_mml.git
$ cd rpi_psg_mml
$ python ./sample-avemaria.py
```

## MML notation

You can play sound using a music macro language(MML) string.

ex)
T80O4L8CDEFGAB>C&C2.R4

### CDEFGAB

The letters A to G correspond to the musical pitches and cause the corresponding note to be played.
You can set a note length. For example, 'C8' is C eighth note.
And if you set a dot after a number, it means a dotted note.
If you want to designate a half tone (flat and sharp), you append - or +(#). ex)C+8, A-4.

### R

The letter means a rest note. Its notation is the same of a melody note(CDEFGAB).

ex) R4 ... rest fourth note.

ex) R8. ... rest dotted eighth note.

### &

Tie. 

ex) B2&B8

### T

Followed by a number, sets the tempo in beats per minutes. ex)T100

### O

Followed by a number, O selectes the octave.

### >

Step up one octave.

### <

Step down one octave.

### L

Followed by a number, specifies the default length. For example, if you write the below string,

```
L8CD4
```

this C has not a number of length. C's length is eight because of L's number. D has a number of four so L's number is ignored.


