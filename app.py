
import random
import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="PRISMA Kalkulator Tangan",
    page_icon="🧮",
    layout="centered",
)

# -----------------------------
# Question generation
# -----------------------------
# Soal asli dari gambar/kisi-kisi yang diberikan.
ORIGINAL_HORIZONTAL = [
    "6 - 2",
    "4 + 3",
    "31 - 8 - 9",
    "9 + 8 + 52",
    "4 + 2 + 4 + 6",
    "8 + 3 + 6 + 5",
    "11 - 8 + 7 + 7",
    "6 + 17 + 9 - 7",
    "35 - 6 - 7 + 14",
    "48 - 9 + 8 + 25",
    "34 + 42 - 37",
    "41 + 41 - 17",
    "85 - 46 + 23",
    "15 + 36 - 27",
    "54 - 48 + 17 + 37",
    "65 + 27 - 17 - 18",
    "37 + 21 - 12 - 28",
    "44 - 15 + 48 - 38 - 15",
    "18 + 15 - 28 + 37 + 57",
    "48 + 39 - 36 + 13 - 28 - 14",
    "49 + 37 - 34 - 28 - 18 + 19",
    "23 + 42 + 61",
    "32 + 45 + 47",
    "41 + 71 + 22",
    "54 + 55 - 25",
    "75 + 83 - 94",
    "93 - 15 + 63",
    "87 - 19 + 87",
    "81 + 47 - 57",
    "95 - 17 + 65",
]

ORIGINAL_VERTICAL = [
    (825, 462, "-"),
    (547, 584, "+"),
    (326, 547, "+"),
    (622, 478, "-"),
    (451, 365, "-"),
    (2365, 214, "+"),
    (5624, 5025, "+"),
    (6211, 2154, "-"),
    (7654, 4587, "-"),
    (9875, 2135, "+"),
]


def evaluate_expression(expr):
    # Only + and - are used, matching the supplied worksheet.
    total = 0
    tokens = expr.split()
    total = int(tokens[0])
    for i in range(1, len(tokens), 2):
        value = int(tokens[i + 1])
        total = total + value if tokens[i] == "+" else total - value
    return total


def original_questions():
    questions = []
    for text in ORIGINAL_HORIZONTAL:
        questions.append({
            "type": "horizontal",
            "text": text,
            "answer": evaluate_expression(text),
            "original": True,
        })
    for a, b, op in ORIGINAL_VERTICAL:
        questions.append({
            "type": "vertical",
            "a": a,
            "b": b,
            "op": op,
            "answer": a + b if op == "+" else a - b,
            "original": True,
        })
    return questions


def make_horizontal():
    """Generate questions similar to items 1-30."""
    n = random.choice([2, 2, 2, 3, 3, 4, 5, 6])
    max_num = random.choice([20, 30, 50, 75, 99])
    nums = [random.randint(2, max_num) for _ in range(n)]

    # Start with addition/subtraction and make sure the running result
    # never becomes negative.
    result = nums[0]
    ops = []
    for i in range(1, n):
        possible = ["+"]
        if result >= nums[i]:
            possible.append("-")
        op = random.choice(possible)
        ops.append(op)
        result = result + nums[i] if op == "+" else result - nums[i]

    expression = str(nums[0])
    for op, num in zip(ops, nums[1:]):
        expression += f" {op} {num}"

    return {
        "type": "horizontal",
        "text": expression,
        "answer": result,
        "original": False,
    }


def make_vertical():
    """Generate 2-line addition/subtraction similar to items 31-40."""
    digits = random.choice([3, 3, 3, 4])
    lo = 10 ** (digits - 1)
    hi = 10 ** digits - 1

    a = random.randint(lo, hi)
    b = random.randint(lo, hi)

    op = random.choice(["+", "-"])
    if op == "-" and b > a:
        a, b = b, a

    result = a + b if op == "+" else a - b

    return {
        "type": "vertical",
        "a": a,
        "b": b,
        "op": op,
        "answer": result,
        "original": False,
    }


def make_question():
    # Same broad balance as the sheet: 30 horizontal + 10 vertical.
    if random.random() < 0.75:
        return make_horizontal()
    return make_vertical()


def format_vertical(q):
    width = max(len(str(q["a"])), len(str(q["b"])))
    return (
        f"{q['a']:>{width}}\n"
        f"{q['op']} {q['b']:>{width-2}}\n"
        f"{'-' * (width + 2)}"
    )


def generate_set(count):
    original = original_questions()
    if count <= len(original):
        # Shuffle the 40 supplied questions so the original worksheet
        # remains available while the order changes.
        random.shuffle(original)
        return original[:count]

    extra = [make_question() for _ in range(count - len(original))]
    random.shuffle(original)
    return original + extra


# -----------------------------
# Session state
# -----------------------------
defaults = {
    "running": False,
    "questions": [],
    "index": 0,
    "started_at": None,
    "answers": {},
    "show_answers": False,
    "finished": False,
    "duration": 5,
    "count": 40,
    "mode": "Campuran",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def start_test():
    st.session_state.questions = generate_set(st.session_state.count)
    st.session_state.index = 0
    st.session_state.started_at = time.monotonic()
    st.session_state.answers = {}
    st.session_state.show_answers = False
    st.session_state.finished = False
    st.session_state.running = True


def next_question():
    st.session_state.index += 1
    st.session_state.started_at = time.monotonic()
    if st.session_state.index >= len(st.session_state.questions):
        st.session_state.running = False
        st.session_state.finished = True


# -----------------------------
# Sidebar / settings
# -----------------------------
st.title("🧮 PRISMA Kalkulator Tangan")
st.caption("Latihan cepat bergaya Olimpiade PRISMA Kategori II")

with st.sidebar:
    st.header("Pengaturan")
    duration = st.slider(
        "Waktu per soal (detik)",
        min_value=1,
        max_value=60,
        value=st.session_state.duration,
    )
    count = st.slider(
        "Jumlah soal",
        min_value=10,
        max_value=200,
        value=st.session_state.count,
        step=10,
    )
    mode = st.selectbox(
        "Jenis soal",
        ["Campuran", "Horizontal saja", "Vertikal saja"],
        index=["Campuran", "Horizontal saja", "Vertikal saja"].index(
            st.session_state.mode
        ),
    )

    st.session_state.duration = duration
    st.session_state.count = count
    st.session_state.mode = mode

    if st.button("Mulai / Acak Soal Baru", use_container_width=True):
        originals = original_questions()
        if mode == "Horizontal saja":
            bank = [q for q in originals if q["type"] == "horizontal"]
            extra = [make_horizontal() for _ in range(max(0, count - len(bank)))]
            random.shuffle(bank)
            st.session_state.questions = (bank + extra)[:count]
        elif mode == "Vertikal saja":
            bank = [q for q in originals if q["type"] == "vertical"]
            extra = [make_vertical() for _ in range(max(0, count - len(bank)))]
            random.shuffle(bank)
            st.session_state.questions = (bank + extra)[:count]
        else:
            st.session_state.questions = generate_set(count)

        st.session_state.index = 0
        st.session_state.started_at = time.monotonic()
        st.session_state.answers = {}
        st.session_state.show_answers = False
        st.session_state.finished = False
        st.session_state.running = True
        st.rerun()

    if st.button("Reset", use_container_width=True):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()

# -----------------------------
# Finished screen
# -----------------------------
if st.session_state.finished:
    st.success("Selesai.")
    total = len(st.session_state.questions)
    correct = 0
    answered = 0

    for i, q in enumerate(st.session_state.questions):
        user_answer = st.session_state.answers.get(i)
        if user_answer is not None:
            answered += 1
            if user_answer == q["answer"]:
                correct += 1

    st.metric("Benar", f"{correct}/{total}")
    st.write(f"Terjawab: {answered}/{total}")

    if st.button("Tampilkan kunci jawaban"):
        st.session_state.show_answers = True

    if st.session_state.show_answers:
        st.subheader("Kunci")
        for i, q in enumerate(st.session_state.questions):
            if q["type"] == "horizontal":
                question_text = q["text"]
            else:
                question_text = format_vertical(q)
            user_answer = st.session_state.answers.get(i, "—")
            status = "✓" if user_answer == q["answer"] else "✗"
            st.write(f"{i+1}. {question_text.replace(chr(10), ' / ')} → {q['answer']} | Jawabanmu: {user_answer} {status}")

    st.stop()


# -----------------------------
# Timer
# -----------------------------
if st.session_state.running:
    # Refresh often enough to make the countdown responsive.
    st_autorefresh(interval=250, key="timer_refresh")

    elapsed = time.monotonic() - st.session_state.started_at
    remaining = max(0.0, st.session_state.duration - elapsed)

    if remaining <= 0:
        next_question()
        st.rerun()

# -----------------------------
# Main question
# -----------------------------
if not st.session_state.questions:
    st.info("Atur waktu dan jumlah soal di sidebar, lalu tekan **Mulai / Acak Soal Baru**.")
    st.markdown("""
### Pola soal
- Operasi horizontal seperti `35 − 6 − 7 + 14`
- Operasi horizontal dengan 2–6 bilangan
- Penjumlahan/pengurangan vertikal 3–4 digit
- Soal diacak setiap sesi
- Waktu setiap soal dapat diatur sendiri
""")
    st.stop()

q = st.session_state.questions[st.session_state.index]
num = st.session_state.index + 1
total = len(st.session_state.questions)

st.progress(num / total)
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Soal {num} / {total}**")
with col2:
    if st.session_state.running:
        st.write(f"**⏱ {remaining:.1f} detik**")

# Large question display
if q["type"] == "horizontal":
    st.markdown(
        f"<div style='font-size:42px; text-align:center; "
        f"font-family:monospace; margin:55px 0;'>{q['text']}</div>",
        unsafe_allow_html=True,
    )
else:
    vertical = format_vertical(q)
    st.code(vertical, language=None)

# Answer box is optional and does not pause the timer.
answer = st.number_input(
    "Jawabanmu",
    value=st.session_state.answers.get(st.session_state.index, 0),
    step=1,
    key=f"answer_{st.session_state.index}",
)
st.session_state.answers[st.session_state.index] = int(answer)

if st.button("Lewati sekarang →", use_container_width=True):
    next_question()
    st.rerun()

st.caption("Soal akan berpindah otomatis ketika waktu habis. Isi jawaban sebelum berganti jika ingin menghitung skor.")
