PWBDIR="/data/project/shared/stable/"
EXECDIR="/data/project/wugbot/CovidGraphs/"

for LANG in en tr
do
	jsub python3 $PWBDIR"pwb.py" -lang:$LANG $EXECDIR"Ingest.py"
done
