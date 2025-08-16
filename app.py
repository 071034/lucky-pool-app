import streamlit as st
import pandas as pd
import os

# 文件路径
POOL_FILE = "favorite_patterns_pool.csv"
HISTORY_FILE = "history_selected.csv"

# -------------------
# 读取号码池
# -------------------
if not os.path.exists(POOL_FILE):
    st.error(f"号码池文件 {POOL_FILE} 不存在，请先生成！")
    st.stop()

pool_df = pd.read_csv(POOL_FILE, dtype=str, header=None, names=["number"])
pool_df["number"] = pool_df["number"].str.zfill(5)

# -------------------
# 读取历史记录（容错）
# -------------------
if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
    history_df = pd.read_csv(HISTORY_FILE, dtype=str)
else:
    history_df = pd.DataFrame(columns=["number"])

# -------------------
# 过滤顺序规则
# -------------------
def is_sequential(s):
    digits = [int(c) for c in s]
    return (digits[1] - digits[0] == 1 and digits[2] - digits[1] == 1) or \
           (digits[1] - digits[0] == -1 and digits[2] - digits[1] == -1)

def filter_numbers(df):
    result = []
    for num in df["number"]:
        if is_sequential(num[:3]):  # 前三位
            continue
        if is_sequential(num[1:4]):  # 中三位
            continue
        if is_sequential(num[2:]):  # 后三位
            continue
        result.append(num)
    return pd.DataFrame(result, columns=["number"])

# -------------------
# 去掉历史已选号码并初步过滤
# -------------------
available_df = pool_df[~pool_df["number"].isin(history_df["number"])]
filtered_df = filter_numbers(available_df)

# -------------------
# 页面布局
# -------------------
st.title("五位数号码推荐")

st.write(f"号码池总数：{len(pool_df)} 组")
st.write(f"过滤顺序后剩余：{len(filtered_df)} 组")

# 清空历史记录按钮
if st.button("清空历史记录"):
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    history_df = pd.DataFrame(columns=["number"])
    st.success("历史记录已清空，请刷新页面")
    st.stop()

if len(filtered_df) == 0:
    st.warning("没有可选号码！")
    st.stop()

# -------------------
# 用户筛选选项
# -------------------
st.subheader("首位数字筛选（可多选）")
start_digits = st.multiselect("选择首位数字", options=[str(i) for i in range(10)], default=[str(i) for i in range(10)])

st.subheader("首位数字大小单双筛选")
big_small = st.multiselect("大小", options=["大", "小"], default=["大","小"])
odd_even = st.multiselect("单双", options=["单","双"], default=["单","双"])

# -------------------
# 应用首位数字筛选 + 首位数字大小单双
# -------------------
def apply_filters(df):
    result = []
    for num in df["number"]:
        first_digit = int(num[0])
        # 首位数字是否在选择列表
        if num[0] not in start_digits:
            continue
        # 首位大小判断
        if first_digit >= 5 and "大" not in big_small:
            continue
        if first_digit <= 4 and "小" not in big_small:
            continue
        # 首位单双判断
        if first_digit % 2 == 0 and "双" not in odd_even:
            continue
        if first_digit % 2 == 1 and "单" not in odd_even:
            continue
        result.append(num)
    return pd.DataFrame(result, columns=["number"])

filtered_df = apply_filters(filtered_df)
st.write(f"筛选后剩余：{len(filtered_df)} 组")

if len(filtered_df) == 0:
    st.warning("筛选后没有可选号码！")
    st.stop()

# -------------------
# 显示所有可选号码（便于参考）
# -------------------
st.subheader("所有可选号码")
st.dataframe(filtered_df)

# -------------------
# 用户输入生成数量
# -------------------
count = st.number_input("生成多少注号码", min_value=1, max_value=len(filtered_df), value=5, step=1)

# -------------------
# 生成按钮
# -------------------
if st.button("生成推荐号码"):
    selection = filtered_df.sample(n=min(count, len(filtered_df)), replace=False).reset_index(drop=True)
    st.write("推荐号码：")
    st.dataframe(selection)

    # 追加到历史记录
    updated_history = pd.concat([history_df, selection], ignore_index=True)
    updated_history.to_csv(HISTORY_FILE, index=False)
    st.success("已保存到历史记录")
