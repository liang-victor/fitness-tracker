from lxml import etree
import os
NS = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}


def tcx_distance_scaler(tcx_file_path, correct_final_distance):
    """Scales distance in a .tcx file by a common factor for each measurement

    When a fitness tracker uses distance estimates from the pedometer, it can be off if stride distance is not accurate.
    By entering the known final distance, a scaling factor is determined and applied to all measurements in the file.
    """

    with open(tcx_file_path) as f:
        tcx_file = etree.parse(f)

    scaling_factor = calculate_scaling_factor(tcx_file, correct_final_distance)
    modify_trackpoints(tcx_file, scaling_factor)
    tcx_file.write(update_filename(tcx_file_path),
                   xml_declaration=True, encoding='UTF-8')


def calculate_scaling_factor(tcx_file, correct_final_distance):
    measured_distance = float(tcx_file.find(
        './tcx:Activities/tcx:Activity/tcx:Lap/tcx:DistanceMeters', NS))
    return measured_distance/correct_final_distance


def modify_trackpoints(tcx_file, scaling_factor):
    track = tcx_file.find(
        './tcx:Activities/tcx:Activity/tcx:Lap/tcx:Track', NS)
    for distance_m in track.iterfind('./tcx:Trackpoint/tcx:DistanceMeters', NS):
        distance_m.text = str(float(distance_m.text)/scaling_factor)


def update_filename(tcx_file_path):
    name, ext = os.path.splitext(tcx_file_path)
    return f'{name}_fixed{ext}'
