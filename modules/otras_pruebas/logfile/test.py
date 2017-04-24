import logging,time

#logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
#						 datefmt='%d/%m/%Y %H:%M:%S')


logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('infoLog2.log')
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s",
                              "%d/%m/%Y-- %H:%M:%S")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info('captura corrupta 99')
logger.info('captura corrupta 100')




#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

#fecha = time.strftime("%d/%m/%Y %H:%M:%S RODRIGO")
#formatter = logging.Formatter(fecha +' %(levelname)s %(message)s')

#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr)
#logger.setLevel(logging.INFO)
#logger.info('captura corrupta 4')
#logger.info('captura corrupta 5')


#
#fecha = time.strftime("%d/%m/%Y %H:%M:%S RODRIGO")
#formatter = logging.Formatter(fecha +' %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr)
#logger.info('captura corrupta 9999')

