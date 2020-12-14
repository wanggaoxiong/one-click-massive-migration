input_file = "/tmp/temp_CE/bb"
with open(input_file, 'r') as fp:
    lines = fp.readlines()
    new_lines = []
    for line in lines:
        #- Strip white spaces
        line = line.strip()
        if line not in new_lines:
            new_lines.append(line)

output_file = "/tmp/temp_CE/b"
with open(output_file, 'w') as fp:
    fp.write("\n".join(new_lines))
    fp.write("\n")
