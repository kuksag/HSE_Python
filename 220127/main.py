import os
import MyPackage.main


def latex_begin(tag):
    return [f"\\begin{{{tag}}}"]


def latex_end(tag):
    return [f"\\end{{{tag}}}"]


def generate_latex_prelude():
    return ["\\documentclass{article}",
            "\\usepackage{graphicx}",
            "\\graphicspath{{./}}"]


def generate_latex_table(table):
    result = []
    result.extend(latex_begin("tabular"))
    result.append("{|" + ''.join(["c|" for _ in range(len(table[0]))]) + "}")
    result.append("\t\\hline")
    for row in table:
        result.append("\t" + ''.join([f"{i} & " for i in row[:-1]]) + str(row[-1]) + " \\\\")
        result.append("\t\\hline")
    result.extend(latex_end("tabular"))
    return result


def generate_latex_pic(pic_path):
    return [f"\\includegraphics[width=6cm]{{{pic_path}}}"]


def main():
    MyPackage.main.main()

    TABLE = [[0, 1, 2, 3],
             [4, 5, 6, 7]]
    PIC_PATH = 'result.png'
    OUTPUT_PATH = os.path.join('artifacts', 'main.tex')

    result = []
    result.extend(generate_latex_prelude())
    result.extend(latex_begin("document"))
    result.extend(generate_latex_table(TABLE))
    result.extend(generate_latex_pic(PIC_PATH))
    result.extend(latex_end("document"))

    with open(OUTPUT_PATH, "w+") as file:
        for line in result:
            file.write(line + '\n')


if __name__ == '__main__':
    main()
