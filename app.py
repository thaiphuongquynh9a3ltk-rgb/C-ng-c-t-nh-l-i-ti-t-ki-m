import streamlit as st
st.image("st.image("logo.jpg").JPG")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm_Thái Phương Quỳnh",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 Tính lãi gửi tiết kiệm_Thái Phương Quỳnh")

st.write(
    "Nhập thông tin khoản tiền gửi để tính tiền lãi định kỳ, "
    "tổng tiền lãi và tổng số tiền nhận được."
)

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================

so_tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0,
    value=100_000_000,
    step=1_000_000,
    format="%d"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_nhan_lai = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 Tính lãi", type="primary", use_container_width=True):

    # Chuyển lãi suất từ % sang số thập phân
    lai_suat_nam = lai_suat / 100

    # Tổng tiền lãi theo kỳ hạn
    tong_tien_lai = so_tien_gui * lai_suat_nam * ky_han / 12

    # Tính tiền lãi định kỳ
    if hinh_thuc_nhan_lai == "Cuối kỳ":
        tien_lai_dinh_ky = tong_tien_lai
        so_ky_nhan_lai = 1
        ten_ky = "cuối kỳ"

    elif hinh_thuc_nhan_lai == "Hàng tháng":
        tien_lai_dinh_ky = so_tien_gui * lai_suat_nam / 12
        so_ky_nhan_lai = ky_han
        ten_ky = "mỗi tháng"

    else:  # Hàng quý
        tien_lai_dinh_ky = so_tien_gui * lai_suat_nam * 3 / 12

        # Số quý đầy đủ
        so_quy = ky_han // 3
        thang_le = ky_han % 3

        # Nếu có tháng lẻ thì có thêm một kỳ nhận lãi
        so_ky_nhan_lai = so_quy + (1 if thang_le > 0 else 0)
        ten_ky = "mỗi quý"

    # Tổng gốc + lãi
    tong_goc_va_lai = so_tien_gui + tong_tien_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.divider()
    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label=f"Tiền lãi {ten_ky}",
            value=dinh_dang_tien(tien_lai_dinh_ky)
        )

        st.metric(
            label="Tổng tiền lãi",
            value=dinh_dang_tien(tong_tien_lai)
        )

    with col2:
        st.metric(
            label="Tiền gốc",
            value=dinh_dang_tien(so_tien_gui)
        )

        st.metric(
            label="Tổng gốc + lãi",
            value=dinh_dang_tien(tong_goc_va_lai)
        )

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================

    st.subheader("📋 Chi tiết khoản tiền gửi")

    st.write(f"**Số tiền gửi:** {dinh_dang_tien(so_tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
    st.write(f"**Số kỳ nhận lãi:** {so_ky_nhan_lai}")

    st.success(
        f"💵 Tổng số tiền gốc và lãi: "
        f"**{dinh_dang_tien(tong_goc_va_lai)}**"
    )

    # =========================
    # GIẢI THÍCH CÔNG THỨC
    # =========================

    with st.expander("Xem công thức tính"):
        st.write("**Tổng tiền lãi:**")
        st.code(
            "Tiền lãi = Tiền gửi × (Lãi suất / 100) × Kỳ hạn / 12"
        )

        st.write("**Tổng tiền nhận được:**")
        st.code(
            "Tổng tiền = Tiền gốc + Tổng tiền lãi"
        )

st.divider()

st.caption(
    "Lưu ý: Kết quả chỉ mang tính tham khảo. "
    "Cách tính thực tế có thể khác tùy quy định của từng ngân hàng."
)
