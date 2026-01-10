import streamlit as st
import sqlite3
import pandas as pd

# --- 資料庫邏輯 ---
def init_db():
    conn = sqlite3.connect('friends.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS friends 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, interests TEXT, likes TEXT, dislikes TEXT, notes TEXT)''')
    conn.commit()
    conn.close()

def get_all_friends():
    conn = sqlite3.connect('friends.db')
    df = pd.read_sql_query("SELECT * FROM friends", conn)
    conn.close()
    return df

# --- 介面開始 ---
init_db()
st.set_page_config(page_title="我的朋友筆記本", layout="wide")

st.sidebar.title("功能選單")
page = st.sidebar.radio("跳轉至：", ["📝 記錄新朋友", "👀 查看與修改"])

if page == "📝 記錄新朋友":
    st.title("📝 錄入新朋友資料")
    with st.form("my_form"):
        name = st.text_input("姓名")
        ints = st.text_input("興趣")
        lks = st.text_area("喜歡")
        dlks = st.text_area("不喜歡")
        nts = st.text_area("備註")
        if st.form_submit_button("儲存"):
            conn = sqlite3.connect('friends.db')
            conn.execute("INSERT INTO friends (name,interests,likes,dislikes,notes) VALUES (?,?,?,?,?)", (name,ints,lks,dlks,nts))
            conn.commit()
            conn.close()
            st.success("儲存成功！")

elif page == "👀 查看與修改":
    st.title("👀 溫習與編輯")
    df = get_all_friends()
    
    if df.empty:
        st.write("目前資料庫是空的。")
    else:
        # 1. 選擇朋友
        friend_names = df['name'].tolist()
        choice = st.selectbox("你想看誰的資料？", friend_names)
        
        # 2. 抓取資料
        data = df[df['name'] == choice].iloc[0]
        fid = int(data['id'])
        
        # 3. 顯示區 (用醒目的框框)
        st.markdown(f"### 📋 {choice} 的個人檔案")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**🌟 興趣：**\n\n{data['interests']}")
            st.success(f"**❤️ 喜歡：**\n\n{data['likes']}")
        with col2:
            st.error(f"**🚫 不喜歡：**\n\n{data['dislikes']}")
            st.warning(f"**📌 備忘：**\n\n{data['notes']}")

        st.divider()

        # 4. 編輯區 (直接顯示，不再隱藏)
        st.subheader("🛠️ 編輯資料（如需修改請直接在下方輸入）")
        
        # 使用 key 確保每個輸入框是唯一的
        new_name = st.text_input("修改姓名", value=data['name'], key="un")
        new_ints = st.text_input("修改興趣", value=data['interests'], key="ui")
        new_lks = st.text_area("修改喜歡", value=data['likes'], key="ul")
        new_dlks = st.text_area("修改不喜歡", value=data['dislikes'], key="ud")
        new_nts = st.text_area("修改備註", value=data['notes'], key="unot")
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("💾 儲存修改內容"):
                conn = sqlite3.connect('friends.db')
                conn.execute("UPDATE friends SET name=?, interests=?, likes=?, dislikes=?, notes=? WHERE id=?",
                             (new_name, new_ints, new_lks, new_dlks, new_nts, fid))
                conn.commit()
                conn.close()
                st.success("修改成功！正在刷新...")
                st.rerun()
        
        with c_btn2:
            if st.button("🗑️ 刪除此人資料"):
                conn = sqlite3.connect('friends.db')
                conn.execute("DELETE FROM friends WHERE id=?", (fid,))
                conn.commit()
                conn.close()
                st.warning("已刪除！")
                st.rerun()
