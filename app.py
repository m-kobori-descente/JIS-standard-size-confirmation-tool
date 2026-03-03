import streamlit as st
import pandas as pd
import time

# 1. ページの設定（中央寄せでプロっぽく）
st.set_page_config(page_title="サイズ判定ツール", layout="centered")

# 簡易パスワード設定（ここを自身のパスワードに！）
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
    st.title("🥿 サイズ・ワイズ判定")
    st.write("測定値を入力して「結果を見る」を押してください。")

    # データの読み込み
    try:
        df = pd.read_csv("data.csv")
    except:
        df = pd.read_csv("data.csv", encoding="cp932")

    # 3. 入力フォーム（ボタンを押すまで判定しない）
    with st.form("input_form"):
        st.subheader("📏 測定値を入力")
        
        gender = st.radio("性別", ["男性", "女性"], horizontal=True)
        
        # 数値入力（整数表示）
        foot_length = st.number_input("足長 (mm)", min_value=100, max_value=350, value=235, step=1, format="%d")
        foot_circ = st.number_input("足囲 (mm)", min_value=100, max_value=350, value=225, step=1, format="%d")
        
        # 送信ボタン
        submitted = st.form_submit_button("結果を見る")

    # 4. ボタンが押された時の処理
    if submitted:
        # 判定ロジック
        result = df[
            (df['性別'] == gender) &
            (df['足長最小'] <= foot_length) & (df['足長最大'] >= foot_length) &
            (df['足囲最小'] <= foot_circ) & (df['足囲最大'] >= foot_circ)
        ]

        st.divider()

        if not result.empty:
            size = result.iloc[0]['サイズ']
            wise = result.iloc[0]['足囲区分']
            
            # 演出：一瞬だけ「判定中...」と出す
            with st.spinner('判定中...'):
                time.sleep(0.5) 

            # 5. 結果を横並びに表示
            st.write("### 判定結果")
            
            col1, col2 = st.columns(2)
            
            # 左右・上下中央揃えを徹底するスタイル
            box_style = """
                display: flex; 
                flex-direction: column; 
                justify-content: center; 
                align-items: center; 
                text-align: center; 
                height: 150px; 
                border-radius: 15px; 
                border: 2px solid #1e88e5; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                width: 100%;
            """
            
            with col1:
                st.markdown(f"""
                    <div style="{box_style} background-color: #e6f3ff;">
                        <div style="width: 100%;">
                            <p style="margin: 0; font-size: 14px; color: #1e88e5; font-weight: bold; width: 100%;">推奨サイズ</p>
                            <h1 style="margin: 5px 0 0 0; font-size: 40px; color: #0d47a1; line-height: 1.2; width: 100%;">{size}<span style="font-size: 18px;">cm</span></h1>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div style="{box_style} background-color: #f0f8ff;">
                        <div style="width: 100%;">
                            <p style="margin: 0; font-size: 14px; color: #1e88e5; font-weight: bold; width: 100%;">ワイズ</p>
                            <h1 style="margin: 5px 0 0 0; font-size: 40px; color: #0d47a1; line-height: 1.2; width: 100%;">{wise}</h1>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
        else:
            st.warning("⚠️ 該当するサイズが見つかりませんでした。入力値を確認してください。")

    st.caption("※JIS規格に基づいた目安です。実際のフィット感は靴の木型により異なります。")




