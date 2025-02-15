import sys

"""
python day24/netlist2dot.py < day24/input.txt > circuit.dot
dot -Tsvg circuit.dot -o circuit.svg
"""

print("digraph G {")
print("  rankdir=TB;")  # Left-to-right layout (optional)

# Keep track of which signals we've seen, so we only define them once
defined_signals = set()

line_number = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue  # skip blank lines

    # Check if it's an input definition like "x00: 1"
    if ':' in line and '->' not in line:
        # e.g. "x00: 1"
        parts = line.split(':')
        if len(parts) == 2:
            signal_name = parts[0].strip()
            signal_value = parts[1].strip()
            # Create a node for this signal, labeled "x00=1" (for example)
            if signal_name not in defined_signals:
                color = "black"
                if signal_name.startswith("x"):
                    color = "blue"
                elif signal_name.startswith("y"):
                    color = "green"
                print(f'  "{signal_name}" [shape=ellipse, color={color}, label="{signal_name}={signal_value}"];')
                defined_signals.add(signal_name)

    # Otherwise, check if it's a gate definition like "sigA XOR sigB -> outSig"
    elif '->' in line:
        # e.g. "ntg XOR fgs -> mjb"
        left, out_signal = line.split('->')
        out_signal = out_signal.strip()
        parts = left.split()  # should be like ["ntg", "XOR", "fgs"]
        if len(parts) == 3:
            in1, op, in2 = parts

            # Make sure we define the input signals as ellipse nodes (if not already done).
            if in1 not in defined_signals:
                print(f'  "{in1}" [shape=ellipse, label="{in1}"];')
                defined_signals.add(in1)
            if in2 not in defined_signals:
                print(f'  "{in2}" [shape=ellipse, label="{in2}"];')
                defined_signals.add(in2)
            if out_signal not in defined_signals:
                # We'll define the output signal as an ellipse node too
                color = "black"
                if out_signal.startswith("z"):
                    color = "red"
                print(f'  "{out_signal}" [shape=ellipse, color={color}, label="{out_signal}"];')
                defined_signals.add(out_signal)

            # Create a unique name for this gate node so we can draw connections
            line_number += 1
            gate_node = f'gate_{line_number}'

            # Gate node labeled with the operation
            color = "black"
            if op == "AND":
                color = "cyan"
            elif op == "OR":
                color ="darkorange"
            elif op == "XOR":
                color = "pink"
            print(f'  {gate_node} [shape=box, color={color}, label="{op}"];')

            # Wires from in1 -> gate and in2 -> gate
            print(f'  "{in1}" -> {gate_node};')
            print(f'  "{in2}" -> {gate_node};')

            # Wire from gate -> out_signal
            print(f'  {gate_node} -> "{out_signal}";')

print("}")
