from openpyxl import Workbook

def generate_excel(total_time, multi_face, audio_count, movement_count):
    wb = Workbook()
    ws = wb.active
    ws.title = "Interview Report"

    ws.append(["Metric", "Value"])
    ws.append(["Total Time In Sec", total_time])
    ws.append(["Multiple Faces", multi_face])
    ws.append(["Multiple Audio", audio_count])
    ws.append(["Suspicious Movement", movement_count])

    wb.save("Interview_Report_Files.xlsx")
