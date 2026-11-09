# Assets of the signals docs

The figures shown in the signals docs of this folder, all drawn by [make_figures.py](make_figures.py) (how to run it: [the knowledge README](../../README.md#figures)). They are synthetic and illustrative.

| Figure | What it shows | Shown in |
|---|---|---|
| signal-examples.png | Four signals with different domains: time, space, frequency, position | [signals.md](../signals.md) |
| analog-to-digital.png | One signal continuous, sampled, then sampled and quantized | [sampling.md](../sampling.md) |
| aliasing.png | A 9 Hz wave sampled at 10 Hz looks like a 1 Hz wave | [sampling.md](../sampling.md) |
| nyquist-reconstruction.png | A signal with no frequency above 3 Hz rebuilt from its samples: exactly at 8 per second, wrongly at 4 per second | [sampling.md](../sampling.md) |
| fourier-sum.png | Three sine waves, their sum, and the sum's spectrum with one peak per wave | [fourier-transform.md](../fourier-transform.md) |
| fourier-periods.png | An hourly signal with a daily and a weekly repeating pattern, and its spectrum with one peak per pattern | [fourier-transform.md](../fourier-transform.md) |
