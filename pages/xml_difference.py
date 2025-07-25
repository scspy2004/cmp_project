import pandas as pd
import streamlit as st
import numpy as np
import xml.etree.ElementTree as ET


st.set_page_config(layout="wide")


compare_type = st.selectbox('Data 비교 방식: ', ['--선택--', '전체 Data 중 차이점 비교', '특정 Data 2가지 선택하여 비교'])


def find_children_by_tag(xml_dir, tag):
    tree = ET.parse(xml_dir)
    root = tree.getroot()
    children = root.findall(f'.//{tag}')
    return children

children = find_children_by_tag('data/sample.xml', 'Measurements')
dict1 = {}
for child in children:
    name = child.attrib['name']
    data = []
    for g_child in child:
        row = {}
        for gg_child in g_child:
            row[gg_child.tag] = gg_child.text
        data.append(row)
    df = pd.DataFrame(data)
    dict1[name] = df

children = find_children_by_tag('data/sample2.xml', 'Measurements')
dict2 = {}
for child in children:
    name = child.attrib['name']
    data = []
    for g_child in child:
        row = {}
        for gg_child in g_child:
            row[gg_child.tag] = gg_child.text
        data.append(row)
    df = pd.DataFrame(data)
    dict2[name] = df


dicts = [dict1, dict2]


def df_reindex_and_diff(df1, df2, index_column):
    df1_id_index = df1.set_index('ID')
    df2_id_index = df2.set_index('ID')

    all_indices = df1_id_index.index.union(df2_id_index.index)

    df1_reindexed = df1_id_index.reindex(all_indices).reset_index()
    df2_reindexed = df2_id_index.reindex(all_indices).reset_index()

    df1 = df1_reindexed
    df2 = df2_reindexed

    diff_mask = df1 != df2
    diff_row_indices = diff_mask.any(axis=1)
    diff_mask_filtered = diff_mask[diff_row_indices]
    return df1, df2, diff_row_indices, diff_mask, diff_mask_filtered


def highlight_diff(data, mask):
    return pd.DataFrame(np.where(mask, 'background-color: rgb(255, 191, 191); font-weight: bold', ''), index=data.index, columns=data.columns)


style_css = """
<style>
table { border-collapse: collapse; }
th:nth-child(1), td:nth-child(1) { width: 25px; }
th:nth-child(2), td:nth-child(2) { width: 25px; }
th:nth-child(3), td:nth-child(3) { width: 100px; }
th, td { border: 1px solid #ddd; padding: 4px; text-align: center; }
</style>
"""

if compare_type == '전체 Data 중 차이점 비교':
    measurement_names = list(set(list(dict1.keys()) + list(dict2.keys())))
    measurement_names.sort()

    for measurement_name in measurement_names:
        st.write(f'Data Name: {measurement_name}')
        cols = st.columns(2)
        dfs = [dict1.get(measurement_name), dict2.get(measurement_name)]
        if dfs[0] is None or dfs[1] is None:
            for i, df in enumerate(dfs):
                with cols[i]:
                    if df is None:
                        st.write('해당되는 Data가 없습니다.')
                    else:
                        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
            continue
        
        dfs[0], dfs[1], diff_row_indices, diff_mask, diff_mask_filtered = df_reindex_and_diff(dfs[0], dfs[1], 'ID')
        if diff_mask_filtered.empty:
            st.write('Data가 동일합니다.')
            continue
        for i, df in enumerate(dfs):
            with cols[i]:
                styled_df = df[diff_row_indices].style.apply(highlight_diff, mask=diff_mask_filtered, axis=None)
                styled_df_html = styled_df.hide(axis="index").to_html(escape=False)
                st.markdown(styled_df_html, unsafe_allow_html=True)
elif compare_type == '특정 Data 2가지 선택하여 비교':
    cols = st.columns(2)
    dfs = []
    for i in range(2):
        with cols[i]:
            dict_selected = st.selectbox('dict: ', ['dict1', 'dict2'], key=f'dict_selectbox_{str(i)}')
            if dict_selected == 'dict1':
                dict = dicts[0]
            elif dict_selected == 'dict2':
                dict = dicts[1]
            measurement_names = list(dict.keys())
            measurement_name = st.selectbox('Data Name: ', measurement_names, key=f'data_selectbox_{str(i)}')
            dfs.append(dict[measurement_name])

    dfs[0], dfs[1], _, diff_mask, _ = df_reindex_and_diff(dfs[0], dfs[1], 'ID')
    cols = st.columns(2)
    for i, df in enumerate(dfs):
        with cols[i]:
            if not diff_mask.empty:
                styled_df = df.style.apply(highlight_diff, mask=diff_mask, axis=None)
                styled_df_html = styled_df.hide(axis="index").to_html(escape=False)
            else:
                styled_df = df
                styled_df_html = styled_df.to_html(escape=False)
            st.markdown(styled_df_html, unsafe_allow_html=True)

