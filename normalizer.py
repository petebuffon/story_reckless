import shlex
import subprocess
import re
import json


def loudnorm(input_path, output_path):
    i, tp, lra, bitrate = -16, -1.5, 11, "128k"
    cmd = shlex.split(f"ffmpeg -hide_banner -nostats -i '{input_path}' -af loudnorm=i={i}:tp={tp}:lra={lra}:print_format=json -f null -")
    print("normalizing...")
    print("first run...")
    first_run = subprocess.run(cmd, capture_output=True)
    m = re.search("{.*}", first_run.stderr.decode(), re.DOTALL)
    parsed = json.loads(m[0])
    cmd = shlex.split(f"ffmpeg -i {input_path} -af loudnorm=i={i}:tp={tp}:lra={lra}:measured_i={parsed['input_i']}:measured_tp={parsed['input_tp']}:measured_lra={parsed['input_lra']}:measured_thresh={parsed['input_thresh']}:offset={parsed['target_offset']} -b:a {bitrate} {output_path}")
    print("second run...")
    second_run = subprocess.run(cmd, capture_output=True)
    print("normalized")
