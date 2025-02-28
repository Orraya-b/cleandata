import pandas as pd

# เก็บชื่อไฟล์
report_name="file2.csv"
dataset_file_name="VM_dataset.csv"

# อ่านไฟล์ที่เรากำหนดตัวแปรไว้ และดึงมาใช้
system_event = pd.read_csv(report_name)
dataset = pd.read_csv(dataset_file_name)


# เลือกเฉพาะแถวที่ต้องการ เช่น ค่าในคอลัมน์ "Status" เป็น "Pass"
start_complete_event = system_event[system_event["Event"].isin(["Scheduled Malware Scan Started", "Scheduled Malware Scan Completed"])]
error_event = system_event[system_event["Event ID"].isin([736, 737])]

# บันทึกไฟล์ Excel ใหม่ คือ data ที่ถูก clean เลือกเฉพาะที่ต้องการแล้ว
start_complete_event.to_csv("data_filtered_start_complete_event.csv", index=False)
error_event.to_csv("data_filtered_error.csv", index=False)

# เลือกค่าใน "Category" ที่พบแค่ครั้งเดียว
unique_only = start_complete_event["Target"].value_counts()
unique_only = unique_only[unique_only == 1].index

# กรองเฉพาะแถวที่มีค่าพบเพียงครั้งเดียว หรือตัวที่ทำงานตาม task start complete ไม่สมบูรณ์
system_event_unique_only = start_complete_event[start_complete_event["Target"].isin(unique_only)]
# ปริ้นออกมาเป็นไฟล์ excel เป็นเครื่องที่ทำงานไม่สมบูรณ์ตาม task
system_event_unique_only.to_csv("data_unique_only.csv", index=False)

# เปรียบเทียบค่าที่แตกต่างกัน 2 ไฟล์ ในคอลัมน์ที่ต่างกันด้วย
missing_VM = dataset[~dataset["Name"].isin(start_complete_event["Target"])]

# แสดงผลลัพธ์
# print(missing_VM)

# บันทึกค่าที่แตกต่างกันระหว่าง 2 ไฟล์ไปยังไฟล์ใหม่
missing_VM.to_csv("difference.csv", index=False)


