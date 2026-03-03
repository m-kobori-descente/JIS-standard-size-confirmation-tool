import streamlit as st
import pandas as pd

# 簡易パスワード設定
PASSWORD = "CM32A"

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    
    if st.session_state["password_correct"]:
        return True

    st.title("サイズ判定ツール ログイン")
    pwd = st.text_input("パスワードを入力してください", type="password")
    if st.button("ログイン"):
        if pwd == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("パスワードが違います")
    return False

if check_password():
    st.title("🥿 サイズ・ワイズ判定ツール")

    # データの読み込み
    try:
        df = pd.read_csv("data.csv")
        
        # 入力エリア
        st.sidebar.header("入力項目")
        gender = st.sidebar.selectbox("性別", ["男性", "女性"])
        foot_length = st.sidebar.number_input("足長 (mm)", value=250.0, step=1.0)
        foot_circ = st.sidebar.number_input("足囲 (mm)", value=240.0, step=1.0)

        # 判定ロジック
        result = df[
            (df['性別'] == gender) &
            (df['足長最小'] <= foot_length) & (df['足長最大'] >= foot_length) &
            (df['足囲最小'] <= foot_circ) & (df['足囲最大'] >= foot_circ)
        ]

        if not result.empty:
            st.success("判定結果")
            col1, col2 = st.columns(2)
            col1.metric("判定サイズ", f"{result.iloc[0]['サイズ']} cm")
            col2.metric("足囲区分 (ワイズ)", result.iloc[0]['足囲区分'])
        else:
            st.warning("該当するサイズ・ワイズが見つかりませんでした。数値を再確認してください。")

    except Exception as e:

        st.error(f"エラーが発生しました: {e}")
