#Set-Location "..\db_backup";

$dumpExe =  "mongodump.exe";

& $dumpExe --host 'localhost:27017' -u 'adminemiko' -p 'KIBASSA13MALIBA' --authenticationDatabase 'admin' -d cinebot