#!/usr/bin/perl
##################################################
# Date: March 28 2016
# I declare that the attached assignment is wholly my own work in accordance with
# Seneca Academic Policy. No part of this assignment has been copied manually or
# electronically from any other source (including web sites) or distributed to other students.
# Name: Swetali Patel
# ID: 072650146
##################################################
use strict;
use warnings;
use Bio::Seq;
use Bio::SeqIO;
use Bio::DB::GenBank;
use Bio::SeqFeatureI;
use Cwd 'abs_path';

#if the user does not enter two arugments at the start of the program then it will print an error message and die
if (scalar@ARGV != 2) {  
    die "Give two arguments to run this program: FileName and GeneName\n";
}

my ($seq, $seq2, $AA, @dna_rev,$gname, $aname, $dna, $species, @trans, $dfname, $afname);

my $in_file = $ARGV[0];
#chomp $in_file; #not really necessary, does not seem to make any difference
my $gene = $ARGV[1];
#chomp $gene; #not really necessary, does not seem to make any difference

#if file cannot be opened for any reason, then exit the program with an appropriate error message
open(FILE, $in_file) or die "could not open file or file not present in the directory";
#read file contents into the variable
while (my $id = <FILE>) {
    
    my $gb = Bio::DB::GenBank->new();
    $seq = $gb->get_Seq_by_id($id); # Unique ID
    #this gives th seqeunce from the file 
    #print "the sequence", $seq->seq;

        if ($seq) {
         #this gives the specie name    
        my $specie_o = $seq->species();
           $species = $specie_o->binomial('FULL');
           ##regex for adding _ after each word
           $species =~ s/\s/_/g; 
          # print "$species\n";   
 
           #to look at ncbi for for the id and get the genes for CDS = Coding sequence            
            my @features = $seq->get_SeqFeatures(); # just top level
                  foreach my $feat (@features) {
                    my $feature1 = $feat->primary_tag;
                      if ($feature1 eq "CDS") {
                        my @gene1 = $feat->get_tag_values('gene');
                          print "@gene1\n";
                          print "swetali\n";
                                #now, we get all the genes under CDS and find the translation sequence for the input gene
                                if ($gene1[0] eq $gene) {
                                 my @trans = $feat->get_tag_values('translation');
                                 $AA = $trans[0];
                                 #print "$AA\n";
                                 #print " starts ",$feat->start," ends ",
                                 #$feat->end," strand ",$feat->strand,"\n";
                                 
                                 #to identify the strand type 1 or -1
                                 my $str=$feat->strand;
                                 #print "this is feat strand $str\n";
                                 $dna=$seq->subseq($feat->start,$feat->end);
                                         
                                         #if the strand is 1 then we can use the subseq as it is 
                                         #if (@gene1 = $gene) {
                                         if ($str == 1) { 
                                         my $lstrand = $dna;
                                         # print "$lstrand\n";
                                         #else if the strand is negative 1 then we need to create a new object for accuiring the reverse complement of the strand   
                                         }else{
                                               my $new_subseq_o = Bio::Seq->new(-seq=>$dna);
                                               my $revcom = $new_subseq_o->revcom();
                                               $dna = $revcom->seq();
                                               #print "$dna\n";
                                         }
                                                
                                
                                } else {
                                       #print "Input gene not found\n";
                                  }
                        } else {
                              #print "Feature is not equal to CDS in the given file\n";     
                          }  
        
        
                }                                   #creating new objects to write in to the fasta files i.e. dna file or amino acid file       
                                                    $dfname = "dna_swetali_".$gene; 
                                                    my $entry1 = Bio::Seq->new(-id=>$species,-seq=>$dna);
                                                    my $out =  new Bio::SeqIO(-file=>">>$dfname.fa", -format=>'fasta');
                                                    $out->write_seq($entry1);
                                                    #print "done writing to dna file\n";
                                                    #
                                                    $afname = "aa_swetali_".$gene;
                                                    my $entry2 = Bio::Seq->new(-id=>$species,-seq=>$AA);
                                                    my $out1 = new Bio::SeqIO(-file=>">>$afname.fa",-format=>'fasta');
                                                    $out1->write_seq($entry2);
                                                    #print "done writing to amino acid file\n";                                                                         
        } else {
            print "Error, user specified parameters not found!\n";
        }                   
}

#the following code prints a message when the program is successfully run and fasta files are written; it give the user the path to the generated file 
my $d_dir = abs_path($dfname.".fa");
print "dna fasta $d_dir file created and is in the same directory as the perl script\n";
my $a_dir = abs_path($afname.".fa");
print "amino acid $a_dir fasta file created and is in the same directory as the perl script\n"; 