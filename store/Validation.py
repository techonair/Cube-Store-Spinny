from . models import Box
from store.constraints import A1, V1, L1, L2
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone

def check_validity(user, request, data, *argpk):

    for key in argpk:
        pk = key

    length = int(data["length"])
    width = int(data["width"])
    height = int(data["height"])

    new_area = 2*((length * width) + (width * height) + (height * length))
    new_volume = length * width * height
    total_number_of_boxes = Box.objects.all().count()
    sum_of_area_of_all_boxes = Box.objects.aggregate(Sum("area"))["area__sum"]
    sum_of_volume_of_boxes_created_by_user = Box.objects.filter(created_by=user).aggregate(Sum('volume'))["volume__sum"]
    
    if total_number_of_boxes == 0:
        return True

    # Request for creating box
    if request.method == "POST":
        if (sum_of_area_of_all_boxes+new_area)/total_number_of_boxes+1 > A1:
            return False
        if (int(sum_of_volume_of_boxes_created_by_user or 0)+new_volume)/total_number_of_boxes+1 > V1:
            return False

    # Request for updating box
    elif request.method == "PUT":
        area_of_requested_box = Box.objects.filter(id=pk).values("area")[0]["area"]
        
        if ((sum_of_area_of_all_boxes-area_of_requested_box)+new_area)/total_number_of_boxes > A1:
            return False
        """
        volume_of_requested_box = Box.objects.filter(id=pk).values("volume")[0]["volume"]

        if ((sum_of_volume_of_boxes_created_by_user-volume_of_requested_box)+new_volume)/total_number_of_boxes > V1:
            return False
        """
    
    datetime_one_week_ago = timezone.now().date() - timedelta(days=7)

    boxes_last_week = Box.objects.filter(created_on__gt=datetime_one_week_ago).count()
    if boxes_last_week+1 > L1:
        return False
    
    boxes_last_week_by_user = Box.objects.filter(created_by=user, created_on__gt=datetime_one_week_ago).count()
    if boxes_last_week_by_user+1 > L2:
        return False
    
    return True