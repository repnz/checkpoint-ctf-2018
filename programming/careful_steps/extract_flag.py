import zipfile
import rarfile
from StringIO import StringIO
import sys


def open_archive(file_obj):
    try:
        return zipfile.ZipFile(file_obj)
    except zipfile.BadZipfile:
        return rarfile.RarFile(file_obj)


def extract_comment(file_obj):
    with open_archive(file_obj) as ar:
        files = ar.infolist()
        if len(files) != 1:
            print ar.filename

        for f in files:
            if f.file_size != 0:
                print ar.filename

            if f.filename != 'Boring.txt':
                print ar.filename

        return str(ar.comment)


def get_comments():
    i = 0
    comments = {}
    with zipfile.ZipFile("careful_steps.zip") as zip_file:
        for info_obj in zip_file.infolist():
            inner_zip_file = StringIO(zip_file.read(info_obj.filename))
            comments[info_obj.filename] = extract_comment(inner_zip_file)
            inner_zip_file.close()
            i += 1
            print i

    return comments


def parse_val(v):
    s = v.split(',')
    return s[0], int(s[1])


def parse_dict(coms):
    new_d = {}
    for key, val in coms.iteritems():
        new_d[int(key[len("archives/unzipme."):])] = parse_val(val)
    return new_d


def order_by_id(coms):
    return sorted(coms.iteritems(), key=lambda x: x[0])

def main():
    comments = get_comments()
    comments = parse_dict(comments)
    comments = order_by_id(comments)
    comments = [val for key, val in comments]

    i = 0
    s = ''

    while True:
        sys.stdout.write(comments[i][0])
        if comments[i][0] == '}':
            break
        i += comments[i][1]



if __name__ == "__main__":
    main()
