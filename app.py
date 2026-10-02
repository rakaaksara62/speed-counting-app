import random
import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="PRISMA Kalkulator Tangan",
    page_icon="🧮",
    layout="centered",
)

# ============================================================
# BANK SOAL ASLI KATEGORI II
# ============================================================
ORIGINAL_HORIZONTAL = [
    "6 - 2", "4 + 3", "31 - 8 - 9", "9 + 8 + 52",
    "4 + 2 + 4 + 6", "8 + 3 + 6 + 5", "11 - 8 + 7 + 7",
    "6 + 17 + 9 - 7", "35 - 6 - 7 + 14", "48 - 9 + 8 + 25",
    "34 + 42 - 37", "41 + 41 - 17", "85 - 46 + 23",
    "15 + 36 - 27", "54 - 48 + 17 + 37", "65 + 27 - 17 - 18",
    "37 + 21 - 12 - 28", "44 - 15 + 48 - 38 - 15",
    "18 + 15 - 28 + 37 + 57", "48 + 39 - 36 + 13 - 28 - 14",
    "49 + 37 - 34 - 28 - 18 + 19", "23 + 42 + 61",
    "32 + 45 + 47", "41 + 71 + 22", "54 + 55 - 25",
    "75 + 83 - 94", "93 - 15 + 63", "87 - 19 + 87",
    "81 + 47 - 57", "95 - 17 + 65",
]

ORIGINAL_VERTICAL = [
    (825, 462, "-"), (547, 584, "+"), (326, 547, "+"),
    (622, 478, "-"), (451, 365, "-"), (2365, 214, "+"),
    (5624, 5025, "+"), (6211, 2154, "-"), (7654, 4587, "-"),
    (9875, 2135, "+"),
]


def evaluate_expression(expr):
    tokens = expr.split()
    total = int(tokens[0])
    for i in range(1, len(tokens), 2):
        value = int(tokens[i + 1])
        total = total + value if tokens[i] == "+" else total - value
    return total


def original_category2():
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


# ============================================================
# BANK SOAL ASLI KATEGORI III
# Berdasarkan gambar yang diberikan:
# 1-15  : 2 digit x 1 digit
# 16-30 : 2 digit x 2 digit
# 31-40 : pembagian tepat
# ============================================================
ORIGINAL_CAT3_MULTIPLICATION = [
    (28, 9), (35, 4), (41, 8), (17, 8), (53, 7),
    (64, 5), (75, 6), (88, 2), (99, 3), (76, 5),
    (12, 7), (24, 6), (33, 7), (23, 3), (24, 21),
    (35, 42), (44, 45), (16, 15), (53, 54), (64, 54),
    (21, 26), (43, 39), (54, 26), (79, 67), (85, 67),
    (57, 55), (21, 22), (38, 42), (23, 27), (34, 75),
]

ORIGINAL_CAT3_DIVISION = [
    (16, 2), (20, 5), (30, 6), (45, 9), (56, 4),
    (24, 8), (70, 2), (155, 5), (511, 7), (450, 3),
]


def original_category3():
    questions = []
    for a, b in ORIGINAL_CAT3_MULTIPLICATION:
        questions.append({
            "type": "multiplication",
            "a": a,
            "b": b,
            "answer": a * b,
            "original": True,
        })
    for a, b in ORIGINAL_CAT3_DIVISION:
        questions.append({
            "type": "division",
            "a": a,
            "b": b,
            "answer": a // b,
            "original": True,
        })
    return questions


# ============================================================
# GENERATOR KATEGORI II
# ============================================================
def make_horizontal():
    n = random.choice([2, 2, 2, 3, 3, 4, 5, 6])
    max_num = random.choice([20, 30, 50, 75, 99])
    nums = [random.randint(2, max_num) for _ in range(n)]

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
    digits = random.choice([3, 3, 3, 4])
    lo = 10 ** (digits - 1)
    hi = 10 ** digits - 1
    a = random.randint(lo, hi)
    b = random.randint(lo, hi)
    op = random.choice(["+", "-"])

    # Pengurangan selalu menghasilkan 0 atau positif.
    if op == "-" and b > a:
        a, b = b, a

    return {
        "type": "vertical",
        "a": a,
        "b": b,
        "op": op,
        "answer": a + b if op == "+" else a - b,
        "original": False,
    }


def generate_category2(count):
    original = original_category2()
    if count <= len(original):
        random.shuffle(original)
        return original[:count]
    extra = [make_horizontal() if random.random() < 0.75 else make_vertical()
             for _ in range(count - len(original))]
    random.shuffle(original)
    return original + extra


# ============================================================
# GENERATOR KATEGORI III
# ============================================================
def make_multiplication_easy():
    # Pola nomor 1-15: 2 digit x 1 digit.
    a = random.randint(10, 99)
    b = random.randint(2, 9)
    return {
        "type": "multiplication",
        "a": a,
        "b": b,
        "answer": a * b,
        "original": False,
    }


def make_multiplication_hard():
    # Pola nomor 16-30: 2 digit x 2 digit.
    a = random.randint(10, 99)
    b = random.randint(10, 99)
    return {
        "type": "multiplication",
        "a": a,
        "b": b,
        "answer": a * b,
        "original": False,
    }


def make_division():
    # Pembagian selalu habis, tanpa sisa, seperti contoh.
    divisor = random.randint(2, 9)
    quotient = random.randint(3, 99)
    dividend = divisor * quotient
    return {
        "type": "division",
        "a": dividend,
        "b": divisor,
        "answer": quotient,
        "original": False,
    }


def generate_category3(count):
    original = original_category3()
    if count <= len(original):
        random.shuffle(original)
        return original[:count]

    extra = []
    for _ in range(count - len(original)):
        # Proporsi dibuat mendekati struktur 30 perkalian : 10 pembagian.
        if random.random() < 0.75:
            if random.random() < 0.5:
                extra.append(make_multiplication_easy())
            else:
                extra.append(make_multiplication_hard())
        else:
            extra.append(make_division())

    random.shuffle(original)
    return original + extra


# ============================================================
# FORMAT TAMPILAN
# ============================================================
def format_vertical(q):
    width = max(len(str(q["a"])), len(str(q["b"])))
    return (
        f"{q['a']:>{width}}\n"
        f"{q['op']} {q['b']:>{width-2}}\n"
        f"{'─' * (width + 2)}"
    )


def start_session(questions):
    st.session_state.questions = questions
    st.session_state.index = 0
    st.session_state.started_at = time.monotonic()
    st.session_state.answers = {}
    st.session_state.show_answers = False
    st.session_state.finished = False
    st.session_state.running = True


# ============================================================
# SESSION STATE
# ============================================================
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
    "category": "Kategori II",
    "mode": "Campuran",
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def next_question():
    st.session_state.index += 1
    st.session_state.started_at = time.monotonic()
    if st.session_state.index >= len(st.session_state.questions):
        st.session_state.running = False
        st.session_state.finished = True


# ============================================================
# SIDEBAR
# ============================================================
st.title("🧮 PRISMA Kalkulator Tangan")
st.caption("Latihan cepat bergaya Olimpiade PRISMA")

with st.sidebar:
    st.header("Pengaturan")

    category = st.selectbox(
        "Kategori",
        ["Kategori II", "Kategori III"],
        index=["Kategori II", "Kategori III"].index(st.session_state.category),
    )

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

    if category == "Kategori II":
        modes = ["Campuran", "Horizontal saja", "Vertikal saja"]
    else:
        modes = ["Campuran", "Perkalian saja", "Pembagian saja"]

    current_mode = st.session_state.mode if st.session_state.mode in modes else modes[0]
    mode = st.selectbox("Jenis soal", modes, index=modes.index(current_mode))

    st.session_state.duration = duration
    st.session_state.count = count
    st.session_state.category = category
    st.session_state.mode = mode

    if st.button("Mulai / Acak Soal Baru", use_container_width=True):
        if category == "Kategori II":
            originals = original_category2()
            if mode == "Horizontal saja":
                bank = [q for q in originals if q["type"] == "horizontal"]
                extra = [make_horizontal() for _ in range(max(0, count - len(bank)))]
            elif mode == "Vertikal saja":
                bank = [q for q in originals if q["type"] == "vertical"]
                extra = [make_vertical() for _ in range(max(0, count - len(bank)))]
            else:
                bank = originals
                extra = []
                if count > len(bank):
                    extra = [make_horizontal() if random.random() < 0.75 else make_vertical()
                             for _ in range(count - len(bank))]
            random.shuffle(bank)
            questions = (bank + extra)[:count]
        else:
            originals = original_category3()
            if mode == "Perkalian saja":
                bank = [q for q in originals if q["type"] == "multiplication"]
                extra = [make_multiplication_easy() if random.random() < 0.5
                         else make_multiplication_hard()
                         for _ in range(max(0, count - len(bank)))]
            elif mode == "Pembagian saja":
                bank = [q for q in originals if q["type"] == "division"]
                extra = [make_division() for _ in range(max(0, count - len(bank)))]
            else:
                bank = originals
                extra = []
                if count > len(bank):
                    extra = [
                        (make_multiplication_easy() if random.random() < 0.375
                         else make_multiplication_hard() if random.random() < 0.5
                         else make_division())
                        for _ in range(count - len(bank))
                    ]
            random.shuffle(bank)
            questions = (bank + extra)[:count]

        start_session(questions)
        st.rerun()

    if st.button("Reset", use_container_width=True):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()

# ============================================================
# FINISHED
# ============================================================
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
            elif q["type"] == "vertical":
                question_text = format_vertical(q)
            elif q["type"] == "multiplication":
                question_text = f"{q['a']} × {q['b']}"
            else:
                question_text = f"{q['a']} : {q['b']}"
            user_answer = st.session_state.answers.get(i, "—")
            status = "✓" if user_answer == q["answer"] else "✗"
            st.write(
                f"{i+1}. {question_text.replace(chr(10), ' / ')} "
                f"→ {q['answer']} | Jawabanmu: {user_answer} {status}"
            )

    st.stop()

# ============================================================
# TIMER
# ============================================================
if st.session_state.running:
    st_autorefresh(interval=250, key="timer_refresh")
    elapsed = time.monotonic() - st.session_state.started_at
    remaining = max(0.0, st.session_state.duration - elapsed)

    if remaining <= 0:
        next_question()
        st.rerun()

# ============================================================
# BELUM MULAI
# ============================================================
if not st.session_state.questions:
    st.info("Atur pengaturan di sidebar, lalu tekan **Mulai / Acak Soal Baru**.")
    st.markdown("""
### Kategori II
- Penjumlahan dan pengurangan.
- Hasil tidak pernah negatif.
- Bentuk horizontal dan vertikal.

### Kategori III
- Perkalian 2 digit × 1 digit.
- Perkalian 2 digit × 2 digit.
- Pembagian yang selalu habis tanpa sisa.
- Pola berdasarkan 40 soal pada gambar yang diberikan.
""")
    st.stop()

# ============================================================
# SOAL AKTIF
# ============================================================
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

# Tampilan soal dibuat besar agar lebih nyaman dilihat dari HP.
if q["type"] == "horizontal":
    st.markdown(
        f"<div style='font-size:42px; line-height:1.3; text-align:center; "
        f"font-family:monospace; margin:45px 0;'>{q['text']}</div>",
        unsafe_allow_html=True,
    )

elif q["type"] == "vertical":
    # Lebih besar dari versi sebelumnya.
    vertical = format_vertical(q).replace("\n", "<br>")
    st.markdown(
        f"<div style='font-size:50px; line-height:1.25; text-align:center; "
        f"font-family:monospace; font-weight:600; margin:35px 0;'>"
        f"{vertical}</div>",
        unsafe_allow_html=True,
    )

elif q["type"] == "multiplication":
    # Meniru bentuk kotak pada contoh: angka atas, angka bawah, lalu x.
    st.markdown(
        f"<div style='font-size:50px; line-height:1.35; text-align:center; "
        f"font-family:monospace; font-weight:600; margin:35px 0;'>"
        f"{q['a']}<br>× {q['b']}<br>────────</div>",
        unsafe_allow_html=True,
    )

else:  # division
    st.markdown(
        f"<div style='font-size:50px; line-height:1.3; text-align:center; "
        f"font-family:monospace; font-weight:600; margin:45px 0;'>"
        f"{q['a']} : {q['b']} = ?</div>",
        unsafe_allow_html=True,
    )

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
