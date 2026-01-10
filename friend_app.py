import streamlit as st
import json

# 1. 頁面設定
st.set_page_config(page_title="我的私人朋友筆記", page_icon="💾")

# 2. 初始化暫存區
if 'my_friends' not in st.session_state:
    st.session_state['my_friends'] = []

# --- 側邊欄：檔案管理 ---
st.sidebar.title("📁 存檔與讀檔")
uploaded_file = st.sidebar.file_uploader("選取你的筆記檔 (.json)", type="json")

# 讀取檔案邏輯
if uploaded_file is not None and len(st.session_state['my_friends']) == 0:
    st.session_state['my_friends'] = json.load(uploaded_file)
    st.sidebar.success("讀取成功！")

# --- 主要顯示區 ---
st.title("💾 我的私人朋友筆記")
tab1, tab2 = st.tabs(["👀 溫習與社交貼士", "➕ 新增朋友"])

with tab2:
    st.subheader("記錄新發現")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("朋友的名字")
        ints = st.text_input("他的興趣")
        lks = st.text_area("他喜歡的東西")
        dlks = st.text_area("他不喜歡/害怕的事")
        if st.form_submit_button("暫存到清單"):
            if name:
                new_entry = {"name": name, "interests": ints, "likes": lks, "dislikes": dlks}
                st.session_state['my_friends'].append(new_entry)
                st.success(f"已加入 {name}。別忘了在下方下載存檔！")
                st.rerun()

with tab1:
    current_list = st.session_state.get('my_friends', [])
    if not current_list:
        st.info("目前沒有資料。請讀取舊檔或新增朋友。")
    else:
        friend_names = [f["name"] for f in current_list]
        selected_idx = st.selectbox("你想見誰？", range(len(friend_names)), format_func=lambda x: friend_names[x])
        f = current_list[selected_idx]

        # --- 社交貼士展示 ---
        st.subheader(f"💡 與 {f['name']} 的交際錦囊")
        st.info(f"✅ **你可以試著這樣開始話題：**\n\n「聽說你對 **{f['interests']}** 很有研究，可以跟我分享嗎？」")
        
        if f['dislikes']:
            st.warning(f"⚠️ **避雷提醒：** 盡量不要提到：**{f['dislikes']}**。")
        
        st.divider()
        
        # --- 修改與刪除區 ---
        with st.expander("🛠️ 修改或刪除這位朋友的資料"):
            st.write("在此修改資料後，請按「確認修改」按鈕：")
            # 建立修改用的輸入框，預填原本的資料
            edit_name = st.text_input("修改名字", value=f['name'])
            edit_ints = st.text_input("修改興趣", value=f['interests'])
            edit_lks = st.text_area("修改喜歡", value=f['likes'])
            edit_dlks = st.text_area("修改不喜歡", value=f['dislikes'])
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 確認修改內容"):
                    # 更新記憶體中的該筆資料
                    st.session_state['my_friends'][selected_idx] = {
                        "name": edit_name,
                        "interests": edit_ints,
                        "likes": edit_lks,
                        "dislikes": edit_dlks
                    }
                    st.success("修改已暫存！")
                    st.rerun()
            with c2:
                if st.button("🗑️ 永久刪除此人"):
                    st.session_state['my_friends'].pop(selected_idx)
                    st.warning("已刪除資料。")
                    st.rerun()

# --- 底部下載按鈕 ---
st.divider()
if len(st.session_state.get('my_friends', [])) > 0:
    st.subheader("💾 永久保存我的筆記")
    json_data = json.dumps(st.session_state['my_friends'], ensure_ascii=False, indent=4)
    st.download_button(
        label="📥 儲存並下載最新筆記到手機",
        data=json_data,
        file_name="my_friend_notes.json",
        mime="application/json",
        use_container_width=True
    )
    st.caption("⚠️ 溫馨提示：修改完資料後，必須點擊此處下載新檔案，修改才會生效喔！")