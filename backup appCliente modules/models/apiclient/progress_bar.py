# -*- coding: utf-8 -*-
# ############################################################################
# This example demonstrates how to use the MultipartEncoderMonitor to create a
# progress bar using clint.
# ############################################################################
from clint.textui.progress import Bar as ProgressBar
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import requests


# https://gitlab.com/sigmavirus24/toolbelt/blob/master/examples/monitor/progress_bar.py

# def create_callback(encoder):
#     # encoder_len = len(encoder)
#     encoder_len = encoder.len
#     bar = ProgressBar(expected_size=encoder_len, filled_char='=')
#     def callback(monitor):
#         bar.show(monitor.bytes_read)
#     return callback


# Retorna el codificador que sube el archivo.
def create_upload():
    return MultipartEncoder({
        'id': 15,
        'nombre': 'Rodrigo',
        'archivo_captura_1': ('foo1.csv', open(__file__, 'rb'),
                                'application/octet-stream'),
        })


encoder = create_upload()    
encoder_len = encoder.len
bar = ProgressBar(expected_size=encoder_len, filled_char='=')

def callback(monitor):
    bar.show(monitor.bytes_read)
    print "monitor.bytes_read: %s" % monitor.bytes_read
    print "-----------------------------------------"
    

if __name__ == '__main__':
    # callback = create_callback(encoder)
    monitor = MultipartEncoderMonitor(encoder, callback)
    print "monitor.content_type: %s" % monitor.content_type
    print ""
    # r = requests.post('https://httpbin.org/post', data=monitor,
    #                   headers={'Content-Type': monitor.content_type})
    r = requests.post('http://localhost/repoProyectoBacheo/web/restapi/upload_pcd/format/json', data=monitor,
                      headers={'Content-Type': monitor.content_type})

    print('\nUpload finished! (Returned status {0} {1})'.format(
        r.status_code, r.reason
        ))