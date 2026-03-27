import streamlit as st
import pandas as pd
import time

# 1. ページの設定
st.set_page_config(page_title="サイズ判定ツール", layout="centered")

# 簡易パスワード設定（ご自身のものに書き換えてください）
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
    st.title("👟JISサイズ・ワイズ判定👣")

    # データの読み込み
    try:
        df = pd.read_csv("data.csv")
    except:
        df = pd.read_csv("data.csv", encoding="cp932")

    # --- 1. 判定用の空のコンテナを先に用意（結果を上に表示するため） ---
    result_container = st.container()

    # --- 2. 入力フォーム（下側に配置） ---
    with st.form("input_form"):
        st.subheader("📏 測定値を入力")
        i1, i2, i3 = st.columns([1, 1.2, 1.2])
        with i1:
            gender = st.radio("性別", ["男性", "女性"], horizontal=True)
        with i2:
            foot_length = st.number_input("足長 (mm)", min_value=100, max_value=350, value=235, step=1, format="%d")
        with i3:
            foot_circ = st.number_input("足囲 (mm)", min_value=100, max_value=350, value=225, step=1, format="%d")
        
        submitted = st.form_submit_button("判定して結果を見る", use_container_width=True)

    # --- 3. 判定ロジックと結果表示 ---
    if submitted:
        result = df[
            (df['性別'] == gender) &
            (df['足長最小'] <= foot_length) & (df['足長最大'] >= foot_length) &
            (df['足囲最小'] <= foot_circ) & (df['足囲最大'] >= foot_circ)
        ]

        with result_container:
            st.divider()
            if not result.empty:
                size = result.iloc[0]['サイズ']
                wise = result.iloc[0]['足囲区分']
                
                with st.spinner('判定中...'):
                    time.sleep(0.4) 

                st.write("### 🎉 判定結果")
                
                col1, col2 = st.columns(2, gap="small")
                box_base = """
                    display: flex; flex-direction: column; justify-content: center; align-items: center;
                    text-align: center; height: 140px; width: 100%; margin: 0 auto 10px auto;
                    border-radius: 15px; border: 2px solid #1e88e5; box-shadow: 0 4px 10px rgba(30,136,229,0.2);
                    box-sizing: border-box;
                """
                val_style = "display: flex; justify-content: center; align-items: baseline; width: 100%;"

                with col1:
                    st.markdown(f"""
                        <div style="{box_base} background-color: #e6f3ff;">
                            <p style="margin: 0; font-size: 14px; color: #1e88e5; font-weight: bold;">あなたのサイズ</p>
                            <div style="{val_style}">
                                <span style="font-size: 38px; color: #0d47a1; font-weight: bold; line-height: 1;">{size}</span>
                                <span style="font-size: 18px; color: #0d47a1; margin-left: 3px;">cm</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                        <div style="{box_base} background-color: #f0f8ff;">
                            <p style="margin: 0; font-size: 14px; color: #1e88e5; font-weight: bold;">ワイズ</p>
                            <div style="{val_style}">
                                <span style="font-size: 40px; color: #0d47a1; font-weight: bold; line-height: 1;">{wise}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # --- カスタマイズした大きなアドバイス文言 ---
                st.markdown(f"""
                    <div style="background-color: #fff9c4; padding: 15px; border-radius: 10px; border-left: 8px solid #fbc02d; margin: 15px 0;">
                        <p style="margin: 0; font-size: 22px; color: #333; font-weight: bold; line-height: 1.4;">
                            💡 普段履きの場合、<br>「判定＋0.5～1cmの靴」がおすすめです
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                st.write("---") 
            else:
                st.warning("⚠️ 該当するサイズが見つかりませんでした。入力値を確認してください。")

    st.caption("※JIS規格に基づいた目安です。実際のフィット感は靴の木型により異なります。")
