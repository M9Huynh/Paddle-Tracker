import cv2
def make_slid(a_min:int, a_max:int, curr:int, slider_id:str, root_win_name:str, on_change_callback =lambda x :x):
    cv2.createTrackbar(slider_id,root_win_name,a_min,a_max,on_change_callback)
    cv2.setTrackbarPos(slider_id,root_win_name, curr)
    return slider_id

def getslid(ids, root_wind:str):
    try:
        results = [cv2.getTrackbarPos(idd, root_wind) for idd in ids]
        return results[0] if len(results) == 1 else results
    except Exception as e:
        print(f'Error in getting slider value - {str(e)}')
        return None
    
def setslid(id_:str, value:int, root_wind:str):
    cv2.setTrackbarPos(id_, root_wind, value)
    