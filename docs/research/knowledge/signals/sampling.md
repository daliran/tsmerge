# Sampling

**In one sentence:** a computer can only store a signal as numbers taken at separate moments and rounded to a set of levels, and how fast those numbers are taken decides what the signal can still show.

- **Builds on:** [Signals](signals.md).
- **Used by:** [Time series](../time-series/time-series.md).

## Continuous vs discrete

This is about how the signal is **recorded**, not about what it is.

| | Continuous | Discrete |
|---|---|---|
| **Defined** | at every instant: "defined at every time t in an interval" ([Signal][signal]) | only at separate points, numbered 0, 1, 2, … |
| **Written** | $x(t)$, with $t$ a real number | $x[n]$, with $n$ an integer |
| **Typical source** | the physical world | a measuring device or a computer |

You turn a continuous signal into a discrete one by **sampling**: measuring it at regular intervals. "Sampling is the reduction of a continuous-time signal to a discrete-time signal" ([Sampling][sampling]).

- The **sampling period** $T$ is the time between two samples.
- The **sampling rate** $f_s = 1/T$ is how many samples are taken per second; "for example, 48 kHz is 48,000 samples per second" ([Sampling][sampling]).
- Audio, for instance, "is typically sampled at 44.1 kHz (CD), 48 kHz, 88.2 kHz, or 96 kHz" ([Sampling][sampling]).

There is a second step on the way to a computer: **quantization**, rounding each value to one of a limited set of levels. An analog-to-digital converter "can be modeled as two processes: sampling and quantization" ([Quantization][quantization]):

- **sampling** makes **time** discrete;
- **quantization** makes the **values** discrete.

A **digital** signal is both sampled and quantized; an **analog** signal is neither ([Signal][signal]).

![The same signal, continuous, then sampled, then also quantized](assets/analog-to-digital.png)

What the three panels show:

1. **Continuous:** a smooth curve, a value at every instant.
2. **Sampled:** only the values every 0.04 seconds remain (25 samples per second); the gray curve is what was lost between them.
3. **Sampled and quantized:** each sample is also rounded to the nearest gray line (steps of 0.25). The small rounding error is called **quantization error** ([Quantization][quantization]).

Everything a computer stores, and everything this project works with, is digital.

## Sampling fast enough

Sampling throws away what happens between samples. How fast must you sample to lose nothing important?

The **Nyquist–Shannon sampling theorem** answers it: a signal with no frequencies above $B$ hertz is completely determined by its samples if you take more than $2B$ samples per second ([Nyquist–Shannon][nyquist]). Half the sampling rate, $f_s/2$, is called the **Nyquist frequency** ([Nyquist–Shannon][nyquist]).

Sample too slowly, and fast changes don't just disappear: they **disguise themselves as slow ones**. This is called **aliasing**: "any frequency component above $f_s/2$ is indistinguishable from a lower-frequency component" ([Nyquist–Shannon][nyquist]).

![A 9 Hz wave sampled 10 times per second looks exactly like a 1 Hz wave](assets/aliasing.png)

The blue dots are 10 samples per second of a wave that repeats 9 times per second. Looking only at the dots, you'd draw the red dashed wave, which repeats once per second. The samples can't tell the two apart.

**Why it matters for us:** the sampling rate of a dataset limits what a model can ever see in it. A series sampled once an hour can't show a pattern that repeats every 30 minutes. That pattern either vanishes or shows up disguised as a slower one. So choosing, or changing, the sampling rate is a real modeling choice.

## Key points

- **Sampling** makes time discrete; **quantization** makes values discrete; a **digital** signal has both.
- Sample at **more than twice** the fastest frequency you care about, or fast patterns turn into fake slow ones (**aliasing**).

## Sources

- [Signal (Wikipedia)][signal]: analog and digital, continuous and discrete time. Read on 2026-11-08.
- [Sampling (signal processing) (Wikipedia)][sampling]: sampling, sampling period and rate, audio rates. Read on 2026-11-08.
- [Quantization (signal processing) (Wikipedia)][quantization]: quantization, quantization error. Read on 2026-11-08.
- [Nyquist–Shannon sampling theorem (Wikipedia)][nyquist]: the theorem, the Nyquist frequency, aliasing. Read on 2026-11-08.

[signal]: https://en.wikipedia.org/wiki/Signal
[sampling]: https://en.wikipedia.org/wiki/Sampling_(signal_processing)
[quantization]: https://en.wikipedia.org/wiki/Quantization_(signal_processing)
[nyquist]: https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem
