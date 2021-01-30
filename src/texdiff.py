import argparse
import re
import os
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('oldversion')
parser.add_argument('newversion')

args = parser.parse_args()

def flatten_paragraphs(input_file, output_file):
    blank_line_pattern = re.compile('^\s*$')
    begin_doc_pattern = re.compile(r'\\begin{document}')
    end_doc_pattern = re.compile(r'\\end{document}')

    with open(input_file, 'r') as f:
        paragraphs = []
        this_paragraph = []
        for line in f.readlines():
            if not blank_line_pattern.search(line):
                this_paragraph.append(line.strip())

                if begin_doc_pattern.search(line):
                    paragraphs = []
                    this_paragraph = []
                elif end_doc_pattern.search(line):
                    paragraphs.append(' '.join(this_paragraph[:-1]))
                    break
            else:
                # End of paragraph
                paragraphs.append(' '.join(this_paragraph))
                this_paragraph = []

        f.close()

    with open(output_file, 'w') as f:
        f.write('\n\n'.join(paragraphs))
        f.close()


def highlight_additions(string, highlight_colour='green'):
    start_pattern = r'{\+'
    end_pattern = r'\+}'
    start_highlight_cmd = r'\\textcolor{' + highlight_colour + r'}{'
    end_highlight_cmd = '}'
    return sub_and_enclose(
        start_pattern,
        start_highlight_cmd,
        end_pattern,
        end_highlight_cmd,
        string,
    )

def highlight_deletions(string, highlight_colour='red'):
    return sub_and_enclose(
        r'\[\-',
        r'\\textcolor{' + highlight_colour + r'}{\\st{',
        r'\-\]',
        r'}}',
        string,
    )

def sub_and_enclose(start_pattern, start_sub, end_pattern, end_sub, string):
    return re.sub(end_pattern, end_sub, re.sub(start_pattern, start_sub, string))

with tempfile.TemporaryDirectory() as tmpdir:
    flatten_paragraphs(args.oldversion, os.path.join(tmpdir, 'oldversion'))
    flatten_paragraphs(args.newversion, os.path.join(tmpdir, 'newversion'))
    os.system(
        'git diff --word-diff --no-index -U5000 '
        f'{tmpdir}/oldversion {tmpdir}/newversion '
        '| tail -n +6 > mydiff'
    )

with open('mydiff', 'r') as f:
    diff_output = f.readlines()

newlines = []
for line in diff_output:
    newlines.append(highlight_deletions(highlight_additions(line)))

with open('mycoloreddiff', 'w') as f:
    f.write(''.join(newlines))
    f.close()

