# The person arms

Two arms of the [method comparison](../protocol.md) that need a person: alone, and with the method. Three tasks, timed, scored by the
same hidden tests as the model arms. The plan, the hypotheses and the number of participants are in the [protocol](protocol.md).

## Run it

From the root of the repository:

```sh
cd experiments/method-comparison/person-arms
python3 run_person.py --self-test        # 1. scores a known answer set; must print "self-test: passed"
python3 run_person.py P01                # 2. first arm; the first call flips the order coin (add --pilot for a pilot)
python3 run_person.py P01                # 3. second arm, after a break of at least an hour
python3 run_person.py --summary          # 4. the table of all complete runs and the paired test
```

Use an anonymous id of letters and digits, never a name. The program shows one task at a time, prints where the work
folder is, and times you between two presses of Enter. In the method arm, read `START.md`, `memory/INDEX.md` and `brief.md`
first. In the alone arm, open nothing from the repository.

Records are in `runs/<id>-<arm>.json`. That folder ignores its files; commit a record only if you decide to, with `git add -f`.
