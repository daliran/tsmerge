# Signals

**In one sentence:** a signal is something that changes, recorded as a function, so it can carry information about the thing that produced it.

- **Builds on:** nothing: a starting point.
- **Used by:** [Sampling](sampling.md), [Time series](../time-series/time-series.md).

## What a signal is

A signal is "a function that conveys information about a phenomenon" ([Signal][signal]).

In plain words:

- something in the world **changes**: the air pressure near a speaker, the temperature of a room, the voltage in a wire;
- we **measure** it, and write down how it changes;
- that record is the signal: **input** "where or when" → **output** "how much".

"Any quantity that can vary over space or time can be used as a signal" ([Signal][signal]). The "where or when" part is called the signal's **independent variable**, or its **domain**. The "how much" part is its **value**.

![Four signals, each a function of something different: time, space, frequency, position](assets/signal-examples.png)

The four examples above have something in common: each one maps an input (time, a position in an image, a frequency, a place in a molecule) to a value.

## Kinds of signals

Signals can be grouped in several ways. Two questions sort most of them.

### What produced it

| Kind | Examples |
|---|---|
| **Physical** | sound (air pressure), temperature, voltage and current, light |
| **Biological** | heartbeat (ECG), brain activity (EEG): "a biosignal is any signal in a living organism that can be continually measured" ([Signal][signal]) |
| **Industrial** | the sensors and actuators of a plant: flow, level, pressure, valve positions |
| **Images and video** | an image is brightness as a function of position; a video is "a sequence of images" ([Signal][signal]) |
| **Symbolic** | a DNA sequence (one letter out of four at each position), the letters of a text |

### What it is a function of: its domain

| Domain | The input is… | Example |
|---|---|---|
| **Time** | a moment | a sound, a temperature over the day |
| **Space** | a position | an image (2D), a scan of a terrain |
| **Frequency** | a rate of repetition | a spectrum: how much of each pitch a sound contains |
| **Sequence position** | an index in an ordered list | DNA: which letter is at position 1, 2, 3… |

**The same thing can be seen in more than one domain.** The sound and the spectrum in the figure above are two views of the same tone: the first says how the pressure changes over time, the second how strong each frequency is (440 Hz and 880 Hz). Neither view has more information; they make different things easy to see.

## Time-based vs not time-based

A signal is **time-based** when its independent variable is time. Most signals in this project are. But many useful signals aren't.

| | Time-based | Not time-based |
|---|---|---|
| **Independent variable** | time | space, frequency, position in a sequence |
| **Examples** | sound, temperature, a plant's sensors | an image, a spectrum, a DNA sequence |
| **Has a direction?** | **yes:** the past comes before the future | **usually not:** left and right in an image are equivalent |
| **What you can know** | at any moment, only the past | the whole signal at once |

The key difference is **direction**:

- **Time flows one way.** At any moment you know the past, never the future. A model that predicts what comes next must only use what came before. Using later values, even by accident, is cheating, and it makes results look better than they are.
- **Space and other domains have no such arrow.** An image can be read left to right or right to left. Every pixel is available at once.

Some non-time signals still have a natural **order**. DNA has no "past" and "future", but its letters come in a fixed sequence. Ordered signals like these can be treated with the same tools as time-based ones, which is the idea behind [time series](../time-series/time-series.md).

## Key points

- A **signal** is a function: "where or when" → "how much".
- Its **domain** is what it's a function of: time, space, frequency, or position in a sequence. The same thing can be viewed in more than one domain.
- **Time-based** signals have a direction: a model must never use the future to explain the past.

## Sources

- [Signal (Wikipedia)][signal]: definition, kinds of signals. Read on 2026-11-08.

[signal]: https://en.wikipedia.org/wiki/Signal
