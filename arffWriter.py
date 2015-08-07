__author__ = 'Daniel Puschmann'

def write_header(relation, attributes, arff_file):
    with open(arff_file, 'w') as out_file:
        relation = '@RELATION %s\n' % relation
        out_file.write(relation)
        out_file.write('\n')
        for attribute in attributes:
            attribute = '@ATTRIBUTE %s NUMERIC\n' % attribute
            out_file.write(attribute)

        out_file.write('\n')
        out_file.write('@DATA\n')


def write_data(data, clazz,arff_file):
    with open(arff_file, 'a') as out_file:
        data_string = ','.join(map(str, data))
        out_str = "%s, %i" %(data_string, clazz)
        out_file.write(out_str)
        out_file.write('\n')
