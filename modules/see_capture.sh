#!/bin/sh
#Modo de ejecucion
#see_capture.sh /home/rodrigo/TESINA-2016-KINECT/appCliente/modules/14-02-2016/grietas GRIETA_DOS_1.pcd
#Primer argumento el dir de captura, segundo la captura pcd.
#cd $1
#pcl_viewer $2
#cd -

#V2. pcl_viewer /home/rodrigo/TESINA-2016-KINECT/appCliente-RGB NO FUNCIONAL-23-01-2017/nuevitaaaa_1.pcd
echo "Invocando a pcl_viewer con parametro "
VAR=""
I=0
for i in "$@"; do
  if [$I -gt 0]; then
  	VAR="$VAR $i";
  fi
  I="$I+1"
done

COMANDO='"'"$VAR"'"'
echo $COMANDO
pcl_viewer $COMANDO