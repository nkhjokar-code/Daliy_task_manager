import streamlit as st

st.set_page_config(
    page_title="مدیریت کارهای روزانه",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- ظاهر فانتزی و سازگار با موبایل ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Vazirmatn', sans-serif;
    direction: rtl;
}
.stApp {
    background:
      radial-gradient(circle at 12% 12%, rgba(255,255,255,.85) 0 3px, transparent 4px),
      radial-gradient(circle at 85% 22%, rgba(255,255,255,.7) 0 4px, transparent 5px),
      linear-gradient(145deg, #ffe3f1 0%, #f0e5ff 48%, #dff4ff 100%);
    background-attachment: fixed;
}
.block-container {
    max-width: 720px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p, label, span, div {
    text-align: right;
}
.hero {
    background: linear-gradient(135deg, rgba(255,255,255,.88), rgba(255,245,252,.78));
    border: 1px solid rgba(255,255,255,.95);
    border-radius: 26px;
    padding: 22px 20px;
    box-shadow: 0 10px 30px rgba(146, 104, 170, .13);
    text-align: center;
    margin-bottom: 18px;
}
.hero h1 {
    color: #8d4c91;
    font-size: 1.75rem;
    font-weight: 800;
    text-align: center;
    margin: 0 0 8px 0;
}
.hero p {
    color: #765e83;
    text-align: center;
    margin: 0;
}
div[data-testid="stForm"], div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,.76);
    border: 1px solid rgba(255,255,255,.9);
    border-radius: 22px;
    padding: 14px;
    box-shadow: 0 7px 22px rgba(146, 104, 170, .09);
}
.stTextInput input {
    border-radius: 14px;
    border: 1px solid #e5c8ee;
    background: #fffaff;
    text-align: right;
}
.stButton button, .stFormSubmitButton button {
    border: 0;
    border-radius: 15px;
    background: linear-gradient(100deg, #d88acb, #a88be8);
    color: white;
    font-weight: 700;
    min-height: 2.7rem;
    box-shadow: 0 5px 13px rgba(168, 139, 232, .22);
}
.stButton button:hover, .stFormSubmitButton button:hover {
    color: white;
    border: 0;
    background: linear-gradient(100deg, #c875bb, #9273d7);
}
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #e78bc9, #9c8be9);
}
div[data-testid="stCheckbox"] {
    background: rgba(255,255,255,.72);
    border-radius: 13px;
    padding: 8px 10px;
}
hr {
    border-color: rgba(177, 139, 202, .25);
}
@media (max-width: 600px) {
    .block-container { padding: 1rem .8rem 2rem .8rem; }
    .hero { padding: 18px 12px; border-radius: 20px; }
    .hero h1 { font-size: 1.4rem; }
    .stButton button { width: 100%; }
}
</style>
""", unsafe_allow_html=True)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "next_id" not in st.session_state:
    st.session_state.next_id = 1

st.markdown("""
<div class="hero">
  <h1>🌸 مدیریت کارهای روزانه 🌸</h1>
  <p>با قدم‌های کوچک، هر روز به هدف‌هایت نزدیک‌تر شو ✨</p>
</div>
""", unsafe_allow_html=True)

with st.form("task_form", clear_on_submit=True):
    new_task_title = st.text_input("💗 عنوان کار جدید:", placeholder="مثلاً: مطالعه، ورزش، انجام تکالیف...")
    submitted = st.form_submit_button("➕ افزودن کار", use_container_width=True)

    if submitted:
        if new_task_title.strip():
            st.session_state.tasks.append({
                "id": st.session_state.next_id,
                "title": new_task_title.strip(),
                "completed": False
            })
            st.session_state.next_id += 1
            st.success("کار جدید با موفقیت اضافه شد! 🌷")
            st.rerun()
        else:
            st.warning("لطفاً عنوان کار را وارد کنید.")

st.divider()
st.subheader("📋 فهرست کارهای من")

if not st.session_state.tasks:
    st.info("هنوز کاری ثبت نشده است. اولین کار امروزت را اضافه کن! 💕")
else:
    completed_count = sum(1 for task in st.session_state.tasks if task["completed"])
    total_count = len(st.session_state.tasks)
    progress = completed_count / total_count

    st.progress(progress)
    st.markdown(
        f"<p style='color:#79558b;font-weight:700'>🌟 پیشرفت امروز: {completed_count} از {total_count} کار</p>",
        unsafe_allow_html=True
    )

    st.divider()

    for task in st.session_state.tasks:
        col1, col2 = st.columns([0.78, 0.22])
        with col1:
            is_checked = st.checkbox(
                task["title"],
                value=task["completed"],
                key=f"task_{task['id']}"
            )
            if is_checked != task["completed"]:
                task["completed"] = is_checked
                st.rerun()

        with col2:
            if st.button("🗑️ حذف", key=f"del_{task['id']}", use_container_width=True):
                st.session_state.tasks = [
                    t for t in st.session_state.tasks if t["id"] != task["id"]
                ]
                st.rerun()

if st.session_state.tasks:
    st.divider()
    if st.button("🧹 پاک کردن کل فهرست", use_container_width=True):
        st.session_state.tasks = []
        st.session_state.next_id = 1
        st.rerun()

st.markdown(
    "<p style='text-align:center;color:#9678a5;font-size: .85rem'>ساخته‌شده با عشق و رنگ‌های خیال‌انگیز 🌸</p>",
    unsafe_allow_html=True
)
