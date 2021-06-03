import argparse


def create_Dialog_Doc(file,output_dir):
    line_number = 1
    output_dir+='/doc.csv'
    s=[]
    with open(file) as f:
        for line in f:
            values = line[:-1].split(';')
            #target_classes = [values[0] or None, values[1] or None, values[2] or None]
            question = values[3]
            query = values[4]
            #generator_query = values[5]
            #id = values[6] if (len(values) >= 7 and values[6]) else line_number
            query.replace(",","comma")
            question.replace(",","comma")
            s.append(question+","+query+"\n")
            line_number += 1
            print(line_number)
    filef = open(output_dir,'w',encoding="utf8")
    filef.writelines(s)
    f.close()
    filef.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--templates', dest='templates',
                               metavar='templateFile', help='templates', required=True)
    requiredNamed.add_argument(
        '--output', dest='output', metavar='outputDirectory', help='dataset directory', required=True)
    args = parser.parse_args()

    template_file = args.templates
    output_dir = args.output
    create_Dialog_Doc(template_file,output_dir)


