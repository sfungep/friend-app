import streamlit as st
import json

st.set_page_config(page_title="我的私人朋友筆記", page_icon="💾")

# --- 初始化：暫存清單 ---
if 'my_friends' not in st.session_state:
    st.session_state['my_friends'] = []

# --- 側邊欄：檔案管理 ---
st.sidebar.title("📁 存檔與讀檔")

uploaded_file = st.sidebar.file_uploader("選取你的筆記檔 (.json)", type="json")
if uploaded_file is not None:
    # 只有在 session 為空時才自動載入，避免覆蓋正在編輯的內容
    if not st.session_state['my_friends']:
        st.session_state['my_friends'] = json.load(uploaded_file)
        st.sidebar.success("讀取成功！")

# 存檔按鈕
if st.session_state['my_friends']:
    json_data = json.dumps(st.session_state['my_friends'], ensure_ascii=False, indent=4)
    st.sidebar.download_button(
        label="📥 儲存並下載最新筆記",
        data=json_data,
        file_name="my_friend_notes.json",
        mime="application/json"
    )

# --- 主要顯示區 ---
st.title("💾 我的私人朋友筆記")
tab1, tab2 = st.tabs(["👀 溫習與修改", "➕ 新增朋友"])

with tab2:
    st.subheader("記錄新發現")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("朋友的名字")
        ints = st.text_input("興趣")
        lks = st.text_area("喜歡")
        dlks = st.text_area("不喜歡")
        if st.form_submit_button("暫存到清單"):
            if name:
                new_entry = {"name": name, "interests": ints, "likes": lks, "dislikes": dlks}
                st.session_state['my_friends'].append(new_entry)
                st.success(f"已加入 {name}。記得按左側『儲存』下載檔案喔！")
                st.rerun()

with tab1:
    if not st.session_state['my_friends']:
        st.info("目前沒有資料。請讀取舊檔或新增朋友。")
    else:
        friend_names = [f["name"] for f in st.session_state['my_friends']]
        selected_idx = st.selectbox("你想看誰？", range(len(friend_names)), format_func=lambda x: friend_names[x])
        
        # 取得目前選中的朋友資料
        current_friend = st.session_state['my_friends'][selected_idx]

        # 顯示區
        st.markdown(f"### 👋 這是 **{current_friend['name']}**")
        
        # --- 修改與刪除區 (直接展開) ---
        with st.expander("🛠️ 修改或刪除資料"):
            new_name = st.text_input("名字", value=current_friend['name'])
            new_ints = st.text_input("興趣", value=current_friend['interests'])
            new_lks = st.text_area("喜歡", value=current_friend['likes'])
            new_dlks = st.text_area("不喜歡", value=current_friend['dislikes'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 確認修改"):
                    # 更新暫存清單中的資料
                    st.session_state['my_friends'][selected_idx] = {
                        "name": new_name, "interests": new_ints, "likes": new_lks, "dislikes": new_dlks
                    }
                    st.success("修改成功！記得按左側按鈕下載存檔。")
                    st.rerun()
            with col2:
                if st.button("🗑️ 刪除此人"):
                    st.session_state['my_friends'].pop(selected_idx)
                    st.warning("已從清單移除。記得下載新存檔以更新檔案。")
                    st.rerun()