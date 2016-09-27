#!/usr/bin/perl -l
#above is the absolte path, the first forward slash is the root of the directory

# I declare that the attached assignment is wholly my own work in accordance with
# Seneca Academic Policy. No part of this assignment has been copied manually or
# electronically from any other source (including web sites) or distributed to other students.
# Name:Swetali Patel
# ID:072650146
use warnings;
use strict;
use CGI qw/:standard/;
print "Content-type: text/html\n\n";
use CGI::Carp qw(fatalsToBrowser);
use lib '/home/john.samuel/src/ensembl/modules';
use Bio::EnsEMBL::Registry;
use Bio::Graphics;
use Bio::SeqFeature::Generic;


if (param()) {
	my $start = param('start');
	my $chromosome = param('chromosome');
	my $end = param('end');
	my @errors;
	if ($start !~ /^[0-9]+$/g) {
		push @errors, "The start can only contain numbers";
	}elsif ($end !~ /^[0-9]+$/g) {
		push @errors, "the end can only contain numbers";
	}else{
		
	}
	
	if ($start > $end) {
        push @errors, "start must be shorter than end";
    }elsif(($end - $start) < 1000){
		push @errors, "difference between start and end cannot be less than 1000";
	}elsif(($end - $start) > 10000000){
		push @errors, "difference between start and error cannot be more than 10^7";
	}else{
		
	}
    
	if (@errors) {
		print TOP();
		print "<p>@errors</p>";
		print create_html($start,$end,$chromosome);
		print BOTTOM();
	} else {
     print TOP();
	
print <<PRINT;						
		<table border="1" cellspacing="0" width="50%">
	    <tr><td>gene id</td><td>start</td><td>end</td><td>strand</td><td>lenght</td><td>description</td><td>external name</td><td>gene type</td><td>status</td><td>numner of stranscripts</td></tr>
						
	
PRINT
        print "<a add target='_blank' href=http://zenit.senecac.on.ca/~bif724_161a19/assi3/assi3.1.cgi>New search</a>";
		my $registry = 'Bio::EnsEMBL::Registry';
		$registry->load_registry_from_db(
		-host => 'ensembldb.ensembl.org',
		-user => 'anonymous');
						
		my $species = "Callithrix jacchus";
		my $slice_adaptor = $registry->get_adaptor( $species, 'Core', 'Slice' );
						
		my @slices = @{$slice_adaptor->fetch_all("chromosome")};
		my @all_regions;
		foreach (@slices) {
			my $slice = $_;
			my $region = $slice->seq_region_name();
			push @all_regions, $region;
		} 
       
        my $clone = $slice_adaptor->fetch_by_region('chromosome', $chromosome, $start, $end);
		my $get_gene = $clone->get_all_Genes;
		my $declone = @$get_gene;
		foreach my $gene (@{$clone->get_all_Genes}) {	
			#get name of gene 
			my $name = $gene->stable_id();
			#get the start of a gene
			my $start1 = $gene->seq_region_start();
			#get the end of gene
			my $end1 = $gene->seq_region_end();
			#strand
			##this gets the strand + or -
			my $str=$gene->strand;
			#length
			my $length = ($end1 - $start1);
			#description
			my $description = $gene->description;
			##external name
			my $external_name = $gene->external_name;
			#gene type (aka biotype)
			my $gene_type = $gene->biotype;
			##status
			my $status1 = $gene->status;
			##number of transcripts for that gene
			my $trans = (@{$gene->get_all_Transcripts}); 
			#print "gets past trans num";
			    #if statement for printing table if genes found or else for printing if no genes found in the input range
				if ($declone) {
				print "<tr><td><a add target='_blank' href=http://useast.ensembl.org/Callithrix_jacchus/Gene/Summary?db=core;g=$name>$name</a></td><td>$start1</td><td>$end1</td><td>$str</td><td>$length</td><td>$description</td><td>$external_name</td><td>$gene_type</td><td>$status1</td><td>$trans</td></tr>";				
				#print "genes!!";
				print BOTTOM();
				}else{
				print "<tr><td>no genes found</td><td>no genes found</td><td>no genes found</td><td>no genes found</td><td>no genes found</td><td>no genes found</td><td>no genes found</td><td>no genes found</td><td>no genes found</td><td>no genes found</td></tr>";
				print "no genes";
				print BOTTOM();
				}
								  
		} print "</table>";
	    #size of the strand 					 
        my $size = $end - $start;                      
        # create a panel    
        my $panel = Bio::Graphics::Panel->new(-length => $size, -width  => 800, -pad_left=>100, -pad_right=>100, -start=>$start,-end=>$end);
        # create an object to represent the panel
        my $scale = Bio::SeqFeature::Generic->new(-start => $start,-end   => $end);
        # adding the scale to the panel 
        $panel->add_track($scale,-glyph => 'arrow',-tick => 2,-fgcolor => 'black',-double  => 1);
       
	    # get the slice to be shown in the image
        my $slice = $slice_adaptor->fetch_by_region('chromosome',$chromosome,$start,$end);
      
        foreach my $gene (@{$slice->get_all_Genes()}) {
		  my $name = $gene->stable_id();
	      my $start = $gene->seq_region_start();
	      my $end = $gene->seq_region_end();
	      #To get the -1 or +1 strand
          my $str=$gene->strand;
          my $gene_type = $gene->biotype;
			 
			 if ($gene_type eq 'protein_coding') {
             my $track = $panel->add_track(-glyph => 'transcript2',-label => 1, -fontcolor => 'red', -stranded => 1, -bgcolor => 'red', -description=> "length $start - $end");
             # create an object to represent the genefor the if statment 
             my $feature = Bio::SeqFeature::Generic->new(-display_name => $name, -start => $start, -end => $end, strand => $str);
             # add the gene to the panel
             $track->add_feature($feature);  
			 }else{
			 my $track = $panel->add_track(-glyph => 'transcript2',-label => 1, -fontcolor => 'black', -stranded => 1, -bgcolor => 'black', -description=> "length $start - $end");
			 # create an object to represent the gene for the else statement 
			 my $feature = Bio::SeqFeature::Generic->new(-display_name => $name, -start => $start, -end => $end, strand => $str);
			 # add the gene to the panel
			 $track->add_feature($feature);
             }
        }
	  #file for graphical representation
      open FH, ">genes.png" or die $!;
      print FH $panel->png;
      close FH;
      print "<img src='genes.png'/>";
	  
    }
   
} else {
	#default page
	print TOP();
	print create_html();
	print BOTTOM();
}
##subroutine for top html
sub TOP {
	return <<T;
<html>
	<head>
		<title>$_[0]</title>
	</head>
	<body>
T
}
##subroutine for bottom HTML
sub BOTTOM {
	return <<B;
		</body>
</html>
B
}
##HTML page that will take user information to process 
sub create_html {
	my $html = "";
	my $start = shift;
    my $end = shift;
	my $chromosome = shift;
	
	$html .= <<PRINT;
		<form action="$0" method="get">
        <br>
		<h1 align= "center"> BIF724 Assignment 3 </h1>
        <p align= "center"> <b> The purpose of this page is to extract desired ensembl data for marmoset (<i>Cllithrix jacchus</i>)<b> </p>
		<p> Examples showing how the page works and what it retrives </p>
		<p> 1. For chromosome 2 within the range 193472325 to 193872325 will give you 5 genes:- ROPN1L, MARCH6, CMBL, CCT5, FAM173B </p>
		<p> 2. For chromosome 5 within the range 100000000 to 100300000 will give you 3 genes:- MSI2, (no external name), AKAP1 </p>
		<p> 3. For chromosome 1 (default example) within range 4005000 to 5005000 will give you 5 genes. </p>
			<table width="700" border="0" cellpadding="0" cellspacing="0">
			<tr> 
			      <td align="right" width="20%">START: </td>
			      <td align="left" width="80%">
			      	<input type="text" name="start" value="4005000"/>
			      </td>
                  <td align="right" width="20%">END: </td>
			      <td align="left" width="80%">
			      	<input type="text" name="end" value="5005000"/>
			      </td>
			</tr>    
			<tr> 
			      <td align="right" width="10%">CHROMOSOME: </td>
			      <td align="left" width="90%"> 
			        <select name="chromosome"/>
					
PRINT
	my @chromosome = qw/1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X Y/;
	foreach (@chromosome) {
		my $sel = "";
		$sel = " selected='selected'" if ($chromosome eq "$_");
		$html .= "<option $sel>$_</option>";
	}
	
	$html .= <<PRINT;
			        </select>
			      </td>
			    </tr>
			    <tr> 
			      
			      <td align="left" width="80%">
PRINT
		
	$html .= <<PRINT;
			      </td>
			    </tr>
			   <tr>   
			</tr>    
			    <tr>
			      <td align="right" width="20%"> 
			        <input type="submit" name="Submit" value="Submit"/>
			      </td>
			      <td width="80%"> </td>
			    </tr>
			</table>
		</form>
PRINT
	return $html;
}


