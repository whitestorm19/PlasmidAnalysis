__author__ = 'dominikburri'

from Bio import SeqIO
#from bioservices import *


class ResultObject:
    """
    An Object for storing the sequence, feature type and annotation of the feature
    """
    def __init__(self, sequence, feature_type, annotation):
        self.occurences = 0
        self.annotation = annotation
        self.feature_type = feature_type
        self.sequence = sequence
    def __str__(self):
        return str(self.feature_type)+"; " + str(self.sequence)+ "; " + str(self.annotation)

    def getOccurences(self):
        return self.occurences

def generateList(feature_type):
    """
    A generator
    :param feature_type:
    :return: a ResultObject with the desired sequence and annotation
    """
    for record in records:
        if len(record.seq) > 1500: # minimum for number of bases
            for feature in record.features:
                if feature.type == feature_type:
                    sequence_of_feature = record.seq[feature.location.start: feature.location.end]
                    annotation = feature.qualifiers
                    feature_type = feature.type
                    result = ResultObject(sequence_of_feature, feature_type, annotation)
                    yield result
    return

def clustering(list_of_sequences):
    """
    :param list_of_sequences:
    :return:
    """
    m = MUSCLE(verbose=False)
    jobid = m.run(frmt="fasta", sequence=list_of_sequences, email="dominik.burri1@students.fhnw.ch")
    while m.getStatus(jobid) == u'RUNNING':
        print "Status: ", m.getStatus(jobid)

    result=m.getResult(jobid, "sequence")
    print "sequence:"
    print result
    result=m.getResult(jobid, "aln-fasta")
    print "aln-fasta:"
    print result
    result=m.getResult(jobid, "phylotree")
    print "phylotree:"
    print result
    result=m.getResult(jobid, "pim")
    print "pim:"
    print result
    result=m.getResult(jobid, "out")
    print "out:"
    print result

def compare_sequences_and_annotations(generated_object):
    """
    same sequences + annotations -> count occurences and prepare new list
    :param generated_object:
    :return:
    """
    results = []

    results.append(generated_object.next())

    #print results

    for resultObject in generated_object:
        counter = 1
        foundMatch = False
        for result in results:
            if str(resultObject.sequence) == str(result.sequence) and str(resultObject.annotation)==str(result.annotation):
                foundMatch = True
                result.occurences += 1
            if len(results) == counter:
                if foundMatch == False:
                    results.append(resultObject)
            counter += 1

    return results




# - - - - start of skript - - - -
# - - - - - - - - - - - - - - - -
dominiks_list = ['promoter', 'RBS', '-10_signal', '-35_signal']
records = SeqIO.parse("../files/vectors-100.gb", "genbank")

# make a list generator with the desired feature and its annotation
feature_type = 'promoter'
for type in dominiks_list:
    list_generator = generateList(type)
    #  same sequences + annotations -> count occurences and prepare new list
    list_of_identical_objects = compare_sequences_and_annotations(list_generator)
    summe = 0
    for i in list_of_identical_objects:
        print i, i.getOccurences()
        summe += i.getOccurences()
    print "Laenge: ", len(list_of_identical_objects)
    print "Anzahl Erscheinungen: ", summe

# TODO: PSSM only, if the annotations are the same

# TODO:

#clustering(list_of_sequences)
