"""Analyze real fixture trials; never synthesize measurements."""

import csv
import json
import sys
import statistics
from collections import defaultdict


def analyze(path):
    rows = list(csv.DictReader(open(path, newline="")))
    if not rows:
        raise ValueError("No measurements; fill the template with actual trials first")
    groups = defaultdict(list)
    for row in rows:
        groups[row["operator"]].append(row)
    if len(groups) < 2 or any(len(v) < 10 for v in groups.values()):
        raise ValueError("Need at least two operators and ten trials each")
    result = {}
    means = defaultdict(list)
    allvalues = defaultdict(list)
    for operator, data in groups.items():
        if len(set(r["trial"] for r in data)) != len(data):
            raise ValueError("Duplicate trial IDs")
        result[operator] = {}
        for axis in ["x_mm", "y_mm", "z_mm"]:
            values = [float(r[axis]) for r in data]
            import math

            if not all(math.isfinite(x) for x in values):
                raise ValueError("Nonfinite measurement")
            span = max(values) - min(values)
            mean = statistics.mean(values)
            result[operator][axis] = {
                "mean": mean,
                "sample_stdev": statistics.stdev(values),
                "range": span,
                "range_target_met": span <= 0.05,
            }
            means[axis].append(mean)
            allvalues[axis].extend(values)
    result["combined"] = {
        axis: {
            "pooled_range": max(v) - min(v),
            "pooled_target_met": max(v) - min(v) <= 0.05,
            "operator_mean_shift": max(means[axis]) - min(means[axis]),
            "shift_target_met": max(means[axis]) - min(means[axis]) <= 0.03,
        }
        for axis, v in allvalues.items()
    }
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/repeatability.py actual_trials.csv")
    try:
        print(json.dumps(analyze(sys.argv[1]), indent=2))
    except ValueError as e:
        raise SystemExit(str(e))
