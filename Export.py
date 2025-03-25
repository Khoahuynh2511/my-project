import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="NMV Automation Dashboard", layout="wide")
st.title("📊 NMV Automation Dashboard for TTS & SHP")

# Upload file Excel đã gộp
uploaded_file = st.file_uploader("📂 Tải lên file Excel đã gộp (gồm sheet TTS và SHP)", type=["xlsx"])

# Hàm sinh bảng và biểu đồ tròn
def create_pie_chart(df, group_col, value_col, title):
    grouped = df.groupby(group_col)[value_col].sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(grouped[value_col], labels=grouped[group_col], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title(title)
    return grouped, fig

# Nếu có file upload
if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    df_tts = xls.parse("TTS")
    df_shp = xls.parse("SHP")

    # 1 & 2. NMV theo Creator Segment
    st.header("📌 1 & 2. NMV theo Creator Segment")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("TTS")
        tts_seg, fig1 = create_pie_chart(df_tts, "Creator Segment", "NMV Affiliate", "TTS - NMV by Creator Segment")
        st.dataframe(tts_seg)
        st.pyplot(fig1)

    with col2:
        st.subheader("SHP")
        shp_seg, fig2 = create_pie_chart(df_shp, "Creator Segment", "NMV Affiliate", "SHP - NMV by Creator Segment")
        st.dataframe(shp_seg)
        st.pyplot(fig2)

    # 3 & 4. Top 10 Creators by NMV
    st.header("📌 3 & 4. Top 10 Creators by NMV")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("TTS - Top 10 Creators")
        top10_tts = df_tts.groupby("Creator")["NMV Affiliate"].sum().sort_values(ascending=False).head(10).reset_index()
        fig3, ax3 = plt.subplots()
        ax3.pie(top10_tts["NMV Affiliate"], labels=top10_tts["Creator"], autopct='%1.1f%%', startangle=90)
        ax3.axis('equal')
        ax3.set_title("TTS - Top 10 Creators")
        st.dataframe(top10_tts)
        st.pyplot(fig3)

    with col4:
        st.subheader("SHP - Top 10 Creators")
        top10_shp = df_shp.groupby("Creator")["NMV Affiliate"].sum().sort_values(ascending=False).head(10).reset_index()
        fig4, ax4 = plt.subplots()
        ax4.pie(top10_shp["NMV Affiliate"], labels=top10_shp["Creator"], autopct='%1.1f%%', startangle=90)
        ax4.axis('equal')
        ax4.set_title("SHP - Top 10 Creators")
        st.dataframe(top10_shp)
        st.pyplot(fig4)

    # 5 & 6. NMV theo loại kế hoạch (Platform Plan)
    st.header("📌 5 & 6. NMV theo loại kế hoạch (Platform Plan)")
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("TTS - Platform Plan")
        tts_plan, fig5 = create_pie_chart(df_tts, "Plan", "NMV Affiliate", "TTS - Platform Plan")
        st.dataframe(tts_plan)
        st.pyplot(fig5)

    with col6:
        st.subheader("SHP - Platform Plan")
        shp_plan, fig6 = create_pie_chart(df_shp, "Plan", "NMV Affiliate", "SHP - Platform Plan")
        st.dataframe(shp_plan)
        st.pyplot(fig6)

    # 7. So sánh tổng NMV TTS vs SHP
    st.header("📌 7. So sánh tổng NMV giữa TTS và SHP")
    total_tts = df_tts["NMV Affiliate"].sum()
    total_shp = df_shp["NMV Affiliate"].sum()
    total_df = pd.DataFrame({
        "Platform": ["TTS", "SHP"],
        "NMV Affiliate": [total_tts, total_shp]
    })

    fig7, ax7 = plt.subplots()
    ax7.pie(total_df["NMV Affiliate"], labels=total_df["Platform"], autopct='%1.1f%%', startangle=90)
    ax7.axis('equal')
    ax7.set_title("TTS vs SHP - Tổng NMV")
    st.dataframe(total_df)
    st.pyplot(fig7)

    # Export bảng ra file Excel
    st.header("📥 Tải xuống file tổng hợp")
    export_buffer = io.BytesIO()
    with pd.ExcelWriter(export_buffer, engine="openpyxl") as writer:
        tts_seg.to_excel(writer, sheet_name="TTS - Segment", index=False)
        shp_seg.to_excel(writer, sheet_name="SHP - Segment", index=False)
        top10_tts.to_excel(writer, sheet_name="TTS - Top 10", index=False)
        top10_shp.to_excel(writer, sheet_name="SHP - Top 10", index=False)
        tts_plan.to_excel(writer, sheet_name="TTS - Platform", index=False)
        shp_plan.to_excel(writer, sheet_name="SHP - Platform", index=False)
        total_df.to_excel(writer, sheet_name="Compare NMV", index=False)

    st.download_button(
        label="⬇️ Tải file Excel tổng hợp",
        data=export_buffer.getvalue(),
        file_name="NMV_Affiliate_Summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
