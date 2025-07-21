import pandas as pd
import streamlit as st
import numpy as np


df1 = pd.read_xml('data/sample.xml')
df2 = pd.read_xml('data/sample2.xml')

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


cols = st.columns(2)
for i, df in enumerate([df1, df2]):
    with cols[i]:
        styled_df = df[diff_row_indices].style.apply(highlight_diff, mask=diff_mask_filtered, axis=None)
        styled_df_html = styled_df.hide(axis="index").to_html(escape=False)
        # st.dataframe(styled_df, use_container_width=True)
        st.markdown(styled_df_html + style_css, unsafe_allow_html=True)

