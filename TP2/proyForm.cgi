#!/usr/bin/perl -w

use CGI;
my $q = new CGI;

if(!$q->param) {
    print $q->header(-charset => 'utf-8');

    print $q->start_html(-title => 'Formulario');
    print $q->start_form(
        -name    => 'main_form',
        -method  => 'GET',
        -enctype => &CGI::URL_ENCODED,
        -onsubmit => 'return javascript:validation_function()',
    );
    print "<div class=\"bodymain\" align=\"center\">\n";
    print $q->h2({-style=>"color:navy"},'Por favor indícanos tu nombre:');
    print $q->textfield(
        -name      => 'Nombre',
        -value     => 'Introduce tu nombre',
        -size      => 20,
        -maxlength => 30,
    );
    print $q->h2({-style=>"color:navy"},'Por favor indícanos tus apellidos:');
    print $q->textfield(
        -name      => 'Apellido',
        -value     => 'Introduce tus apellidos',
        -size      => 20,
        -maxlength => 30,
    );
    print $q->h2({-style=>"color:navy"},'Por favor indícanos tu Localidad:');
    print $q->textfield(
        -name      => 'Localidad',
        -value     => 'Introduce tu Localidad',
        -size      => 20,
        -maxlength => 30,
    );

    print $q->h2({-style=>"color:navy"},'¿Cuáles son tus deportes favoritos?');
    print $q->checkbox_group(
        -name     => 'deportes',
        -values   => ['Fútbol', 'Baloncesto', 'Balonmano', 'Tenis', 'Fútbol Americano', 'Béisbol','Voleibol','Snooker','Pádel'],
        -defaults => ['Baloncesto', 'Fútbol'],
        -columns  => 3,
        -rows     => 3,
    );

    print $q->h2({-style=>"color:navy"},'¿Cuál es tu equipo favorito?');
    print $q->radio_group(
        -name     => 'Favorito',
        -values   => ['Sevilla FC', 'New York Knicks', 'LA Lakers', 'Arsenal FC', 'TAU Cerámica', 'Denver Nuggets','Chelsea','Joventud','FC Bayern'],
        -defaults => 'Sevilla FC',
        -columns  => 3,
        -rows     => 3,
    );

    print $q->h2({-style=>"color:navy"},'Indicanos algunas sugerencias:');
    print $q->textarea(
        -name  => 'textarea1',
        -value => 'Escriba aquí sus sugerencias',
        -cols  => 60,
        -rows  => 3,
    );

    print ("<br>");
    print ("<br>");
    print ("<br>");

    print 'Aquí puedes añadir un archivo de texto acerca de este tema:*    ',
          $q->filefield(
              -name      => 'filename',
          -size      => 40,
          -maxlength => 80);
    print $q->hr;
    print $q->submit(-value => 'Enviar');
    print $q->reset(-value => 'Borrar');
    print $q->hr;
    print "</div>";

    if (!$q->param('filename') && $q->cgi_error()) {
        print $q->cgi_error();
        print "El archivo que intenta subir es demasiado grande";
        print $q->hr;
        exit 0;
    }
    save_file($q);

    print $q->end_html;
    exit 0;


    #
    print $q->end_form;
    print $q->end_html;
}
else {

    print $q->header(-charset => 'utf-8');
    print $q->start_html(-title => 'Formulario');
    print $q->h3({-style=>"color:navy"},'¡Gracias por rellenar el formulario!');
    @vg = $q->param('deportes');
    print $q->h2({-style=>"color:navy"},"Hola , " . $q->param('Nombre') . " " . $q->param('Apellido') . " residente en " . $q->param('Localidad') . ", ha informado, que sus deportes favoritos son: ");
    foreach $deportes (@vg) {
        print (" ► " . $deportes);
        print ("<br>");
    }
    print $q->h2({-style=>"color:navy"}," y su equipo favorito de nuestra lista es " . $q->param('Favorito'));
    print $q->end_html;

 sub save_file($) {

        my ($q) = @_;
        my ($bytesread, $buffer);
        my $num_bytes = 1024;
        my $totalbytes;
        my $filename = $q->upload('filename');
        my $untainted_filename;

        if (!$filename) {
            print $q->h5({-style=>"color:darkred"},'*Debes añadir un archivo antes de enviar el formulario');
        return;
        }

        # Untaint $filename

        if ($filename =~ /^([-\@:\/\\\w.]+)$/) {
            $untainted_filename = $1;
        } else {
            die;
        }

        if ($untainted_filename =~ m/\.\./) {
            die;
        }

        my $file = "/tmp/$untainted_filename";

        print "Subiendo $filename a $file<BR>";

        open (OUTFILE, ">", "$file") or die "Couldn't open $file for writing: $!";

        while ($bytesread = read($filename, $buffer, $num_bytes)) {
            $totalbytes += $bytesread;
            print OUTFILE $buffer;
        }
        die "Read failure" unless defined($bytesread);
        unless (defined($totalbytes)) {
            print "<p>Error: No se ha podido leer el archivo ${untainted_filename}, ";
            print "o el archivo no tenía contenido.";
        } else {
            print "<p>Archivo $filename subido a $file ($totalbytes bytes)";
        }
        close OUTFILE or die "No se ha podido cerrar $file: $!";
    };
   }