from django.http import JsonResponse
from . import pyqas
def SerliazeprofileData(main_data, profile_data_image) :
    lst_profile_images=[]
    for item in pyqas.Reverse_Lst(profile_data_image) :
        data={
            "src" :item[0],
            "id" :item[2]
        }
        lst_profile_images.append(data)
    objects={
        "name" :main_data[0],
        "email" :main_data[1],
        "phone" :main_data[2],
        "pio" :main_data[4],
        "profile_image_src" :profile_data_image[-1][0],
        "profile_image_id" :profile_data_image[-1][2],
        "profile_images" :lst_profile_images,
    }
    return JsonResponse(objects)