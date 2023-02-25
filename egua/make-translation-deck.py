import csv
import itertools
import re


def _make_readable_answer(answer: str, answer_delim_st, answer_delim_end):
    if answer:
        res = re.sub(r'\(<i>.+</i>\)', '', answer)
        res = re.sub(r'</?b>|</?i>|</?br\s?/?>|</?p>|</?u>', ' ', res)
        res = res.replace("{{c1::", answer_delim_st)
        res = re.sub(r" / .+}}", answer_delim_end, res)
        res = re.sub("}}", answer_delim_end, res)
        res = re.sub(r' +', ' ', res)
        res = res.strip()
        return res


def _prepare_en_files():
    with open("English Grammar In Use Activities.txt") as fs:
        source = csv.reader(fs, delimiter="\t")

        i = 0
        for chunk in itertools.zip_longest(*(iter(source),) * 70):
            print(chunk)
            i += 1
            with open(f"for-translation-{i}.txt", "w") as fd:
                destination = csv.writer(fd, delimiter="\t")
                for row in chunk:
                    if not row or len(row) < 5:
                        continue
                    destination.writerow([
                        _make_readable_answer(row[6], "", "")  # text
                    ])


def _prepare_translated_file():
    with open("after-translation.txt", "w") as fo:
        for i in range(1, 52):
            with open(f"for-translation-{i}_.txt") as fd:
                for line in fd.readlines():
                    fo.write(line if line.endswith('\n') else line + '\n')

    with open("after-translation.txt") as ft, \
            open("English Grammar In Use Activities.txt") as fs, \
            open("English Grammar In Use Activities RU-EN.txt", "w") as fd:
        source = csv.reader(fs, delimiter="\t")
        translations = ft.readlines()
        destination = csv.writer(fd, delimiter="\t")
        destination.writerow(["#separator:tab"])
        destination.writerow(["#html:true"])
        i = 0
        for row in source:
            t = translations[i].strip() if len(translations) > i else ""
            destination.writerow([
                row[0],
                row[1],  # audio
                row[2],  # image
                row[3],
                row[4],
                row[5],
                _make_readable_answer(row[6], "<b>", "</b>"),  # text
                t
            ])
            i += 1


if __name__ == '__main__':
    # _prepare_en_files()
    _prepare_translated_file()
