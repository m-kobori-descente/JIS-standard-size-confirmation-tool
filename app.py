import streamlit as st
import pandas as pd

# 1. ページの設定（PCでもスマホでも中央に寄せて見やすくする）
st.set_page_config(page_title="サイズ判定ツール", layout="centered")

# 簡易パスワード設定
PASSWORD = "CM32A"

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True
    st.title("🔐 ログイン")
    pwd = st.text_input("パスワードを入力してください", type="password")
    if st.button("ログイン"):
        if pwd == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("パスワードが違います")
    return False

if check_password():
    # 2. タイトル表示
    st.title("👣 サイズ・ワイズ判定 👟")
    st.write("測定値を入力すると、JIS規格に基づいた推奨サイズを表示します。")

    # データの読み込み
    try:
        df = pd.read_csv("data.csv")
    except:
        df = pd.read_csv("data.csv", encoding="cp932")

# 3. 入力フォームの作成
    with st.form("input_form"):
        st.subheader("📏 測定値を入力")
        
        gender = st.radio("性別", ["男性", "女性"], horizontal=True)
        foot_length = st.number_input("足長 (mm)", min_value=100, max_value=350, value=235, step=1, format="%d")
        foot_circ = st.number_input("足囲 (mm)", min_value=100, max_value=350, value=225, step=1, format="%d")
        
        # フォーム専用の送信ボタン
        submitted = st.form_submit_button("結果を見る")

    # 4. ボタンが押されたときだけ判定を実行
    if submitted:
        # 判定ロジック
        result = df[
            (df['性別'] == gender) &
            (df['足長最小'] <= foot_length) & (df['足長最大'] >= foot_length) &
            (df['足囲最小'] <= foot_circ) & (df['足囲最大'] >= foot_circ)
        ]

        st.divider()

        # 5. 結果表示
        if not result.empty:
            size = result.iloc[0]['サイズ']
            wise = result.iloc[0]['足囲区分']
            
            # 演出（スピンさせてからバルーン！）
            with st.spinner('判定中...'):
                import time
                time.sleep(0.5) 

            st.markdown(f"""
                <div style="text-align: center; background-color: #e6f3ff; padding: 30px; border-radius: 15px; border: 2px solid #1e88e5; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <p style="margin: 0; font-size: 18px; color: #1e88e5; font-weight: bold;">あなたの推奨サイズ</p>
                    <h1 style="margin: 10px 0; font-size: 64px; color: #0d47a1; line-height: 1;">{size}<span style="font-size: 28px;">cm</span></h1>
                    <h2 style="margin: 0; font-size: 42px; color: #1565c0;">ワイズ: {wise}</h2>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.warning("⚠️ 該当するサイズが見つかりませんでした。入力値を確認してください。")
    st.caption("※この判定はJIS規格に基づいた目安です。靴の木型によってフィット感は異なります。")



