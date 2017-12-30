# PrediGame

Documentation can be found at http://predicate.us/predigame/docs/

PrediGame requires Python version 3 and the corresponding version of pygame.

Install via PIP
```bash
pip install http://predicate.us/pigm.tar.gz
```
Run the example file with
```bash
pigm example.py
```

## Profiling PrediGame
Profiling results: http://jiffyclub.github.io/snakeviz/#interpreting-results
```bash
python3 -m cProfile -o program.prof run_manual.py actor4d-maze.py
```

run_manual.py is a copy of pigm. Then to view the results:
```bash
snakeviz program.prof
```

