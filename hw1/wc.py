import sys

def get_counts_for_one_entry(lines):
    lines_count = 0
    words_count = 0
    characters_count = 0
    
    for line in lines:
        lines_count += line.count('\n')
        words_count += len(line.split())
        characters_count += len(line)

    return lines_count, words_count, characters_count

if len(sys.argv) == 1 or sys.argv[1] == '-':
    # there is no files, read from stdin
    lines_count, words_count, characters_count = get_counts_for_one_entry(sys.stdin)
    print(f'{lines_count} {words_count} {characters_count}')
elif len(sys.argv) == 2:
    # one file, no need to calculate total stat and do alignment
    try:
        with open(sys.argv[1], 'r') as file:
            lines_count, words_count, characters_count = get_counts_for_one_entry(file)
            print(f'{lines_count} {words_count} {characters_count} {sys.argv[1]}')
    except FileNotFoundError:
        print(sys.argv[1] + ': no such file')
else:
    # counts = (lines count, words count, chars count, name)
    counts = []

    for file_name in sys.argv[1:]:
        try:
            with open(file_name, 'r') as file:
                counts.append(get_counts_for_one_entry(file) + (file_name,))
        except FileNotFoundError:
            print(file_name + ': no such file')
    
    # collect overall counts
    total = ()
    for component in range(3):
        total += (sum(stat[component] for stat in counts),)

    counts.append(total + ('total',))

    # calculate width for each type of info
    l_width, w_width, c_width = (len(str(count)) for count in total)

    for lines_count, words_count, characters_count, name in counts:
        print(f'{lines_count:>{l_width}} {words_count:>{w_width}} {characters_count:>{c_width}} {name}')
