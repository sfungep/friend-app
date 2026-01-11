import streamlit as st
import json
import base64
from datetime import date
from PIL import Image
import io

st.set_page_config(page_title="私人朋友筆記本", layout="wide")

# --- 1. 初始化 ---
if 'my_friends' not in st.session_state:
    st.session_state['my_friends'] = []

# --- 2. 輔助功能 ---
def img_to_base64(img_file):
    if img_file is not None:
        try:
            img = Image.open(img_file)
            img.thumbnail((300, 300))
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode()
        except:
            return None
    return None

# --- 3. 側邊欄檔案管理 ---
st.sidebar.title("📁 檔案管理")
uploaded_file = st.sidebar.file_uploader("選取你的筆記檔 (.json)", type="json")
if uploaded_file is not None and not st.session_state['my_friends']:
    st.session_state['my_friends'] = json.load(uploaded_file)
    st.sidebar.success("讀取成功！")

# --- 4. 主要內容 ---
st.title("💾 我的私人朋友筆記")
tab1, tab2 = st.tabs(["👀 溫習與社交建議", "➕ 新增朋友"])

with tab2:
    st.subheader("📝 記錄新朋友")
    with st.form("add_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("朋友名字")
            birthday = st.date_input("生日日期", value=date(2010, 1, 1))
            siblings = st.text_input("有哪些兄弟姐妹？")
        with col_b:
            photo = st.file_uploader("上傳朋友相片", type=['jpg', 'png', 'jpeg'])
            ints = st.text_input("主要興趣 (例如：地鐵、巴士、繪畫)")
        
        lks = st.text_area("喜歡的東西", placeholder="例如：顏色、食物、運動、學科、遊戲、地方")
        dlks = st.text_area("他不喜歡/害怕的事 (避雷區)")
        
        if st.form_submit_button("暫存到清單"):
            if name:
                encoded_img = img_to_base64(photo)
                new_entry = {
                    "name": name, "birthday": str(birthday), "siblings": siblings,
                    "interests": ints, "likes": lks, "dislikes": dlks,
                    "photo": encoded_img, "last_updated": str(date.today())
                }
                st.session_state['my_friends'].append(new_entry)
                st.success(f"已暫存 {name}！請記得在下方下載存檔。")
                st.rerun()

with tab1:
    current_list = st.session_state.get('my_friends', [])
    if not current_list:
        st.info("請先讀取舊檔或新增朋友。")
    else:
        friend_names = [f["name"] for f in current_list]
        selected_idx = st.selectbox("你想溫習誰？", range(len(friend_names)), format_func=lambda x: friend_names[x])
        f = current_list[selected_idx]

        # --- 朋友概覽 ---
        col_img, col_info = st.columns([1, 2])
        with col_img:
            if f.get('photo'):
                st.image(base64.b64decode(f['photo']), width=200)
            else:
                st.info("無相片")
        with col_info:
            st.header(f"{f['name']}")
            st.write(f"🎂 **生日：** {f.get('birthday')} | 👨‍👩‍👧‍👦 **家族：** {f.get('siblings')}")
            st.caption(f"📅 資訊最後更新：{f.get('last_updated')}")

        st.divider()

        # --- 社交建議 (根據你的建議修改) ---
        topic = f.get('interests') if f.get('interests') else (f.get('likes') if f.get('likes') else "你喜歡的東西")
        topic_short = (topic[:15] + '..') if len(topic) > 15 else topic

        st.subheader("💡 社交教練：嘗試用「六何法」聊天")
        col_tips, col_warn = st.columns(2)
        
        with col_tips:
            st.info(f"✅ **與 {f['name']} 開啟話題：**")
            st.write(f"**何人：** 「除了你，還有誰也喜歡 **{topic_short}** 嗎？」")
            st.write(f"**何時：** 「你通常在什麼時候睇/玩有關 **{topic_short}** 的東西？」")
            st.write(f"**何地：** 「你最喜歡在哪裡看/玩有關 **{topic_short}** 的東西？」")
            st.write(f"**何事：** 「關於 **{topic_short}**，你最近有什麼新發現嗎？」")
            st.write(f"**為何：** 「為什麼你會對 **{topic_short}** 這麼感興趣？」")
            st.write(f"**如何：** 「如果我想學/試試有關 **{topic_short}**，要怎麼開始？」")
        
        with col_warn:
            st.error("🚫 **避雷提醒 (絕對不要談及)：**")
            if f.get('dislikes'):
                st.markdown(f"### 👉 **{f['dislikes']}**")
                st.warning("⚠️ **如果對方不開心了：**\n\n可以說：「對不起，我們換個話題吧。」然後改聊他喜歡的內容。")
            else:
                st.write("目前尚未記錄地雷。")

        # --- 修改功能 ---
        st.divider()
        with st.expander("🛠️ 修改或刪除資料"):
            edit_name = st.text_input("修改名字", value=f['name'])
            edit_ints = st.text_input("修改興趣", value=f['interests'])
            edit_lks = st.text_area("修改喜歡", value=f['likes'])
            edit_dlks = st.text_area("修改不喜歡", value=f['dislikes'])
            edit_siblings = st.text_input("修改兄弟姐妹", value=f.get('siblings',''))
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 確認並暫存修改"):
                    st.session_state['my_friends'][selected_idx].update({
                        "name": edit_name,
                        "interests": edit_ints,
                        "likes": edit_lks,
                        "dislikes": edit_dlks,
                        "siblings": edit_siblings,
                        "last_updated": str(date.today())
                    })
                    st.success("修改已暫存！")
                    st.rerun()
            with c2:
                if st.button("🗑️ 刪除此人"):
                    st.session_state['my_friends'].pop(selected_idx)
                    st.rerun()

# --- 底部下載按鈕 ---
st.divider()
if len(st.session_state.get('my_friends', [])) > 0:
    json_data = json.dumps(st.session_state['my_friends'], ensure_ascii=False, indent=4)
    st.download_button(
        label="📥 儲存並下載最新筆記到手機 (永久保存)",
        data=json_data,
        file_name="my_social_notes.json",
        mime="application/json",
        use_container_width=True
    )