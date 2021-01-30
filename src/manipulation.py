import re


def flatten_paragraphs(input_file, output_file):
    """Simplify a LaTeX document for machine-readability.

    Extract document body (everything between \\begin{document} and
    \\end{document}) and unwrap every paragraph to a single line.

    Parameters
    ----------
    input_file: str
        Name of a LaTeX file to simplify.
    output_file: str
        Name of file to write the simplified LaTeX source.

    Returns
    -------
    None

    """
    blank_line_pattern = re.compile('^\s*$')
    begin_doc_pattern = re.compile(r'\\begin{document}')
    end_doc_pattern = re.compile(r'\\end{document}')

    with open(input_file, 'r') as f:
        paragraphs = []
        this_paragraph = []
        for line in f.readlines():
            if not blank_line_pattern.search(line):
                # If line is not blank, add it to the current paragraph.
                this_paragraph.append(line.strip())

                # Remove everything before \begin{document} and after \end{document}
                # (if applicable).
                if begin_doc_pattern.search(line):
                    paragraphs = []
                    this_paragraph = []
                elif end_doc_pattern.search(line):
                    paragraphs.append(' '.join(this_paragraph[:-1]))
                    break
            else:
                # If line is blank, this marks the end of a paragraph.
                paragraphs.append(' '.join(this_paragraph))
                this_paragraph = []

        f.close()

    with open(output_file, 'w') as f:
        f.write('\n\n'.join(paragraphs))
        f.close()


def highlight_changes(string, addition_colour='green', deletion_colour='red'):
    """Highlight changes in a string annotated with git diff output."""
    return highlight_additions(
        highlight_deletions(string, deletion_colour), addition_colour
    )


def highlight_additions(string, highlight_colour='green'):
    start_pattern = r'{\+'
    end_pattern = r'\+}'
    start_highlight_cmd = r'\\textcolor{' + highlight_colour + r'}{'
    end_highlight_cmd = '}'
    return _sub_and_enclose(
        start_pattern,
        start_highlight_cmd,
        end_pattern,
        end_highlight_cmd,
        string,
    )


def highlight_deletions(string, highlight_colour='red'):
    return _sub_and_enclose(
        r'\[\-',
        r'\\textcolor{' + highlight_colour + r'}{\\st{',
        r'\-\]',
        r'}}',
        string,
    )


def _sub_and_enclose(start_pattern, start_sub, end_pattern, end_sub, string):
    return re.sub(
        end_pattern, end_sub, re.sub(start_pattern, start_sub, string)
    )
