import streamlit as st
import pandas as pd
import os

# --------------------
# 多语言字典
# --------------------
LANG = {
    "中文": {
        "title": "五位数号码推荐",
        "pool_total": "号码池总数：{n} 组",
        "filtered_remaining": "过滤顺序后剩余：{n} 组",
        "clear_history": "清空历史记录",
        "history_cleared": "历史记录已清空，请刷新页面",
        "no_available": "没有可选号码！",
        "first_digit_filter": "首位数字筛选（可多选）",
        "first_digit_filter_label": "选择首位数字",
        "big_small_filter": "首位数字大小单双筛选",
        "big_small_label": "大小",
        "odd_even_label": "单双",
        "filtered_count": "筛选后剩余：{n} 组",
        "no_filtered": "筛选后没有可选号码！",
        "all_numbers": "所有可选号码",
        "generate_count_label": "生成多少注号码",
        "generate_button": "生成推荐号码",
        "selection_title": "推荐号码：",
        "history_saved": "已保存到历史记录"
    },
    "English": {
        "title": "5-Digit Number Recommendation",
        "pool_total": "Total pool: {n} numbers",
        "filtered_remaining": "After filtering sequential numbers: {n} numbers",
        "clear_history": "Clear history",
        "history_cleared": "History cleared, please refresh",
        "no_available": "No available numbers!",
        "first_digit_filter": "First Digit Filter (Multiple select)",
        "first_digit_filter_label": "Select first digit",
        "big_small_filter": "First Digit Big/Small & Odd/Even Filter",
        "big_small_label": "Big/Small",
        "odd_even_label": "Odd/Even",
        "filtered_count": "After filtering: {n} numbers",
        "no_filtered": "No numbers available after filtering!",
        "all_numbers": "All available numbers",
        "generate_count_label": "How many numbers to generate",
        "generate_button": "Generate recommended numbers",
        "selection_title": "Recommended numbers:",
        "history_saved": "Saved to history"
    },
    "ລາວ": {  # 老挝文
        "title": "ແນະນຳຕົວເລກ 5 ໂຕ",
        "pool_total": "ຈຳນວນຕົວເລກໃນຖານ: {n}",
        "filtered_remaining": "ຫຼັງການກອງຕົວຕໍ່ຊ້ຳ: {n}",
        "clear_history": "ລ້າງປະຫວັດ",
        "history_cleared": "ປະຫວັດຖືກລ້າງແລ້ວ, ກະລຸນາປັບໃໝ່",
        "no_available": "ບໍ່ມີຕົວເລກທີ່ເລືອກໄດ້!",
        "first_digit_filter": "ການກອງຕົວເລກຫຼັກແລກ (ເລືອກໄດ້ຫຼາຍຕົວ)",
        "first_digit_filter_label": "ເລືອກຕົວເລກຫຼັກ",
        "big_small_filter": "ການກອງຕົວເລກຫຼັກ ໃຫຍ່/ນ້ອຍ & ຄີ/ຄິດ",
        "big_small_label": "ໃຫຍ່/ນ້ອຍ",
        "odd_even_label": "ຄີ/ຄິດ",
        "filtered_count": "ຫຼັງການກອງ: {n} ຕົວ",
        "no_filtered": "ຫຼັງການກອງບໍ່ມີຕົວເລກ!",
        "all_numbers": "ຕົວເລກທີ່ເລືອກໄດ້ທັງໝົດ",
        "generate_count_label": "ຈຳນວນທີ່ຈະສ້າງ",
        "generate_button": "ສ້າງຕົວເລກແນະນຳ",
        "selection_title": "ຕົວເລກແນະນຳ:"
    },
    "ไทย": {  # 泰文
        "title": "แนะนำเลข 5 หลัก",
        "pool_total": "จำนวนเลขทั้งหมด: {n}",
        "filtered_remaining": "หลังกรองลำดับตัวเลข: {n}",
        "clear_history": "ล้างประวัติ",
        "history_cleared": "ล้างประวัติเรียบร้อยแล้ว กรุณารีเฟรช",
        "no_available": "ไม่มีตัวเลขให้เลือก!",
        "first_digit_filter": "กรองเลขหลักแรก (เลือกหลายตัวได้)",
        "first_digit_filter_label": "เลือกเลขหลักแรก",
        "big_small_filter": "กรองเลขหลักแรก ขนาด / คี่-คู่",
        "big_small_label": "ใหญ่/เล็ก",
        "odd_even_label": "คี่/คู่",
        "filtered_count": "หลังกรอง: {n} ตัว",
        "no_filtered": "ไม่มีตัวเลขหลังกรอง!",
        "all_numbers": "ตัวเลขทั้งหมดที่สามารถเลือกได้",
        "generate_count_label": "จำนวนตัวเลขที่ต้องการสร้าง",
        "generate_button": "สร้างตัวเลขแนะนำ",
        "selection_title": "ตัวเลขแนะนำ:"
    }
}

# --------------------
# 页面顶部语言选择
# --------------------
lang_choice = st.selectbox("选择语言 / Select Language / ເລືອກພາສາ / เลือกภาษา", list(LANG.keys()))
T = LANG[lang_choice]

st.title(T["title"])

# -------------------
# 读取号码池
# -------------------
POOL_FILE = "favorite_patterns_pool.csv"
HISTORY_FILE = "history_selected.csv"

if not os.path.exists(POOL_FILE):
    st.error(f"{POOL_FILE} 不存在，请先生成！")
    st.stop()

pool_df = pd.read_csv(POOL_FILE, dtype=str, header=None, names=["number"])
pool_df["number"] = pool_df["number"].str.zfill(5)

# -------------------
# 读取历史记录
# -------------------
if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
    history_df = pd.read_csv(HISTORY_FILE, dtype=str)
else:
    history_df = pd.DataFrame(columns=["number"])

# -------------------
# 顺序过滤
# -------------------
def is_sequential(s):
    digits = [int(c) for c in s]
    return (digits[1]-digits[0]==1 and digits[2]-digits[1]==1) or \
           (digits[1]-digits[0]==-1 and digits[2]-digits[1]==-1)

def filter_numbers(df):
    result = []
    for num in df["number"]:
        if is_sequential(num[:3]) or is_sequential(num[1:4]) or is_sequential(num[2:]):
            continue
        result.append(num)
    return pd.DataFrame(result, columns=["number"])

available_df = pool_df[~pool_df["number"].isin(history_df["number"])]
filtered_df = filter_numbers(available_df)

# -------------------
# 页面布局
# -------------------
st.write(T["pool_total"].format(n=len(pool_df)))
st.write(T["filtered_remaining"].format(n=len(filtered_df)))

# 清空历史记录按钮
if st.button(T["clear_history"]):
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    history_df = pd.DataFrame(columns=["number"])
    st.success(T["history_cleared"])
    st.stop()

if len(filtered_df) == 0:
    st.warning(T["no_available"])
    st.stop()

# -------------------
# 用户筛选选项
# -------------------
st.subheader(T["first_digit_filter"])
start_digits = st.multiselect(T["first_digit_filter_label"], options=[str(i) for i in range(10)],
                              default=[str(i) for i in range(10)])

st.subheader(T["big_small_filter"])
big_small = st.multiselect(T["big_small_label"], options=["大","小"], default=["大","小"])
odd_even = st.multiselect(T["odd_even_label"], options=["单","双"], default=["单","双"])

# -------------------
# 应用筛选
# -------------------
def apply_filters(df):
    result = []
    for num in df["number"]:
        first_digit = int(num[0])
        if num[0] not in start_digits:
            continue
        if first_digit >= 5 and "大" not in big_small:
            continue
        if first_digit <= 4 and "小" not in big_small:
            continue
        if first_digit % 2 == 0 and "双" not in odd_even:
            continue
        if first_digit % 2 == 1 and "单" not in odd_even:
            continue
        result.append(num)
    return pd.DataFrame(result, columns=["number"])

filtered_df = apply_filters(filtered_df)
st.write(T["filtered_count"].format(n=len(filtered_df)))

if len(filtered_df) == 0:
    st.warning(T["no_filtered"])
    st.stop()

# -------------------
# 显示可选号码
# -------------------
st.subheader(T["all_numbers"])
st.dataframe(filtered_df)

# -------------------
# 用户输入生成数量
# -------------------
count = st.number_input(T["generate_count_label"], min_value=1, max_value=len(filtered_df), value=5, step=1)

# -------------------
# 生成推荐号码
# -------------------
if st.button(T["generate_button"]):
    selection = filtered_df.sample(n=min(count,len(filtered_df)), replace=False).reset_index(drop=True)
    st.write(T["selection_title"])
    st.dataframe(selection)
    updated_history = pd.concat([history_df, selection], ignore_index=True)
    updated_history.to_csv(HISTORY_FILE, index=False)
    st.success(T["history_saved"])
